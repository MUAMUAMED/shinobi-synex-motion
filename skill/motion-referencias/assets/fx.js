// Ajudantes do video. Tempos em segundos do video inteiro; S = inicio da cena.
(function () {
  const FX = { W: 1920, H: 1080 };
  FX.rng = (s) => () => {
    s |= 0; s = (s + 0x6d2b79f5) | 0;
    let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };

  // keys: [[tempo, {props}, ease?], ...]
  FX.k = (tl, sel, S, keys) => {
    let state = Object.assign({}, keys[0][1]);
    gsap.set(sel, state);
    for (let i = 1; i < keys.length; i++) {
      const t0 = keys[i - 1][0];
      const [t1, p, ease] = keys[i];
      const to = Object.assign({}, state, p);
      tl.fromTo(sel, Object.assign({}, state), Object.assign({}, to, {
        duration: Math.max(t1 - t0, 0.001), ease: ease || "none", immediateRender: false,
      }), t0 - S);
      state = to;
    }
  };

  // Palavra desliza e foca
  FX.w = (tl, sel, S, t, dur) => {
    gsap.set(sel, { opacity: 0 });
    tl.fromTo(sel, { opacity: 0, x: 30, y: 16, filter: "blur(7px)" },
      { opacity: 1, x: 0, y: 0, filter: "blur(0px)", duration: dur || 0.26, ease: "power2.out", immediateRender: false }, t - S);
  };

  // Entra so com foco e opacidade, sem mexer na posicao
  FX.fi = (tl, sel, S, t, dur) => {
    gsap.set(sel, { opacity: 0 });
    tl.fromTo(sel, { opacity: 0, filter: "blur(7px)" }, { opacity: 1, filter: "blur(0px)", duration: dur || 0.22, ease: "power2.out", immediateRender: false }, t - S);
  };

  // Impacto: entra enorme e desfocado, assenta rapido
  FX.hit = (tl, sel, S, t, o) => {
    o = Object.assign({ from: 2.3, dur: 0.3, blur: 22 }, o || {});
    gsap.set(sel, { opacity: 0 });
    tl.fromTo(sel, { opacity: 0, scale: o.from, filter: `blur(${o.blur}px)` },
      { opacity: 1, scale: 1, filter: "blur(0px)", duration: o.dur, ease: "expo.out", immediateRender: false }, t - S);
  };

  // Implosao de saida
  FX.out = (tl, sel, S, t, dur) => {
    tl.to(sel, { scale: 0.05, opacity: 0, duration: dur || 0.2, ease: "power3.in", immediateRender: false }, t - S);
  };

  FX.fade = (tl, sel, S, t, dur) => { tl.to(sel, { opacity: 0, duration: dur || 0.15, immediateRender: false }, t - S); };

  // Pulo curto de "carimbo"
  FX.stamp = (tl, sel, S, t) => {
    gsap.set(sel, { opacity: 0 });
    tl.fromTo(sel, { opacity: 0, scale: 1.4 }, { opacity: 1, scale: 1, duration: 0.14, ease: "back.out(2.4)", immediateRender: false }, t - S);
  };

  // Anel que nasce e abre
  FX.ring = (tl, sel, S, t, dur) => {
    gsap.set(sel, { opacity: 0 });
    tl.fromTo(sel, { opacity: 1, scale: 0.25 }, { opacity: 0, scale: 1.5, duration: dur || 0.7, ease: "power2.out", immediateRender: false }, t - S);
  };

  // Boca da narradora segue as palavras. segs: [[prefixoDoId, de, ate], ...]
  FX.talk = (tl, S, segs) => {
    segs.forEach(([id, from, to]) => {
      const f = "#" + id + "f", a = "#" + id + "a";
      gsap.set([f, a], { opacity: 0 });
      tl.set(f, { opacity: 1 }, Math.max(from - S, 0.001));
      (window.WORDS || []).forEach((w) => {
        if (w.e <= from || w.s >= to) return;
        for (let t = Math.max(w.s, from); t < Math.min(w.e, to); t += 0.13) {
          tl.set(a, { opacity: 1 }, t - S); tl.set(f, { opacity: 0 }, t - S);
          const c = Math.min(t + 0.08, to - 0.001);
          tl.set(a, { opacity: 0 }, c - S); tl.set(f, { opacity: 1 }, c - S);
        }
      });
      tl.set(f, { opacity: 0 }, to - S); tl.set(a, { opacity: 0 }, to - S);
    });
  };

  // Balanco suave enquanto fala
  FX.sway = (tl, sel, S, t0, t1, amp) => {
    const n = Math.max(1, Math.floor((t1 - t0) / 0.7));
    gsap.set(sel, { transformOrigin: "50% 100%" });
    for (let i = 0; i < n; i++) {
      tl.fromTo(sel, { rotation: i % 2 ? (amp || 1.6) : -(amp || 1.6) },
        { rotation: i % 2 ? -(amp || 1.6) : (amp || 1.6), duration: (t1 - t0) / n, ease: "sine.inOut", immediateRender: false }, t0 - S + i * (t1 - t0) / n);
    }
  };

  // Troca de quadros: mostra um id por vez
  FX.swap = (tl, ids, S, t0, step) => {
    ids.forEach((id, i) => {
      gsap.set(id, { opacity: 0 });
      tl.set(id, { opacity: 1 }, Math.max(t0 + i * step - S, 0.001));
      if (i < ids.length - 1) tl.set(id, { opacity: 0 }, t0 + (i + 1) * step - S);
    });
  };

  FX.drive = (tl, S, t0, t1, fn) => {
    const o = { t: t0 };
    tl.fromTo(o, { t: t0 }, { t: t1, duration: t1 - t0, ease: "none", immediateRender: false, onUpdate: () => fn(o.t) }, t0 - S);
    fn(t0);
  };

  FX.dust = (cv, o) => {
    const g = cv.getContext("2d"), r = FX.rng(o.seed || 7), P = [], W = cv.width, H = cv.height;
    for (let i = 0; i < (o.n || 70); i++) P.push({ x: r() * W, y: r() * H, a: r() * 3.14, l: 8 + r() * 26,
      vx: (r() - 0.5) * 70, vy: (r() - 0.6) * 60, al: 0.2 + r() * 0.6, w: 1.5 + r() * 2.5 });
    return (t) => {
      g.clearRect(0, 0, W, H);
      g.strokeStyle = o.color || "#fff"; g.lineCap = "round";
      P.forEach((p) => {
        const x = ((p.x + p.vx * t) % W + W) % W, y = ((p.y + p.vy * t) % H + H) % H;
        g.globalAlpha = p.al * (o.alpha || 1); g.lineWidth = p.w;
        g.beginPath(); g.moveTo(x - Math.cos(p.a) * p.l, y - Math.sin(p.a) * p.l); g.lineTo(x + Math.cos(p.a) * p.l, y + Math.sin(p.a) * p.l); g.stroke();
      });
      g.globalAlpha = 1;
    };
  };

  FX.confetti = (cv, o) => {
    const g = cv.getContext("2d"), r = FX.rng(o.seed || 1), P = [];
    for (let i = 0; i < (o.n || 170); i++) {
      const a = r() * 6.283, v = 500 + Math.sqrt(r()) * 3200;
      P.push({ vx: Math.cos(a) * v, vy: Math.sin(a) * v, c: o.colors[Math.floor(r() * o.colors.length)], l: 9 + r() * 18, w: 5 + r() * 6,
        rot: r() * 6.28, sp: (r() - 0.5) * 7, cur: (r() - 0.5) * 22, fall: 50 + r() * 90, ph: r() * 6.28 });
    }
    return (t) => {
      g.clearRect(0, 0, cv.width, cv.height);
      const T = t - o.t0;
      if (T < 0) return;
      const K = 3.4;
      P.forEach((p) => {
        const e = (1 - Math.exp(-K * T)) / K;
        const x = o.x + p.vx * e + Math.sin(T * 2 + p.ph) * 18, y = o.y + p.vy * e + p.fall * T;
        g.save(); g.translate(x, y); g.rotate(p.rot + p.sp * T);
        g.strokeStyle = p.c; g.lineWidth = p.w; g.globalAlpha = 0.95;
        g.beginPath(); g.moveTo(-p.l, 0); g.quadraticCurveTo(0, p.cur, p.l, 0); g.stroke();
        g.restore();
      });
    };
  };

  // Raios: [{t, d, pts, c, w}] com t e d em segundos
  FX.bolts = (cv, bolts, seed) => {
    const g = cv.getContext("2d"), r = FX.rng(seed || 3);
    bolts.forEach((b) => {
      const out = [b.pts[0]];
      for (let i = 1; i < b.pts.length; i++) {
        const A = b.pts[i - 1], B = b.pts[i];
        for (let k = 1; k <= 4; k++) out.push([A[0] + (B[0] - A[0]) * k / 4 + (k === 4 ? 0 : (r() - 0.5) * 40), A[1] + (B[1] - A[1]) * k / 4 + (k === 4 ? 0 : (r() - 0.5) * 40)]);
      }
      b.path = out;
    });
    return (t) => {
      g.clearRect(0, 0, cv.width, cv.height);
      bolts.forEach((b) => {
        const d = b.d || 0.1;
        if (t < b.t || t >= b.t + d) return;
        g.save(); g.globalAlpha = 0.5 + 0.5 * (1 - (t - b.t) / d); g.strokeStyle = b.c; g.lineWidth = b.w || 6;
        g.lineJoin = "round"; g.lineCap = "round"; g.shadowColor = b.c; g.shadowBlur = 36;
        g.beginPath(); b.path.forEach((p, i) => (i ? g.lineTo(p[0], p[1]) : g.moveTo(p[0], p[1]))); g.stroke();
        g.shadowBlur = 0; g.strokeStyle = "#fff"; g.globalAlpha *= 0.55; g.lineWidth = (b.w || 6) * 0.35; g.stroke();
        g.restore();
      });
    };
  };
  // Keyframes em frames do Voltz, remapeados para o tempo da narracao e para 16:9.
  // m: {f0, t0, r} = tempo t0 no frame f0, r segundos por frame; dx, dy deslocam o quadro vertical.
  FX.pk = (tl, sel, S, m, keys) => {
    const dx = m.dx === undefined ? 420 : m.dx, dy = m.dy === undefined ? -420 : m.dy;
    let px = null, py = null;
    FX.k(tl, sel, S, keys.map(([f, p, e]) => {
      const q = Object.assign({}, p);
      if (typeof q.x === "number") q.x += dx;
      if (typeof q.y === "number") q.y += dy;
      return [m.t0 + (f - m.f0) * m.r, q, e];
    }));
  };
  // Mapa de tempo para a narracao nova: toda animacao continua descrita no tempo base.
  FX.T = (t) => {
    const M = window.TMAP;
    if (!M) return t;
    for (let i = 1; i < M.length; i++) if (t <= M[i][0]) return M[i - 1][1] + (t - M[i - 1][0]) * (M[i][1] - M[i - 1][1]) / (M[i][0] - M[i - 1][0]);
    return t + M[M.length - 1][1] - M[M.length - 1][0];
  };
  FX.tl = (S) => {
    const tl = gsap.timeline({ paused: true }), to = tl.to.bind(tl), ft = tl.fromTo.bind(tl), st = tl.set.bind(tl), B = FX.T(S);
    const m = (v, p) => { const a = FX.T(S + p), b = FX.T(S + p + (v.duration || 0)); return [Object.assign({}, v, { duration: Math.max(b - a, 0.001) }), a - B]; };
    tl.to = (t, v, p) => { const [w, q] = m(v, p); return to(t, w, q); };
    tl.fromTo = (t, f, v, p) => { const [w, q] = m(v, p); return ft(t, f, w, q); };
    tl.set = (t, v, p) => st(t, v, FX.T(S + p) - B);
    return tl;
  };
  FX.starSvg = (c) => `<svg viewBox="-100 -100 200 200" width="100%" height="100%" style="overflow:visible"><defs><radialGradient id="sg${c.slice(1)}"><stop offset="0" stop-color="#fff"/><stop offset=".25" stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="${c}" stop-opacity="0"/></radialGradient></defs><circle r="92" fill="url(#sg${c.slice(1)})"/><path d="M0-100 2.5-4 100 0 2.5 4 0 100-2.5 4-100 0-2.5-4Z" fill="#fff"/></svg>`;
  // Confete que sobe de um ponto, freia e cai
  FX.jato = (cv, o) => {
    const g = cv.getContext("2d"), r = FX.rng(o.seed || 1), P = [];
    for (let i = 0; i < (o.n || 200); i++) {
      const a = -Math.PI / 2 + (r() - 0.5) * (o.spread || 1.6), v = 700 + Math.sqrt(r()) * (o.speed || 3000) * 2.2;
      P.push({ vx: Math.cos(a) * v, vy: Math.sin(a) * v, c: o.colors[Math.floor(r() * o.colors.length)], l: 9 + r() * 18, w: 5 + r() * 6,
        rot: r() * 6.28, sp: (r() - 0.5) * 7, cur: (r() - 0.5) * 22, fall: 50 + r() * 90, dx: (r() - 0.5) * 80, ph: r() * 6.28 });
    }
    return (t) => {
      g.clearRect(0, 0, cv.width, cv.height);
      const T = t - o.t0;
      if (T < 0) return;
      const K = 3.4;
      P.forEach((p) => {
        const e = (1 - Math.exp(-K * T)) / K;
        const x = o.x + p.vx * e + p.dx * T + Math.sin(T * 2 + p.ph) * 18, y = o.y + p.vy * e + p.fall * T;
        const L = p.l + Math.hypot(p.vx, p.vy) * Math.exp(-K * T) * 0.005;
        g.save(); g.translate(x, y); g.rotate(p.rot + p.sp * T);
        g.strokeStyle = p.c; g.lineWidth = p.w; g.globalAlpha = 0.95;
        g.beginPath(); g.moveTo(-L, 0); g.quadraticCurveTo(0, p.cur, L, 0); g.stroke();
        g.restore();
      });
    };
  };
  // Iris: a camada nasce de um circulo dentro da cena e cobre a tela
  FX.iris = (tl, sel, S, t, dur, cx, cy) => {
    const c = (r) => `circle(${r}% at ${cx || 50}% ${cy || 50}%)`;
    gsap.set(sel, { clipPath: c(0) });
    tl.fromTo(sel, { clipPath: c(0) }, { clipPath: c(120), duration: dur || 0.22, ease: "power2.in", immediateRender: false }, t - S);
  };
  // Cursor: chega, clica e sai. O elemento clicado reage em tClique.
  FX.clique = (tl, sel, S, de, ate, sai, tChega, tClique, tSai) => {
    FX.k(tl, sel, S, [[tChega - 0.3, { x: de[0], y: de[1], scale: 1 }], [tChega, { x: ate[0], y: ate[1] }, "power2.out"], [tClique - 0.01, { scale: 1 }], [tClique + 0.03, { scale: 0.82 }], [tClique + 0.1, { scale: 1 }], [tSai, { x: ate[0], y: ate[1] }], [tSai + 0.25, { x: sai[0], y: sai[1] }, "power2.in"]]);
  };
  window.FX = FX;
})();
