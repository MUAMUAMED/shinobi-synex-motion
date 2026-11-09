// Biblioteca de movimento do filme. Todos os tempos são globais (segundos do vídeo); S = início da cena.
(function () {
  const L = {};

  L.rng = (s) => () => {
    s |= 0; s = (s + 0x6d2b79f5) | 0;
    let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };

  // Quadros-chave: [[tempo, {props}, ease?], ...]. O primeiro vira o estado inicial.
  L.k = (tl, sel, S, keys) => {
    let st = Object.assign({}, keys[0][1]);
    gsap.set(sel, st);
    for (let i = 1; i < keys.length; i++) {
      const t0 = keys[i - 1][0];
      const [t1, p, ease] = keys[i];
      const to = Object.assign({}, st, p);
      tl.fromTo(sel, Object.assign({}, st), Object.assign({}, to, { duration: Math.max(t1 - t0, 0.001), ease: ease || "none", immediateRender: false }), t0 - S);
      st = to;
    }
  };

  // Liga e desliga em instantes exatos
  L.mostra = (tl, sel, S, de, ate) => {
    gsap.set(sel, { opacity: 0 });
    tl.set(sel, { opacity: 1 }, Math.max(de - S, 0.001));
    if (ate !== undefined) tl.set(sel, { opacity: 0 }, ate - S);
  };

  // Palavra entra só com foco (sem deslizar): 0,13 s
  L.palavra = (tl, sel, S, t, d) => {
    gsap.set(sel, { opacity: 0 });
    tl.fromTo(sel, { opacity: 0, filter: "blur(7px)" }, { opacity: 1, filter: "blur(0px)", duration: d || 0.14, ease: "power2.out", immediateRender: false }, t - S);
  };
  // Palavra entra do cinza para a cor final
  L.acende = (tl, sel, S, t, cor) => {
    tl.fromTo(sel, { color: "#5a5866" }, { color: cor, duration: 0.12, immediateRender: false }, t - S);
  };
  // Saída limpa: foco e opacidade
  L.sai = (tl, sel, S, t, d) => {
    tl.to(sel, { opacity: 0, filter: "blur(8px)", duration: d || 0.16, ease: "power2.in", immediateRender: false }, t - S);
  };
  // Impacto: chega grande e desfocado, assenta com cauda longa
  L.impacto = (tl, sel, S, t, o) => {
    o = Object.assign({ de: 1.9, d: 0.38, blur: 22 }, o || {});
    gsap.set(sel, { opacity: 0 });
    tl.fromTo(sel, { opacity: 0, scale: o.de, filter: `blur(${o.blur}px)` }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: o.d, ease: "expo.out", immediateRender: false }, t - S);
  };
  // Implosão: encolhe acelerando até um ponto
  L.implode = (tl, sel, S, t, d, extra) => {
    tl.to(sel, Object.assign({ scale: 0.02, opacity: 0, duration: d || 0.22, ease: "power3.in", immediateRender: false }, extra || {}), t - S);
  };
  // Anel que abre e some
  L.anel = (tl, sel, S, t, d, ate) => {
    gsap.set(sel, { opacity: 0 });
    tl.fromTo(sel, { opacity: 1, scale: 0.2 }, { opacity: 0, scale: ate || 1.6, duration: d || 0.6, ease: "power2.out", immediateRender: false }, t - S);
  };
  // Carimbo: bate e assenta
  L.carimbo = (tl, sel, S, t, rot) => {
    gsap.set(sel, { opacity: 0 });
    tl.fromTo(sel, { opacity: 0, scale: 1.6, rotation: (rot || 0) - 8 }, { opacity: 1, scale: 1, rotation: rot || 0, duration: 0.16, ease: "back.out(2.2)", immediateRender: false }, t - S);
  };
  // Íris: a camada nasce de um círculo e cobre a tela
  L.iris = (tl, sel, S, t, d, cx, cy, abre) => {
    const c = (r) => `circle(${r}% at ${cx}% ${cy}%)`;
    const [a, b] = abre === false ? [130, 0] : [0, 130];
    gsap.set(sel, { clipPath: c(a) });
    tl.fromTo(sel, { clipPath: c(a) }, { clipPath: c(b), duration: d, ease: abre === false ? "power3.in" : "power2.in", immediateRender: false }, t - S);
  };
  // Movimento de recorte, 12 quadros por segundo
  L.passos = (d) => `steps(${Math.max(1, Math.round(d * 12))})`;

  // Cursor: chega, clica, sai
  L.cursor = (tl, sel, S, de, ate, sai, tChega, tClique, tSai) => {
    L.k(tl, sel, S, [[tChega - 0.32, { x: de[0], y: de[1], scale: 1, opacity: 1 }], [tChega, { x: ate[0], y: ate[1] }, "power3.out"], [tClique - 0.02, { scale: 1 }], [tClique + 0.03, { scale: 0.8 }], [tClique + 0.11, { scale: 1 }], [tSai, { x: ate[0], y: ate[1] }], [tSai + 0.26, { x: sai[0], y: sai[1] }, "power3.in"]]);
  };

  // Separa o texto em letras (montagem síncrona)
  L.letras = (el) => {
    const t = el.textContent;
    el.textContent = "";
    [...t].forEach((c) => { const s = document.createElement("span"); s.textContent = c === " " ? " " : c; s.style.display = "inline-block"; el.appendChild(s); });
    return [...el.children];
  };
  // Digitação: letras aparecem uma a uma, com o cursor de texto acompanhando
  L.digita = (tl, el, S, t, porLetra) => {
    const ls = L.letras(el);
    ls.forEach((s, i) => { gsap.set(s, { opacity: 0 }); tl.set(s, { opacity: 1 }, t - S + i * (porLetra || 0.035)); });
    return ls;
  };

  L.drive = (tl, S, t0, t1, fn) => {
    const o = { t: t0 };
    tl.fromTo(o, { t: t0 }, { t: t1, duration: t1 - t0, ease: "none", immediateRender: false, onUpdate: () => fn(o.t) }, t0 - S);
    fn(t0);
  };

  // Confete em fitinhas: estoura de um ponto e cai
  L.confete = (cv, o) => {
    const g = cv.getContext("2d"), r = L.rng(o.seed || 1), P = [];
    for (let i = 0; i < (o.n || 160); i++) {
      const a = (o.ang === undefined ? -Math.PI / 2 : o.ang) + (r() - 0.5) * (o.abre || 6.3), v = 600 + Math.sqrt(r()) * (o.vel || 2400);
      P.push({ vx: Math.cos(a) * v, vy: Math.sin(a) * v, c: o.cores[Math.floor(r() * o.cores.length)], l: 8 + r() * 16, w: 5 + r() * 5, rot: r() * 6.28, sp: (r() - 0.5) * 8, cur: (r() - 0.5) * 20, cai: 60 + r() * 90, ph: r() * 6.28 });
    }
    return (t) => {
      g.clearRect(0, 0, cv.width, cv.height);
      const T = t - o.t0;
      if (T <= 0 || T > (o.vida || 3)) return;
      const K = 3.2, fade = Math.min(1, ((o.vida || 3) - T) / 0.6);
      P.forEach((p) => {
        const e = (1 - Math.exp(-K * T)) / K;
        const x = o.x + p.vx * e + Math.sin(T * 2 + p.ph) * 16, y = o.y + p.vy * e + p.cai * T * T;
        g.save(); g.translate(x, y); g.rotate(p.rot + p.sp * T);
        g.globalAlpha = fade; g.strokeStyle = p.c; g.lineWidth = p.w;
        g.beginPath(); g.moveTo(-p.l, 0); g.quadraticCurveTo(0, p.cur, p.l, 0); g.stroke(); g.restore();
      });
    };
  };

  // Poeira de luz lenta
  L.poeira = (cv, o) => {
    const g = cv.getContext("2d"), r = L.rng(o.seed || 7), P = [], W = cv.width, H = cv.height;
    for (let i = 0; i < (o.n || 60); i++) P.push({ x: r() * W, y: r() * H, s: 1 + r() * 2.6, vx: (r() - 0.5) * 30, vy: -10 - r() * 40, a: 0.2 + r() * 0.6 });
    return (t) => {
      g.clearRect(0, 0, W, H);
      g.fillStyle = o.cor || "#fff";
      P.forEach((p) => {
        g.globalAlpha = p.a * (o.alpha || 1);
        g.beginPath(); g.arc(((p.x + p.vx * t) % W + W) % W, ((p.y + p.vy * t) % H + H) % H, p.s, 0, 6.283); g.fill();
      });
      g.globalAlpha = 1;
    };
  };

  // Ícones do game-icons.net: <svg data-ic="nome"> recebe o desenho, na cor do texto
  L.icones = (raiz) => {
    (raiz || document).querySelectorAll("svg[data-ic]").forEach((s) => {
      const p = (window.ICONES || {})[s.getAttribute("data-ic")] || [];
      s.setAttribute("viewBox", "0 0 512 512");
      s.innerHTML = p.map((d) => `<path fill="currentColor" d="${d}"/>`).join("");
    });
  };

  // ---- Tipografia em batida (referência snapinsta) ----
  // Cada quadro é uma tela cheia com fundo próprio: entra por corte seco no tempo da palavra,
  // o texto (.bt) chega 14% maior e desfocado e assenta em 4 quadros, e a camada .dr deriva
  // até o próximo quadro, para a tela nunca ficar parada.
  // quadros: [{ sel, t, deriva?: {scale, x, y, rotation}, de? }]
  L.batida = (tl, S, quadros, fim) => {
    quadros.forEach((q, i) => {
      const ate = i < quadros.length - 1 ? quadros[i + 1].t : fim;
      L.mostra(tl, q.sel, S, q.t, ate);
      const bt = q.sel + " > .dr > .bt", dr = q.sel + " > .dr";
      if (document.querySelector(bt)) tl.fromTo(bt, { scale: q.de || 1.14, filter: "blur(8px)" }, { scale: 1, filter: "blur(0px)", duration: 0.13, ease: "expo.out", immediateRender: false }, q.t - S);
      const dv = Object.assign({ scale: 1.06, x: 0, y: 0, rotation: 0 }, q.deriva || {});
      tl.fromTo(dr, { scale: 1, x: 0, y: 0, rotation: 0 }, Object.assign({}, dv, { duration: Math.max(ate - q.t, 0.05), ease: "none", immediateRender: false }), q.t - S);
    });
  };
  // Palavra que estala dentro de um quadro já visível
  L.pop = (tl, sel, S, t, de) => {
    gsap.set(sel, { opacity: 0 });
    tl.fromTo(sel, { opacity: 1, scale: de || 1.3, filter: "blur(6px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.12, ease: "expo.out", immediateRender: false }, t - S);
  };
  // Movimento contínuo e lento entre t0 e t1 (nada fica estacionado)
  L.vivo = (tl, sel, S, t0, t1, de, ate) => {
    tl.fromTo(sel, Object.assign({}, de), Object.assign({}, ate, { duration: Math.max(t1 - t0, 0.05), ease: "none", immediateRender: false }), t0 - S);
  };
  // Ecos: cópias em contorno que crescem e somem atrás de uma palavra
  L.ecos = (tl, sels, S, t, d) => {
    sels.forEach((s, i) => {
      gsap.set(s, { opacity: 0 });
      tl.fromTo(s, { opacity: 0.55, scale: 1 }, { opacity: 0, scale: 1.55, duration: d || 0.5, ease: "power2.out", immediateRender: false }, t + i * 0.08 - S);
    });
  };
  // Tremida curta de câmera (impacto)
  L.treme = (tl, sel, S, t, forca, quadros) => {
    const f = 1 / 30, r = L.rng(Math.round(t * 1000));
    for (let i = 0; i < (quadros || 5); i++) {
      const k = (forca || 14) * (1 - i / (quadros || 5));
      tl.set(sel, { x: (r() - 0.5) * 2 * k, y: (r() - 0.5) * 2 * k }, t + i * f - S);
    }
    tl.set(sel, { x: 0, y: 0 }, t + (quadros || 5) * f - S);
  };

  window.L = L;
})();
