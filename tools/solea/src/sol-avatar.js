import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

const STATES = new Set(['idle', 'thinking', 'happy', 'talking']);
const DURATION = 4;
const RAY_COUNT = 18;
const FPS = 30;
const modelCache = new Map();

function loadModel(url) {
  if (!modelCache.has(url)) {
    modelCache.set(url, new GLTFLoader().loadAsync(url).then(gltf => gltf.scene));
  }
  return modelCache.get(url);
}

class SolAvatar extends HTMLElement {
  static get observedAttributes() { return ['state']; }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this.shadowRoot.innerHTML = `
      <style>
        :host { display: inline-block; width: 128px; height: 128px; contain: layout paint; }
        .frame { position: relative; width: 100%; height: 100%; }
        canvas, img { position: absolute; inset: 0; width: 100%; height: 100%; display: block; }
        img { object-fit: contain; transition: opacity 180ms ease-out; }
        canvas { opacity: 0; transition: opacity 180ms ease-out; }
        .ready canvas { opacity: 1; }
        .ready img { opacity: 0; }
        @media (prefers-reduced-motion: reduce) { canvas, img { transition: none; } }
      </style>
      <div class="frame">
        <img alt="" aria-hidden="true">
        <div class="mount" aria-hidden="true"></div>
      </div>`;
    this.frame = this.shadowRoot.querySelector('.frame');
    this.poster = this.shadowRoot.querySelector('img');
    this.mount = this.shadowRoot.querySelector('.mount');
    this.playing = false;
    this.visible = true;
    this.ready = false;
    this.elapsed = 0;
    this.lastFrame = 0;
    this.raf = 0;
    this.reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  }

  connectedCallback() {
    this.setAttribute('role', 'img');
    // Interactive: she turns her face and eyes towards the pointer anywhere on the page, smiles
    // when hovered and gives a little jump and a spin of her rays when poked.
    this.pointer = { x: 0, y: 0, at: -1e9 };
    this.onPointerMove = event => {
      const r = this.getBoundingClientRect();
      const cx = r.left + r.width / 2;
      const cy = r.top + r.height / 2;
      this.pointer.x = Math.max(-1, Math.min(1, (event.clientX - cx) / (innerWidth * 0.45)));
      this.pointer.y = Math.max(-1, Math.min(1, (cy - event.clientY) / (innerHeight * 0.45)));
      this.pointer.at = performance.now();
    };
    this.onEnter = () => { this.hovered = true; };
    this.onLeave = () => { this.hovered = false; };
    this.onPoke = () => this.poke();
    addEventListener('pointermove', this.onPointerMove, { passive: true });
    this.addEventListener('pointerenter', this.onEnter);
    this.addEventListener('pointerleave', this.onLeave);
    this.addEventListener('pointerdown', this.onPoke);
    if (!this.hasAttribute('state')) this.state = 'idle';
    queueMicrotask(() => {
      if (!this.isConnected || this.initializing || this.ready) return;
      const defaultPoster = new URL('./sol-idle-poster.png', import.meta.url).href;
      this.poster.src = this.getAttribute('poster') || defaultPoster;
      this.initialize();
    });
  }

  disconnectedCallback() {
    removeEventListener('pointermove', this.onPointerMove);
    this.removeEventListener('pointerenter', this.onEnter);
    this.removeEventListener('pointerleave', this.onLeave);
    this.removeEventListener('pointerdown', this.onPoke);
    this.pause();
    this.resizeObserver?.disconnect();
    this.intersectionObserver?.disconnect();
    this.renderer?.dispose();
    this.environmentTarget?.dispose();
    this.model = null;
    this.ready = false;
  }

  attributeChangedCallback(name, oldValue, newValue) {
    if (name === 'state' && oldValue !== newValue) {
      if (!STATES.has(newValue)) {
        this.setAttribute('state', 'idle');
        return;
      }
      this.stateSince = this.elapsed;
      this.updateLabel();
      if (this.model) {
        this.sample(0);
        this.render();
      }
      this.dispatchEvent(new CustomEvent('statechange', { detail: { state: newValue } }));
    }
  }

  get state() { return this.getAttribute('state') || 'idle'; }
  set state(value) {
    if (!STATES.has(value)) throw new Error(`Unknown Soléa state: ${value}`);
    this.setAttribute('state', value);
  }

  get modelUrl() {
    return this.getAttribute('model') || new URL('./sol-nueva-living.glb', import.meta.url).href;
  }

  updateLabel() {
    this.setAttribute('aria-label', `Soléa, AI-avatar i läget ${this.state}`);
  }

  async initialize() {
    if (this.initializing) return;
    this.initializing = true;
    try {
      this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'low-power' });
      this.renderer.setPixelRatio(Math.min(devicePixelRatio, 1.75));
      this.renderer.setClearColor(0xf4ead9, 0);
      this.renderer.outputColorSpace = THREE.SRGBColorSpace;
      this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
      this.renderer.toneMappingExposure = 0.94;
      this.mount.appendChild(this.renderer.domElement);

      this.scene = new THREE.Scene();
      this.camera = new THREE.OrthographicCamera(-2.5, 2.5, 2.5, -2.5, 0.1, 40);
      this.camera.position.set(0, 0.08, 8);
      this.camera.lookAt(0, 0, 0);

      const pmrem = new THREE.PMREMGenerator(this.renderer);
      const room = new RoomEnvironment();
      this.environmentTarget = pmrem.fromScene(room, 0.035);
      this.scene.environment = this.environmentTarget.texture;
      this.scene.environmentIntensity = 0.82;
      room.dispose();
      pmrem.dispose();

      const key = new THREE.DirectionalLight(0xfff4df, 3.2);
      key.position.set(-3.5, 4.5, 6);
      this.scene.add(key);
      const fill = new THREE.DirectionalLight(0xdde8ef, 1.35);
      fill.position.set(4, 0.5, 4);
      this.scene.add(fill);
      const rim = new THREE.DirectionalLight(0xffe2ae, 1.1);
      rim.position.set(1, -3, -2);
      this.scene.add(rim);
      this.scene.add(new THREE.AmbientLight(0xf4ead9, 0.5));

      const source = await loadModel(this.modelUrl);
      if (!this.isConnected) return;
      this.model = source.clone(true);
      this.scene.add(this.model);
      this.rays = this.model.getObjectByName('Engraved_rays');
      this.sun = this.model.getObjectByName('Sun_medallion');
      this.smile = this.model.getObjectByName('Calm_smile');
      this.eyes = ['Eye_left', 'Eye_right'].map(name => this.model.getObjectByName(name));
      this.talkingMouth = new THREE.Mesh(new THREE.SphereGeometry(1, 20, 12), this.eyes[0].material);
      this.talkingMouth.name = 'Runtime_talking_mouth';
      this.talkingMouth.position.set(0, -0.29, 0.34);
      this.talkingMouth.scale.set(0.16, 0.08, 0.035);
      this.talkingMouth.visible = false;
      this.sun.add(this.talkingMouth);
      if (this.getAttribute('finish') !== 'kimi') this.applyBrandFinish();
      this.smileBase = this.getAttribute('finish') === 'kimi' ? 1 : 0.84;
      this.cheeks = ['Cheek_left', 'Cheek_right'].map(name => this.model.getObjectByName(name)).filter(Boolean);
      this.waves = ['Wave_1', 'Wave_2', 'Wave_3'].map(name => this.model.getObjectByName(name)).filter(Boolean);
      this.rest = {
        sun: { position: this.sun.position.clone(), rotation: this.sun.rotation.clone(), scale: this.sun.scale.clone() },
        eyes: this.eyes.map(eye => eye.position.clone()),
        cheeks: this.cheeks.map(cheek => cheek.scale.clone()),
        waves: this.waves.map(wave => wave.position.clone()),
        rays: this.rays.children.map(ray => ray.scale.clone()),
      };
      this.motion = { lookX: 0, lookY: 0, tilt: 0, spin: 0, smile: 1, bounce: 0 };
      this.stateSince = 0;
      this.pokedAt = -1e9;

      this.resizeObserver = new ResizeObserver(() => this.resize());
      this.resizeObserver.observe(this);
      this.intersectionObserver = new IntersectionObserver(entries => {
        this.visible = entries[0]?.isIntersecting ?? true;
        if (this.visible) this.play();
        else this.pause();
      }, { rootMargin: '80px' });
      this.intersectionObserver.observe(this);
      this.reducedMotion.addEventListener('change', () => {
        if (this.reducedMotion.matches) this.pause();
        else this.play();
      });

      this.ready = true;
      this.resize();
      this.sample(0);
      this.render();
      this.frame.classList.add('ready');
      this.updateLabel();
      this.play();
      this.dispatchEvent(new CustomEvent('ready', { detail: this.getStats() }));
    } catch (error) {
      this.ready = false;
      this.frame.classList.remove('ready');
      this.dispatchEvent(new CustomEvent('avatarerror', { detail: { message: String(error) } }));
    } finally {
      this.initializing = false;
    }
  }

  resize() {
    if (!this.renderer || !this.camera) return;
    const width = Math.max(1, this.clientWidth);
    const height = Math.max(1, this.clientHeight);
    const aspect = width / height;
    const viewHeight = aspect < 1 ? 4.95 / aspect : 4.95;
    this.camera.left = -viewHeight * aspect / 2;
    this.camera.right = viewHeight * aspect / 2;
    this.camera.top = viewHeight / 2;
    this.camera.bottom = -viewHeight / 2;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(width, height, false);
    this.render();
  }

  // Nueva Living's finish, applied over the model Kimi delivered (finish="kimi" keeps the original):
  // the brand gold (#a8834a) instead of a lighter yellow-beige, brushed rather than glossy, darker
  // espresso engraving, cheeks reduced to a hint of warmth and a sea of sand and pale gold instead
  // of blue-grey, so she sits beside the engraved logo rather than apart from it. The model's
  // materials are recognised by their original colour, which the GLB fixes.
  applyBrandFinish() {
    const srgb = hex => new THREE.Color(hex);
    // The clone shares its materials with the cached model, so each is copied before it changes.
    const copies = new Map();
    this.model.traverse(node => {
      if (!node.isMesh) return;
      if (copies.has(node.material)) { node.material = copies.get(node.material); return; }
      const original = node.material;
      const material = original.clone();
      copies.set(original, material);
      node.material = material;
      const { r, b } = material.color;
      const near = (value, target) => Math.abs(value - target) < 0.006;
      if (b > r) {                                // the three waves
        const sand = [[0.198, '#c4a56c'], [0.238, '#d6bf8f'], [0.159, '#b08f55']];
        const match = sand.find(([value]) => near(r, value));
        material.color = srgb(match ? match[1] : '#c4a56c');
        material.metalness = 0.35;
        material.roughness = 0.58;
      } else if (near(r, 0.485)) {                       // rays, edge, rim
        material.color = srgb('#8a6630');
        material.metalness = 0.86;
        material.roughness = 0.52;
      } else if (near(r, 0.571)) {                // the face
        material.color = srgb('#a07a40');
        material.metalness = 0.8;
        material.roughness = 0.48;
      } else if (near(r, 0.25)) {                 // engraved lines
        material.color = srgb('#4a3520');
        material.metalness = 0.5;
        material.roughness = 0.6;
      } else if (near(r, 0.68)) {                 // cheeks
        material.color = srgb('#c98f6f');
        material.opacity = 0.22;
      }
      material.needsUpdate = true;
    });
  }

  poke() {
    this.pokedAt = this.elapsed;
    if (!this.playing) this.play();
    this.dispatchEvent(new CustomEvent('poke'));
  }

  sample(time) {
    if (!this.model) return;
    const dt = Math.min(this.dt || 1 / FPS, 0.1);
    const ease = rate => 1 - Math.exp(-dt * rate);
    const state = this.state;
    const m = this.motion;
    const rest = this.rest;
    const t = time;
    const sinceState = t - (this.stateSince || 0);
    const pokeAge = t - this.pokedAt;
    const poked = pokeAge >= 0 && pokeAge < 1.4;
    const cheerful = state === 'happy' || this.hovered || poked;

    // Where she looks: the pointer while it moves, otherwise a slow wander; up and aside in thought.
    let lookX;
    let lookY;
    if (state === 'thinking') {
      lookX = 0.5 + 0.12 * Math.sin(t * 0.9);
      lookY = 0.65;
    } else if (performance.now() - this.pointer.at < 4000) {
      lookX = this.pointer.x;
      lookY = this.pointer.y;
    } else {
      lookX = 0.45 * Math.sin(t * 0.37) + 0.18 * Math.sin(t * 1.13);
      lookY = 0.22 * Math.sin(t * 0.53 + 1);
    }
    m.lookX += (lookX - m.lookX) * ease(5);
    m.lookY += (lookY - m.lookY) * ease(5);
    m.tilt += ((state === 'thinking' ? 0.16 : 0) - m.tilt) * ease(4);
    m.smile += ((cheerful ? 1.28 : 1) - m.smile) * ease(8);

    // Rays turn all the time, faster in thought, and spin up when poked.
    const raySpeed = { idle: 0.22, thinking: 1.1, happy: 0.6, talking: 0.35 }[state] ?? 0.22;
    m.spin += dt * (raySpeed + (poked ? 9 * Math.exp(-pokeAge * 2.6) : 0));
    this.rays.rotation.z = m.spin;
    const shimmer = { idle: 0.045, thinking: 0.09, happy: 0.11, talking: 0.06 }[state] ?? 0.05;
    this.rays.children.forEach((ray, i) => {
      ray.scale.copy(rest.rays[i]).multiplyScalar(1 + shimmer * Math.sin(t * 3.1 - i * 0.7));
    });
    this.rays.scale.setScalar(1 + (state === 'thinking' ? 0.035 * Math.sin(t * 4) : 0));

    // The body floats and breathes, sways, bounces when happy and jumps when poked.
    let lift = 0.065 * Math.sin(t * 1.7);
    if (state === 'happy') lift += 0.11 * Math.abs(Math.sin(t * 5.2)) * Math.exp(-Math.max(0, sinceState - 1.6));
    if (poked) lift += 0.3 * Math.max(0, Math.sin(Math.PI * Math.min(1, pokeAge / 0.55)));
    const nod = state === 'talking' ? 0.05 * Math.sin(t * 6.3) : 0;
    const twirl = poked ? Math.PI * 2 * (1 - Math.pow(1 - Math.min(1, pokeAge / 1.1), 3)) : 0;
    this.sun.position.set(rest.sun.position.x, rest.sun.position.y + lift, rest.sun.position.z);
    this.sun.rotation.set(
      rest.sun.rotation.x - m.lookY * 0.3 + nod,
      rest.sun.rotation.y + m.lookX * 0.42 + twirl,
      rest.sun.rotation.z + m.tilt + 0.045 * Math.sin(t * 0.8) - m.lookX * 0.05,
    );
    this.sun.scale.copy(rest.sun.scale).multiplyScalar(1 + 0.018 * Math.sin(t * 1.7 + 1.2));

    // Eyes follow the gaze and blink: every few seconds, now and then twice.
    const cycle = t % 3.7;
    const second = Math.floor(t / 3.7) % 3 === 2 ? Math.max(0, 1 - Math.abs(cycle - 0.34) / 0.08) : 0;
    const blink = Math.max(Math.max(0, 1 - Math.abs(cycle - 0.08) / 0.08), second);
    const open = state === 'thinking' ? 0.8 : cheerful ? 0.78 : 1;
    this.eyes.forEach((eye, i) => {
      eye.position.set(rest.eyes[i].x + m.lookX * 0.045, rest.eyes[i].y + m.lookY * 0.035, rest.eyes[i].z);
      eye.scale.y = 0.115 * open * (1 - 0.92 * blink);
    });
    this.cheeks.forEach((cheek, i) => cheek.scale.copy(rest.cheeks[i]).multiplyScalar(cheerful ? 1.22 : 1));

    // Mouth: the calm smile, wider when cheerful; a moving mouth while she talks.
    this.smile.visible = state !== 'talking';
    this.talkingMouth.visible = state === 'talking';
    const base = this.smileBase ?? 1;
    this.smile.scale.set(base * (m.smile + (cheerful ? 0.05 * Math.sin(t * 3) : 0)), base * (1 + (m.smile - 1) * 0.6), 1);
    if (state === 'talking') {
      const voice = 0.5 + 0.32 * Math.sin(t * 12.5) + 0.22 * Math.sin(t * 7.9 + 1.3) - 0.12 * Math.sin(t * 3.1);
      const openness = Math.max(0, Math.min(1, voice));
      const base = this.smileBase ?? 1;
      this.talkingMouth.scale.set(base * (0.15 + 0.03 * openness), base * (0.035 + 0.085 * openness), 0.035);
    }

    // The sea rolls under her.
    this.waves.forEach((wave, i) => {
      wave.position.set(
        rest.waves[i].x + 0.07 * Math.sin(t * 1.25 + i * 1.15),
        rest.waves[i].y + 0.022 * Math.sin(t * 1.7 + i * 0.9),
        rest.waves[i].z,
      );
    });
  }

  render() {
    if (this.renderer && this.scene && this.camera) this.renderer.render(this.scene, this.camera);
  }

  tick = now => {
    if (!this.playing) return;
    this.raf = requestAnimationFrame(this.tick);
    if (now - this.lastFrame < 1000 / FPS) return;
    const delta = this.lastFrame ? Math.min((now - this.lastFrame) / 1000, 0.1) : 0;
    this.lastFrame = now;
    this.elapsed += delta;
    this.dt = delta;
    this.sample(this.elapsed);
    this.render();
  };

  play() {
    if (!this.ready || this.playing || this.reducedMotion.matches || !this.visible) return;
    this.playing = true;
    this.lastFrame = 0;
    this.raf = requestAnimationFrame(this.tick);
  }

  pause() {
    this.playing = false;
    cancelAnimationFrame(this.raf);
  }

  getStats() {
    return {
      state: this.state,
      ready: this.ready,
      playing: this.playing,
      fpsTarget: this.reducedMotion.matches ? 0 : FPS,
      drawCalls: this.renderer?.info.render.calls || 0,
      triangles: this.renderer?.info.render.triangles || 0,
      canvas: this.renderer ? [this.renderer.domElement.width, this.renderer.domElement.height] : [0, 0]
    };
  }
}

if (!customElements.get('sol-avatar')) customElements.define('sol-avatar', SolAvatar);
export { SolAvatar };
