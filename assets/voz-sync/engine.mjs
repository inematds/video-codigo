// Motor de tiempo para vídeos con voz: todo es función del tiempo, seek(t) pinta el instante t
// sin depender de en qué orden se pidan los fotogramas. Los tiempos salen de la voz (window.TIEMPOS).
import {spring, track, clamp, mix} from './motion.mjs';
export {spring, track, clamp, mix};

export const T = window.TIEMPOS;

// ── Tiempos de la voz ──
export function fr(id) {
  const f = T.frases.find(x => x.id === id);
  if (!f) throw new Error('Não existe a frase ' + id + ' no roteiro');
  return f;
}
export const ini = id => fr(id).inicio;
export const fin = id => fr(id).fin;
const norm = s => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9/]/g, '');
// Instante en que se dice la palabra `w` (empieza por) dentro de la frase `id`; `n` = qué aparición.
export function pal(id, w, n = 0) {
  const m = T.palabras.filter(p => p.frase === id && norm(p.texto).startsWith(norm(w)));
  if (!m[n]) throw new Error(`Não encontrei «${w}» na frase ${id} do roteiro`);
  return m[n].inicio;
}
export const palFin = (id, w, n = 0) => {
  const m = T.palabras.filter(p => p.frase === id && norm(p.texto).startsWith(norm(w)));
  if (!m[n]) throw new Error(`Não encontrei «${w}» na frase ${id} do roteiro`);
  return m[n].fin;
};
export const bloque = id => T.bloques.find(b => b.id === id);

// ── Curvas ──
export const ease = (t, t0, d = .5) => { const x = clamp((t - t0) / d); return 1 - Math.pow(1 - x, 3); };
export const easeIO = (t, t0, d = .6) => { const x = clamp((t - t0) / d); return x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };
export const sp = (t, t0, o = {frequency: 2.1, damping: .78}) => (t <= t0 ? 0 : spring(t - t0, o));
// Presencia de 0 a 1: entra en t0, sale en t1.
export const win = (t, t0, t1, din = .35, dout = .3) => Math.min(ease(t, t0, din), 1 - ease(t, t1, dout));

export function set(el, {o = 1, x = 0, y = 0, s = 1, r = 0, blur = 0} = {}) {
  el.style.opacity = o;
  el.style.transform = `translate(${x}px,${y}px) scale(${s}) rotate(${r}deg)`;
  el.style.filter = blur > .05 ? `blur(${blur}px)` : 'none';
}
// Entrada con muelle y salida opcional.
export function pop(el, t, t0, {y = 34, x = 0, s0 = .9, out = null, dout = .3, oy = -20, freq = 2.1, damp = .78} = {}) {
  const p = sp(t, t0, {frequency: freq, damping: damp});
  const a = ease(t, t0, .22);
  let o = a, yy = (1 - p) * y, xx = (1 - p) * x, s = mix(s0, 1, p);
  if (out != null) { const q = ease(t, out, dout); o *= 1 - q; yy += q * oy; }
  set(el, {o, x: xx, y: yy, s});
  return o;
}
export const count = (t, t0, t1, a, b) => Math.round(mix(a, b, easeIO(t, t0, Math.max(.01, t1 - t0))));

// ── Escribir texto ──
const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
// Revela el texto del elemento de izquierda a derecha sin mover el layout (el resto queda invisible).
export function type(el, t, t0, cps = 60) {
  if (el.__full == null) el.__full = el.textContent;
  const full = el.__full, n = Math.max(0, Math.min(full.length, Math.floor((t - t0) * cps)));
  const key = n;
  if (el.__n === key) return n >= full.length;
  el.__n = key;
  el.innerHTML = esc(full.slice(0, n)) + '<span style="opacity:0">' + esc(full.slice(n)) + '</span>';
  return n >= full.length;
}

// ── Escenas ──
export class Film {
  constructor() { this.scenes = []; this.always = []; }
  add(el, start, end, render) { this.scenes.push({el, start, end, render}); return this; }
  every(fn) { this.always.push(fn); return this; }
  seek(t) {
    for (const s of this.scenes) {
      const on = t >= s.start && t < s.end;
      if (s.el.__on !== on) { s.el.style.display = on ? 'block' : 'none'; s.el.__on = on; }
      if (on) s.render(t, t - s.start);
    }
    for (const fn of this.always) fn(t);
  }
}

// ── Chat de Claude ──
// items: [{el, t}] dentro de `col`. Dentro de cada item, los elementos con data-t (segundos absolutos)
// aparecen a su hora. Los .tw se escriben letra a letra. El chat baja solo para enseñar lo último.
export function chat(view, col, items, {cps = 70, margen = 30} = {}) {
  const subs = [...col.querySelectorAll('[data-t]')].map(el => ({el, t: +el.dataset.t}));
  const todos = [...items, ...subs];
  const veo = (t, completo) => {
    for (const it of todos) {
      const v = t >= it.t;
      it.el.style.display = v ? '' : 'none';
      if (completo && it.el.classList.contains('tw') && it.el.__full != null) it.el.textContent = it.el.__full;
    }
  };
  let keys = null;
  function medir() {
    for (const it of todos) {
      if (it.el.classList.contains('tw') && it.el.__full == null) it.el.__full = it.el.textContent;
      it.el.style.transform = 'none';
    }
    const tiempos = [...new Set(todos.map(i => i.t))].sort((a, b) => a - b);
    keys = [[-10, 0]];
    for (const e of tiempos) {
      veo(e + .001, true);
      const target = Math.max(0, col.offsetHeight - view.clientHeight + margen);
      if (e > keys[keys.length - 1][0]) keys.push([e, target]);
    }
    for (const it of todos) if (it.el.__full != null) it.el.__n = null;
  }
  function render(t) {
    if (!keys) medir();
    veo(t, false);
    for (const it of todos) {
      if (t < it.t) continue;
      pop(it.el, t, it.t, {y: 22, s0: .97, freq: 2.6, damp: .9});
      if (it.el.classList.contains('tw')) type(it.el, t, it.t, cps);
    }
    const y = track(t, keys, {frequency: 1.6, damping: 1});
    col.style.transform = `translateY(${-Math.max(0, y)}px)`;
  }
  return {render, medir};
}

// Botón que se pulsa: escala y anillo violeta.
export function tap(el, t, t0) {
  const x = clamp((t - t0) / .5);
  const s = x <= 0 || x >= 1 ? 1 : 1 - .12 * Math.sin(Math.PI * x);
  const ring = x <= 0 || x >= 1 ? 0 : Math.sin(Math.PI * x);
  el.style.transform = `scale(${s})`;
  el.style.boxShadow = ring ? `0 0 0 ${10 * ring}px rgba(109,40,217,${.28 * ring})` : 'none';
}
// Barra que se llena.
export function fill(el, t, t0, d = 1.4) { el.style.transform = `scaleX(${easeIO(t, t0, d)})`; }

// ── Subtítulos palabra a palabra ──
export function subtitulos(box, {max = 4, clase = ''} = {}) {
  if (clase) box.className = clase;
  const trozos = [];
  for (const f of T.frases) {
    const ws = T.palabras.filter(p => p.frase === f.id);
    let cur = [];
    ws.forEach((w, i) => {
      cur.push(w);
      const corte = /[.,:;?!]$/.test(w.texto) && cur.length >= 2;
      if (cur.length >= max || corte || i === ws.length - 1) { trozos.push(cur); cur = []; }
    });
  }
  // Cada trozo se ve desde su primera palabra hasta que empieza el siguiente (o 0,35 s tras su última palabra).
  trozos.forEach((c, i) => {
    c.ini = c[0].inicio - .05;
    const sig = trozos[i + 1];
    c.fin = Math.min(sig ? sig[0].inicio - .05 : Infinity, c[c.length - 1].fin + .35);
  });
  let actual = null;
  return t => {
    const c = trozos.find(x => t >= x.ini && t < x.fin);
    if (c !== actual) {
      actual = c;
      box.innerHTML = c ? '<div class="line">' + c.map(w => `<span class="w">${esc(w.texto.replace(/[.,:;]$/, ''))}</span>`).join('') + '</div>' : '';
    }
    if (!c) return;
    const spans = box.querySelectorAll('.w');
    c.forEach((w, i) => {
      spans[i].classList.toggle('dicha', t >= w.inicio);
      spans[i].classList.toggle('ahora', t >= w.inicio && t < (c[i + 1] ? c[i + 1].inicio : w.fin + .3));
    });
    const line = box.firstChild, a = ease(t, c.ini, .12);
    line.style.opacity = a;
    line.style.transform = `translateY(${(1 - a) * 10}px)`;
  };
}

// ── Arranque común ──
export function arrancar(film, {fps = 30, cola = 1.2} = {}) {
  window.videoSpec = {width: 1920, height: 1080, fps, duration: Math.ceil((T.duracion + cola) * fps) / fps};
  window.seek = t => film.seek(t);
  // Un recorrido completo antes del primer fotograma: así cada escena ya se ha pintado una vez y el primer
  // instante queda igual que cuando se vuelve a él tras un salto (la comprobación de determinismo del render).
  window.renderReady = document.fonts.ready.then(async () => {
    for (let t = 0; t < window.videoSpec.duration; t += 2) film.seek(t);
    film.seek(0);
    await document.fonts.ready;
  });
}
