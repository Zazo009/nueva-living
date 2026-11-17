# Soléa's 3D avatar

Source of `assets/liora/solea/sol-avatar.js`, the `<sol-avatar>` web component the chat uses
(`assets/liora/nueva-solea.js`). The model (`sol-nueva-living.glb`), the posters and the first
version of this component came from the Kimi handoff of 16 November 2026; the motion and the
interaction (follows the pointer, smiles on hover, jumps and spins its rays when poked, blinks,
floats, rolling sea) were rewritten here on 17 November 2026.

Rebuild after editing `src/sol-avatar.js`:

```
cd tools/solea && npm ci && npx vite build --config vite.avatar.config.js
cp dist-component/sol-avatar.js ../../assets/liora/solea/sol-avatar.js && rm -rf dist-component
```

The bundle includes Three.js, so it is about 1 MB (210 KB compressed). The site loads it only
after the page has finished loading, and build_dist versions its URL by its hash.
