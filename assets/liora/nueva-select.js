/* Nueva Living: the open list of a <select>, drawn by the site.
 *
 * Safari and Chrome on a Mac open a <select> as a system menu (grey panel,
 * blue highlight, system font) that no CSS reaches. On a device with a fine
 * pointer this script opens its own list instead. The real <select> stays
 * in the page and stays the source of truth: the list is rebuilt from its
 * options every time it opens, and a choice is written back to it with the
 * same input and change events the browser would fire, so the hero search,
 * the Developments filters, the forms and the URL state read it unchanged.
 *
 * Touch devices keep the native picker, which is the better control there.
 * A <select multiple> or one with a size, and anything inside
 * [data-native-select], is left alone.
 */
(function () {
  'use strict';

  if (typeof window === 'undefined' || !window.matchMedia) return;
  if (!window.matchMedia('(hover: hover) and (pointer: fine)').matches) return;

  var list = null;
  var current = null;   // the <select> whose list is open
  var items = [];       // [{ el, index }] for every enabled option row
  var active = -1;      // position in items
  var typed = '';
  var typedAt = 0;
  var uid = 0;

  function eligible(select) {
    return select &&
      select.tagName === 'SELECT' &&
      !select.multiple &&
      !(select.size > 1) &&
      !select.disabled &&
      !select.closest('[data-native-select]');
  }

  function ensureList() {
    if (list) return list;
    list = document.createElement('ul');
    list.className = 'nv-select-list';
    list.id = 'nv-select-list';
    list.setAttribute('role', 'listbox');
    list.hidden = true;
    // mousedown, not click: keep focus on the <select> while choosing.
    list.addEventListener('mousedown', function (event) {
      event.preventDefault();
      var row = event.target.closest('.nv-select-option');
      if (!row || row.getAttribute('aria-disabled') === 'true') return;
      choose(Number(row.dataset.index));
    });
    list.addEventListener('mousemove', function (event) {
      var row = event.target.closest('.nv-select-option');
      if (!row || row.getAttribute('aria-disabled') === 'true') return;
      for (var i = 0; i < items.length; i += 1) {
        if (items[i].el === row) { setActive(i, false); return; }
      }
    });
    document.body.appendChild(list);
    return list;
  }

  function build(select) {
    var ul = ensureList();
    ul.textContent = '';
    items = [];
    var cs = window.getComputedStyle(select);
    ul.style.fontFamily = cs.fontFamily;
    ul.setAttribute('dir', cs.direction);
    var lang = select.closest('[lang]');
    if (lang) ul.setAttribute('lang', lang.getAttribute('lang'));

    Array.prototype.forEach.call(select.children, function (child) {
      if (child.tagName === 'OPTGROUP') {
        var head = document.createElement('li');
        head.className = 'nv-select-group';
        head.setAttribute('role', 'presentation');
        head.textContent = child.label;
        ul.appendChild(head);
        Array.prototype.forEach.call(child.children, function (opt) { addOption(ul, opt, child.disabled); });
      } else if (child.tagName === 'OPTION') {
        addOption(ul, child, false);
      }
    });
  }

  function addOption(ul, opt, groupDisabled) {
    if (opt.hidden) return;
    var li = document.createElement('li');
    uid += 1;
    li.id = 'nv-select-option-' + uid;
    li.className = 'nv-select-option';
    li.setAttribute('role', 'option');
    li.dataset.index = String(opt.index);
    li.textContent = opt.textContent.trim();
    var selected = opt.selected;
    li.setAttribute('aria-selected', selected ? 'true' : 'false');
    if (opt.disabled || groupDisabled) {
      li.setAttribute('aria-disabled', 'true');
    } else {
      items.push({ el: li, index: opt.index });
    }
    ul.appendChild(li);
  }

  function place() {
    if (!current || !list) return;
    var rect = current.getBoundingClientRect();
    if (rect.width === 0 && rect.height === 0) { close(false); return; }
    var vw = document.documentElement.clientWidth;
    var vh = window.innerHeight;
    list.style.minWidth = Math.round(rect.width) + 'px';
    list.style.maxWidth = Math.max(200, vw - 24) + 'px';
    list.style.maxHeight = '';
    var below = vh - rect.bottom - 12;
    var above = rect.top - 12;
    var natural = Math.min(list.scrollHeight, 320);
    var up = natural > below && above > below;
    var room = Math.max(120, up ? above : below);
    if (natural > room) list.style.maxHeight = room + 'px';
    var height = Math.min(natural, room);
    list.style.top = Math.round(up ? rect.top - height - 4 : rect.bottom + 4) + 'px';
    var width = list.offsetWidth;
    var rtl = list.getAttribute('dir') === 'rtl';
    var left = rtl ? rect.right - width : rect.left;
    left = Math.min(Math.max(12, left), vw - width - 12);
    list.style.left = Math.round(left) + 'px';
  }

  function open(select) {
    if (current === select) return;
    if (current) close(false);
    current = select;
    build(select);
    list.hidden = false;
    place();
    select.setAttribute('aria-expanded', 'true');
    select.setAttribute('aria-controls', list.id);
    var start = 0;
    for (var i = 0; i < items.length; i += 1) {
      if (items[i].index === select.selectedIndex) { start = i; break; }
    }
    setActive(start, true);
    window.addEventListener('scroll', place, true);
    window.addEventListener('resize', place);
  }

  function close(refocus) {
    if (!current) return;
    var select = current;
    current = null;
    active = -1;
    if (list) list.hidden = true;
    select.setAttribute('aria-expanded', 'false');
    select.removeAttribute('aria-activedescendant');
    window.removeEventListener('scroll', place, true);
    window.removeEventListener('resize', place);
    if (refocus) select.focus({ preventScroll: true });
  }

  function setActive(position, scroll) {
    if (!items.length) return;
    position = Math.max(0, Math.min(items.length - 1, position));
    if (active >= 0 && items[active]) items[active].el.classList.remove('is-active');
    active = position;
    var el = items[active].el;
    el.classList.add('is-active');
    if (current) current.setAttribute('aria-activedescendant', el.id);
    if (scroll) {
      var top = el.offsetTop;
      var bottom = top + el.offsetHeight;
      if (top < list.scrollTop) list.scrollTop = top - 6;
      else if (bottom > list.scrollTop + list.clientHeight) list.scrollTop = bottom - list.clientHeight + 6;
    }
  }

  function choose(index) {
    var select = current;
    if (!select) return;
    var changed = select.selectedIndex !== index;
    select.selectedIndex = index;
    close(true);
    if (changed) {
      select.dispatchEvent(new Event('input', { bubbles: true }));
      select.dispatchEvent(new Event('change', { bubbles: true }));
    }
  }

  // Type-ahead, as the native list has: letters within 700 ms build a prefix.
  function typeAhead(key) {
    var now = Date.now();
    typed = now - typedAt > 700 ? key : typed + key;
    typedAt = now;
    var needle = typed.toLocaleLowerCase();
    var startAt = typed.length === 1 ? active + 1 : active;
    for (var n = 0; n < items.length; n += 1) {
      var i = (Math.max(0, startAt) + n) % items.length;
      if (items[i].el.textContent.toLocaleLowerCase().indexOf(needle) === 0) {
        setActive(i, true);
        return true;
      }
    }
    return false;
  }

  // The <select> a press is meant for: the select itself, or the label
  // wrapped around it. The hero search fields are labels the width of their
  // cell, so a press on the caption ("Price"), the chevron or the padding
  // went to the label, which the browser forwards to the select as its own
  // click -- and that opened the system menu this script exists to replace.
  function targetSelect(target) {
    if (!target || !target.closest) return null;
    var select = target.closest('select');
    if (select) return select;
    if (target.closest('a, button, input, textarea, [contenteditable]')) return null;
    var label = target.closest('label');
    var control = label && label.control;
    return control && control.tagName === 'SELECT' ? control : null;
  }

  // The label's own activation comes on click, after the mousedown above has
  // already opened the list; stop it, or it reaches the select as well.
  document.addEventListener('click', function (event) {
    var select = targetSelect(event.target);
    if (select && select !== event.target && eligible(select)) event.preventDefault();
  }, true);

  document.addEventListener('mousedown', function (event) {
    var select = targetSelect(event.target);
    if (select && eligible(select)) {
      if (event.button !== 0) return;
      event.preventDefault();
      if (current === select) { close(true); return; }
      select.focus({ preventScroll: true });
      open(select);
      return;
    }
    if (current && list && !list.contains(event.target)) close(false);
  }, true);

  document.addEventListener('keydown', function (event) {
    var select = event.target;
    if (!eligible(select)) return;
    var key = event.key;
    if (current !== select) {
      // Enter is left alone: in a form it submits, as it does natively.
      if (key === 'ArrowDown' || key === 'ArrowUp' || key === ' ') {
        event.preventDefault();
        open(select);
      }
      return;
    }
    switch (key) {
      case 'ArrowDown': event.preventDefault(); setActive(active + 1, true); break;
      case 'ArrowUp': event.preventDefault(); setActive(active - 1, true); break;
      case 'Home': case 'PageUp': event.preventDefault(); setActive(0, true); break;
      case 'End': case 'PageDown': event.preventDefault(); setActive(items.length - 1, true); break;
      case 'Enter': case ' ':
        event.preventDefault();
        if (items[active]) choose(items[active].index);
        break;
      case 'Escape': event.preventDefault(); close(true); break;
      case 'Tab': close(false); break;
      default:
        if (key.length === 1 && !event.metaKey && !event.ctrlKey && !event.altKey) {
          event.preventDefault();
          typeAhead(key);
        }
    }
  }, true);

  document.addEventListener('focusout', function (event) {
    if (current && event.target === current) {
      window.setTimeout(function () {
        if (current && document.activeElement !== current) close(false);
      }, 0);
    }
  });
})();
