// Animación declarativa: cada elemento dice en el HTML cuándo entra y cuándo sale, atado a la voz.
//   data-in="frase"            entra al empezar la frase
//   data-in="frase@palabra"    entra al decir esa palabra (empieza por); «@palabra#2» = 2.ª aparición
//   data-in="frase@palabra+.3" con desfase en segundos (también «-.2»)
//   data-in="12.5"             segundos absolutos
//   data-out=…                 lo mismo para salir (si falta, se queda hasta que acaba la escena)
//   data-a="up|left|right|scale|fade"   cómo entra (por defecto, up)
//   data-on=…                  añade la clase «on» a partir de ese instante
import {ini, fin, pal, pop, ease} from './engine.mjs';

export function cuando(spec) {
  if (spec == null || spec === '') return null;
  if (/^-?[\d.]+$/.test(spec)) return +spec;
  const m = spec.match(/^([\w-]+)(?:@([^#+\-]+)(?:#(\d+))?)?(?::fin)?([+-][\d.]+)?$/);
  if (!m) throw new Error('Tiempo mal escrito: ' + spec);
  const [, id, w, n, off] = m;
  let t = w ? pal(id, w, n ? +n - 1 : 0) : (spec.includes(':fin') ? fin(id) : ini(id));
  return t + (off ? +off : 0);
}

const DESDE = {up: {y: 40}, left: {x: -80, y: 0}, right: {x: 80, y: 0}, scale: {y: 0, s0: .6, damp: .6}, fade: {y: 0, s0: 1}, down: {y: -40}};

export function preparar(raiz) {
  const els = [...raiz.querySelectorAll('[data-in]')].map(el => ({
    el, t: cuando(el.dataset.in), out: cuando(el.dataset.out), a: DESDE[el.dataset.a || 'up'],
  }));
  const ons = [...raiz.querySelectorAll('[data-on]')].map(el => ({el, t: cuando(el.dataset.on)}));
  return t => {
    for (const e of els) {
      if (t < e.t - .05) { e.el.style.opacity = 0; continue; }
      pop(e.el, t, e.t, {...e.a, out: e.out, oy: -20});
    }
    for (const o of ons) o.el.classList.toggle('on', t >= o.t);
  };
}
