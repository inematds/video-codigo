// Motor do molde b-roll: lê window.PLANO (scripts/broll-plano.py) e monta, para cada instante t, a pessoa (tela
// inteira, meia tela ou círculo no canto) e o visual da frase (traço do conceito, número, comparação, passos).
// Contrato do render-video.mjs: window.videoSpec, window.seek(t) (assíncrono: espera o quadro decodificar), window.renderReady.
// Tudo é função de t — sem relógio, sem animação CSS — então qualquer instante sai igual, em qualquer ordem.

const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const ease = (t, t0, d) => { const x = clamp((t - t0) / d); return x * x * (3 - 2 * x); };
const out3 = (t, t0, d) => 1 - Math.pow(1 - clamp((t - t0) / d), 3);
const mix = (a, b, k) => a + (b - a) * k;
const win = (t, a, b, fi = .3, fo = .3) => Math.min(ease(t, a, fi), 1 - ease(t, b - fo, fo));
const circ = (cx, cy, r) => `M${cx - r} ${cy}a${r} ${r} 0 1 0 ${2 * r} 0a${r} ${r} 0 1 0 ${-2 * r} 0`;
const engr = () => { const d = []; for (let i = 0; i < 8; i++) { const a = i * Math.PI / 4, c = Math.cos(a), s = Math.sin(a); d.push(`M${50 + 26 * c} ${50 + 26 * s}L${50 + 38 * c} ${50 + 38 * s}`); } return [circ(50, 50, 26), circ(50, 50, 10), ...d]; };

// Ícones em traço (viewBox 0 0 100 100). O último caminho sai em amarelo. Ícone novo: acrescente aqui e no ICONE do broll-plano.py.
export const ICONES = {
  lampada: ['M50 12C32 12 22 26 22 40C22 52 30 58 34 66L34 74L66 74L66 66C70 58 78 52 78 40C78 26 68 12 50 12Z', 'M38 82L62 82', 'M42 90L58 90', 'M42 48L50 58L58 48'],
  engrenagem: engr(),
  relogio: [circ(50, 50, 36), 'M50 50L50 26', 'M50 50L66 60'],
  alvo: [circ(50, 50, 36), circ(50, 50, 22), circ(50, 50, 8), 'M52 48L84 16M72 16L84 16L84 28'],
  lupa: [circ(42, 42, 26), 'M61 61L86 86'],
  balao: ['M18 20H82A8 8 0 0 1 90 28V60A8 8 0 0 1 82 68H44L28 82V68H18A8 8 0 0 1 10 60V28A8 8 0 0 1 18 20Z', 'M26 36H74', 'M26 50H58'],
  lista: ['M14 18H30V34H14Z', 'M14 44H30V60H14Z', 'M14 70H30V86H14Z', 'M40 26H86M40 52H86M40 78H72', 'M17 26L21 31L28 21M17 52L21 57L28 47'],
  alerta: ['M50 12L90 84H10Z', 'M50 38V60', 'M50 70V73'],
  chip: ['M28 28H72V72H28Z', 'M40 40H60V60H40Z', 'M38 28V16M50 28V16M62 28V16M38 72V84M50 72V84M62 72V84M28 38H16M28 50H16M28 62H16M72 38H84M72 50H84M72 62H84'],
  codigo: ['M34 28L14 50L34 72', 'M66 28L86 50L66 72', 'M58 20L42 80'],
  cifrao: ['M66 30C62 20 38 18 34 32C30 46 68 48 66 66C64 80 38 82 32 70', 'M50 10V90'],
  semente: ['M22 88H78', 'M50 88V46', 'M50 62C30 62 20 46 22 34C40 34 50 46 50 62Z', 'M50 52C52 34 64 24 80 26C80 40 68 52 50 52Z'],
  raio: ['M58 8L24 56H48L40 92L76 40H52Z'],
  pessoa: [circ(50, 30, 15), 'M20 90C20 62 34 52 50 52C66 52 80 62 80 90'],
  livro: ['M50 26C40 20 26 20 12 24V80C26 76 40 76 50 82C60 76 74 76 88 80V24C74 20 60 20 50 26Z', 'M50 26V82'],
  foguete: ['M50 8C66 22 70 44 64 68H36C30 44 34 22 50 8Z', circ(50, 38, 7), 'M36 54L22 74L36 70M64 54L78 74L64 70', 'M44 74L50 92L56 74'],
  grafico: ['M14 14V86H88', 'M24 72L40 56L54 62L82 28', 'M70 28H82V40'],
  nuvem: ['M30 72C14 72 12 52 28 50C28 32 50 28 56 42C62 32 82 36 78 54C90 56 88 72 74 72Z'],
  ferramenta: ['M64 16C52 12 40 22 43 36L16 63C11 68 11 75 16 80C21 85 28 85 33 80L60 53C74 56 84 44 80 32L68 42L58 38L56 28Z'],
  seta: ['M12 50H82', 'M62 30L84 50L62 70'],
};

function svgIcone(nome, lado) {
  const ps = ICONES[nome] || ICONES.lampada;
  const ns = 'http://www.w3.org/2000/svg', s = document.createElementNS(ns, 'svg');
  s.setAttribute('viewBox', '0 0 100 100'); s.setAttribute('class', 'ic');
  Object.assign(s.style, {width: lado + 'px', height: lado + 'px', strokeWidth: 3.4});
  const paths = ps.map((d, i) => { const p = document.createElementNS(ns, 'path'); p.setAttribute('d', d); p.setAttribute('pathLength', '1');
    p.style.strokeDasharray = '1 1'; if (i === ps.length - 1 && ps.length > 1) p.classList.add('acc'); s.appendChild(p); return p; });
  return {el: s, desenha: k => paths.forEach((p, i) => { const n = paths.length, a = i / n * .7; p.style.strokeDashoffset = 1 - clamp((k - a) / (1 - a + .0001) * 1.0); })};
}

const el = (tag, cls, txt, pai) => { const e = document.createElement(tag); if (cls) e.className = cls; if (txt != null) e.textContent = txt; pai.appendChild(e); return e; };
const fmt = (v, u) => { const s = Number.isInteger(v) ? String(v) : v.toFixed(1).replace('.', ','); return s + (u === '%' ? '%' : u === 'x' ? '×' : u ? ' ' + u : ''); };

// Cada visual: (caixa, v, G) → função (t) que pinta. G = geometria do quadro.
const VISUAIS = {
  traco(box, v, G) {
    const lado = G.H * .42, ic = svgIcone(v.icone, lado);
    const area = G.vertical ? {x: G.W * .1, y: G.H * .12, w: G.W * .8} : {x: G.W * .07, y: G.H * .2, w: G.W * .6};
    Object.assign(ic.el.style, G.vertical ? {left: (G.W - lado * .9) / 2 + 'px', top: G.H * .14 + 'px', width: lado * .9 + 'px', height: lado * .9 + 'px'}
      : {left: area.x + 'px', top: (G.H - lado) / 2 - G.H * .04 + 'px'});
    box.appendChild(ic.el);
    const tt = el('div', 'titulo', v.titulo || '', box); el('i', '', null, tt);
    const fs = G.vertical ? G.W * .1 : G.H * .1;
    Object.assign(tt.style, G.vertical ? {left: G.W * .08 + 'px', right: G.W * .08 + 'px', top: G.H * .52 + 'px', fontSize: fs + 'px', textAlign: 'center'}
      : {left: area.x + lado + G.H * .06 + 'px', width: G.W * .62 - lado - G.H * .06 + 'px', top: G.H * .42 + 'px', fontSize: fs + 'px'});
    const sub = tt.querySelector('i');
    return t => {
      ic.desenha(ease(t, v.ancora, 1.1));
      const e = v.entra ?? v.ancora + .1;   // o título entra com a frase; o desenho se completa na palavra
      tt.style.opacity = ease(t, e, .3); tt.style.transform = `translateY(${(1 - out3(t, e, .45)) * 30}px)`;
      sub.style.transform = `scaleX(${out3(t, Math.max(e, v.ancora) + .25, .6)})`;
    };
  },
  numero(box, v, G) {
    const n = el('div', 'num', '', box), r = el('div', 'rot', v.rotulo || '', box), ic = svgIcone(v.icone, G.H * .16);
    box.appendChild(ic.el);
    const fs = (G.vertical ? G.W * .36 : G.H * .36);
    Object.assign(n.style, {left: 0, right: 0, textAlign: 'center', top: (G.vertical ? G.H * .3 : G.H * .2) + 'px', fontSize: fs + 'px'});
    Object.assign(r.style, {left: 0, right: 0, textAlign: 'center', top: (G.vertical ? G.H * .3 : G.H * .2) + fs * 1.12 + 'px', fontSize: fs * .16 + 'px'});
    Object.assign(ic.el.style, {left: (G.W - G.H * .16) / 2 + 'px', top: (G.vertical ? G.H * .18 : G.H * .04) + 'px'});
    return t => {   // a contagem TERMINA na palavra do número (sincronia com a fala), começa 0,8 s antes
      const k = out3(t, v.ancora - .8, .8), x = v.numero * k;
      n.textContent = fmt(Number.isInteger(v.numero) ? Math.round(x) : Math.round(x * 10) / 10, v.unidade);
      n.style.opacity = ease(t, v.ancora - .9, .25);
      r.style.opacity = ease(t, v.ancora + .05, .3);
      ic.desenha(ease(t, v.ancora - .9, 1));
    };
  },
  comparacao(box, v, G) {
    const max = Math.max(...v.itens.map(i => i.valor)) || 1, larg = G.W * (G.vertical ? .72 : .62), x0 = G.vertical ? G.W * .14 : G.W * .19;
    const tt = el('div', 'titulo', v.titulo || '', box);
    Object.assign(tt.style, {left: x0 + 'px', top: G.H * .14 + 'px', fontSize: (G.vertical ? G.W * .07 : G.H * .075) + 'px'});
    const linhas = v.itens.map((it, i) => {
      const y = G.H * (G.vertical ? .36 + i * .2 : .38 + i * .24), h = G.H * (G.vertical ? .08 : .13);
      const b = el('div', 'barra' + (i ? ' b2' : ''), null, box), val = el('div', 'val', fmt(it.valor, it.unidade), box), rot = el('div', 'rot', it.rotulo || '', box);
      Object.assign(b.style, {left: x0 + 'px', top: y + 'px', height: h + 'px', width: larg * it.valor / max + 'px'});
      Object.assign(val.style, {left: x0 + larg * it.valor / max + G.H * .03 + 'px', top: y + h * .12 + 'px', fontSize: h * .7 + 'px'});
      Object.assign(rot.style, {left: x0 + 'px', top: y - G.H * .055 + 'px', fontSize: G.H * .035 + 'px', color: '#9a9aa6'});
      return {b, val, rot, it};
    });
    return t => {
      tt.style.opacity = ease(t, v.ancora - .6, .3);
      for (const {b, val, rot, it} of linhas) {   // estrutura entra antes; o valor assenta NA palavra
        rot.style.opacity = ease(t, it.t - .5, .25);
        b.style.transform = `scaleX(${out3(t, it.t - .6, .6)})`;
        val.style.opacity = ease(t, it.t - .05, .2);
      }
    };
  },
  passos(box, v, G) {
    const tt = el('div', 'titulo', v.titulo || '', box), n = v.itens.length;
    const x0 = G.vertical ? G.W * .08 : G.W * .12, w = G.vertical ? G.W * .84 : G.W * .62;
    Object.assign(tt.style, {left: x0 + 'px', top: G.H * (G.vertical ? .14 : .1) + 'px', width: w + 'px', fontSize: (G.vertical ? G.W * .075 : G.H * .08) + 'px'});
    const alto = Math.min(G.H * .15, G.H * .62 / n - G.H * .025);
    const cards = v.itens.map((it, i) => {
      const c = el('div', 'passo', null, box), b = el('b', '', String(i + 1), c); el('span', '', it.texto, c);
      Object.assign(c.style, {left: x0 + 'px', width: w + 'px', top: G.H * (G.vertical ? .3 : .28) + i * (alto + G.H * .025) + 'px', height: alto + 'px',
        fontSize: alto * .3 + 'px', gap: alto * .25 + 'px', padding: `0 ${alto * .3}px`});
      Object.assign(b.style, {width: alto * .62 + 'px', height: alto * .62 + 'px', fontSize: alto * .34 + 'px'});
      return {c, it};
    });
    return t => {
      tt.style.opacity = ease(t, v.ancora - .5, .3);
      for (const {c, it} of cards) { const k = out3(t, it.t - .2, .45); c.style.opacity = k; c.style.transform = `translateX(${(1 - k) * -50}px)`; }
    };
  },
};

export function iniciar(P) {
  const W = P.video.largura, H = P.video.altura, fps = P.video.fps, dur = P.video.duracao, nq = P.video.n_quadros || Math.floor(dur * fps);
  const vertical = H > W, G = {W, H, vertical};
  const R = P.rosto, img = document.getElementById('q'), pessoa = document.getElementById('pessoa'), anel = document.getElementById('anel');
  img.style.width = W + 'px'; img.style.height = H + 'px';

  // trechos: cada frase vale até a próxima começar; "segue" estica o gráfico anterior
  const frs = P.frases.filter(f => f.tratamento !== 'segue');
  // um visual que ainda está sendo lido (fim_visual) empurra o começo da frase seguinte
  const ini = frs.map((f, i) => i ? Math.max(f.inicio, frs[i - 1].fim_visual || 0) - .15 : 0);
  const trechos = frs.map((f, i) => ({...f, a: ini[i], b: i + 1 < frs.length ? ini[i + 1] : dur + 5}));
  const vis = document.getElementById('vis');
  for (const tr of trechos) {
    if (tr.tratamento === 'rosto' || !VISUAIS[tr.visual.tipo]) continue;
    const box = el('div', 'vis' + (tr.tratamento === 'cheio' ? ' cheio' : ''), null, vis);
    box.dataset.frase = tr.id;
    tr.box = box; tr.pinta = VISUAIS[tr.visual.tipo](box, tr.visual, G);
  }

  // onde a pessoa fica em cada tratamento: caixa {x, y, w, h, raio} + escala/posição do quadro dentro dela
  const D = Math.min(W, H) * .36, m = Math.min(W, H) * .05;
  const cheia = {x: 0, y: 0, w: W, h: H, raio: 0, s: 1, ox: 0, oy: 0, o: 1};
  const meia = vertical ? {x: 0, y: H / 2, w: W, h: H / 2, raio: 0} : {x: W / 2, y: 0, w: W / 2, h: H, raio: 0};
  if (R.tamanho === 'meia') { const s = Math.max(meia.w / W, meia.h / H); // centrado no rosto, sem deixar borda vazia
    Object.assign(meia, {s, ox: clamp(meia.x + meia.w / 2 - R.cx * W * s, meia.x + meia.w - W * s, meia.x), oy: clamp(meia.y + meia.h / 2 - R.cy * H * s, meia.y + meia.h - H * s, meia.y), o: 1}); }
  const circulo = (() => { const x = W - m - D, y = H - m - D, s = D / (2 * R.r * H); return {x, y, w: D, h: D, raio: D / 2, s, ox: x + D / 2 - R.cx * W * s, oy: y + D / 2 - R.cy * H * s, o: 1}; })();
  // meia tela: a outra metade mostra a palavra-chave da frase dita
  if (R.tamanho === 'meia') for (const tr of trechos) if (tr.tratamento === 'rosto' && tr.visual.titulo) {
    const box = el('div', 'vis', null, vis), tt = el('div', 'titulo', tr.visual.titulo, box); el('i', '', null, tt);
    Object.assign(tt.style, vertical ? {left: W * .08 + 'px', right: W * .08 + 'px', top: H * .2 + 'px', fontSize: W * .1 + 'px', textAlign: 'center'}
      : {left: W * .06 + 'px', width: W * .38 + 'px', top: H * .42 + 'px', fontSize: H * .09 + 'px'});
    const sub = tt.querySelector('i'), e = tr.visual.entra ?? tr.inicio;
    tr.box = box; tr.pinta = t => { tt.style.opacity = ease(t, e, .3); sub.style.transform = `scaleX(${out3(t, e + .2, .6)})`; };
  }
  const estado = tr => tr.tratamento === 'rosto' ? (R.tamanho === 'meia' ? meia : cheia) : tr.tratamento === 'cheio' ? {...circulo, o: 0} : circulo;
  const lerp = (A, B, k) => Object.fromEntries(Object.keys(A).map(key => [key, mix(A[key], B[key] ?? A[key], k)]));

  window.videoSpec = {width: W, height: H, fps, duration: Math.floor(dur * fps) / fps};
  window.CORTES = trechos.slice(1).filter((tr, i) => tr.tratamento !== trechos[i].tratamento || tr.tratamento !== 'rosto').map(tr => +tr.a.toFixed(3));
  let atual = 0;
  const quadro = async t => {
    const i = Math.min(nq, Math.max(1, Math.floor(t * fps + 1e-6) + 1));
    if (i === atual) return;
    atual = i; img.src = `quadros/${String(i).padStart(5, '0')}.jpg`;
    await img.decode();
  };
  window.seek = async t => {
    await quadro(t);
    const k = trechos.findIndex(tr => t >= tr.a && t < tr.b), tr = trechos[Math.max(0, k)], ant = trechos[Math.max(0, k - 1)];
    const S = lerp(estado(ant), estado(tr), out3(t, tr.a, .45));
    Object.assign(pessoa.style, {left: S.x + 'px', top: S.y + 'px', width: S.w + 'px', height: S.h + 'px', borderRadius: S.raio + 'px', opacity: S.o});
    img.style.transform = `translate(${S.ox - S.x}px,${S.oy - S.y}px) scale(${S.s})`;
    const anelOn = tr.tratamento === 'pip' ? ease(t, tr.a + .25, .2) : 0;
    Object.assign(anel.style, {left: S.x + 'px', top: S.y + 'px', width: S.w + 'px', height: S.h + 'px', opacity: anelOn * S.o});
    for (const x of trechos) if (x.box) { const o = win(t, x.a, x.b + .15, .3, .3); x.box.style.opacity = o; x.box.style.display = o > 0 ? '' : 'none'; if (o > 0) x.pinta(t); }
  };
  window.renderReady = (async () => { await document.fonts.ready; await window.seek(0); })();
}
