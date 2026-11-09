// Ajudantes compartilhados. Tudo e funcao do tempo: nada de Math.random solto.
(function () {
  const FX = {};
  FX.c = (n) => n * 5.684; // celula da folha de frames (190px) -> canvas 1080
  FX.rng = (s) => () => {
    s |= 0; s = (s + 0x6d2b79f5) | 0;
    let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };

  // Keyframes por numero de frame do video original.
  // keys: [[frame, {props}, ease?], ...]
  FX.keys = (tl, sel, S, keys) => {
    let state = Object.assign({}, keys[0][1]);
    gsap.set(sel, state);
    for (let i = 1; i < keys.length; i++) {
      const [f0] = keys[i - 1];
      const [f1, p, ease] = keys[i];
      const to = Object.assign({}, state, p);
      tl.fromTo(sel, Object.assign({}, state), Object.assign({}, to, {
        duration: Math.max((f1 - f0) / 30, 0.001), ease: ease || "none", immediateRender: false,
      }), (f0 - S) / 30);
      state = to;
    }
  };

  // Palavra entra deslizando, desfocada, como no original
  FX.word = (tl, sel, S, f, dur) => {
    gsap.set(sel, { opacity: 0 });
    tl.fromTo(sel, { opacity: 0, x: 26, y: 14, filter: "blur(6px)" },
      { opacity: 1, x: 0, y: 0, filter: "blur(0px)", duration: (dur || 8) / 30, ease: "power2.out", immediateRender: false }, (f - S) / 30);
  };

  FX.drive = (tl, S, f0, f1, fn) => {
    const o = { t: f0 / 30 };
    tl.fromTo(o, { t: f0 / 30 }, { t: f1 / 30, duration: (f1 - f0) / 30, ease: "none", immediateRender: false,
      onUpdate: () => fn(o.t) }, (f0 - S) / 30);
    fn(f0 / 30);
  };

  // Confete em fitinhas: estoura de um ponto, freia e cai devagar
  FX.confetti = (cv, o) => {
    const g = cv.getContext("2d"), r = FX.rng(o.seed || 1), P = [];
    const cols = o.colors;
    for (let i = 0; i < (o.n || 160); i++) {
      const a = -Math.PI / 2 + (r() - 0.5) * (o.spread || 1.5), v = (o.vmin || 700) + Math.sqrt(r()) * (o.speed || 2600) * 2.3;
      P.push({ vx: Math.cos(a) * v, vy: Math.sin(a) * v, c: cols[Math.floor(r() * cols.length)],
        l: 9 + r() * 18, w: 5 + r() * 6, rot: r() * 6.28, sp: (r() - 0.5) * 7, cur: (r() - 0.5) * 22, fall: 50 + r() * 90,
        dx: (r() - 0.5) * 80, ph: r() * 6.28 });
    }
    return (t) => {
      g.clearRect(0, 0, cv.width, cv.height);
      const T = t - o.t0;
      if (T < 0) return;
      const K = 3.4;
      P.forEach((p) => {
        const e = (1 - Math.exp(-K * T)) / K;
        const x = o.x + p.vx * e + p.dx * T + Math.sin(T * 2 + p.ph) * 18;
        const y = o.y + p.vy * e + p.fall * T;
        const sp = Math.hypot(p.vx, p.vy) * Math.exp(-K * T);
        const L = p.l + sp * 0.005;
        g.save(); g.translate(x, y); g.rotate(p.rot + p.sp * T);
        g.strokeStyle = p.c; g.lineWidth = p.w; g.lineCap = "butt"; g.globalAlpha = o.alpha || 0.95;
        g.beginPath(); g.moveTo(-L, 0); g.quadraticCurveTo(0, p.cur, L, 0); g.stroke();
        g.restore();
      });
    };
  };

  // Poeira: riscos finos e lentos
  FX.dust = (cv, o) => {
    const g = cv.getContext("2d"), r = FX.rng(o.seed || 7), P = [];
    for (let i = 0; i < (o.n || 70); i++) P.push({ x: r() * 1080, y: r() * 1920, a: r() * 3.14, l: 8 + r() * 26,
      vx: (r() - 0.5) * 50, vy: (r() - 0.6) * 60, al: 0.2 + r() * 0.6, w: 1.5 + r() * 2.5 });
    return (t) => {
      g.clearRect(0, 0, cv.width, cv.height);
      g.strokeStyle = o.color || "#fff"; g.lineCap = "round";
      P.forEach((p) => {
        const x = ((p.x + p.vx * t) % 1080 + 1080) % 1080, y = ((p.y + p.vy * t) % 1920 + 1920) % 1920;
        g.globalAlpha = p.al * (o.alpha || 1); g.lineWidth = p.w;
        g.beginPath(); g.moveTo(x - Math.cos(p.a) * p.l, y - Math.sin(p.a) * p.l); g.lineTo(x + Math.cos(p.a) * p.l, y + Math.sin(p.a) * p.l); g.stroke();
      });
      g.globalAlpha = 1;
    };
  };

  // Raios: cada um existe em uma janela de frames. bolts: [{f,d,pts:[[x,y],..],c,w}]
  FX.bolts = (cv, bolts, seed) => {
    const g = cv.getContext("2d"), r = FX.rng(seed || 3);
    const jag = (pts) => {
      const out = [pts[0]];
      for (let i = 1; i < pts.length; i++) {
        const [a, b] = [pts[i - 1], pts[i]];
        for (let k = 1; k <= 4; k++) {
          const q = k / 4, m = k === 4 ? 0 : 34;
          out.push([a[0] + (b[0] - a[0]) * q + (r() - 0.5) * m, a[1] + (b[1] - a[1]) * q + (r() - 0.5) * m]);
        }
      }
      return out;
    };
    bolts.forEach((b) => (b.path = jag(b.pts)));
    return (t) => {
      g.clearRect(0, 0, cv.width, cv.height);
      const fr = t * 30;
      bolts.forEach((b) => {
        if (fr < b.f || fr >= b.f + (b.d || 2)) return;
        const fade = 1 - (fr - b.f) / (b.d || 2);
        g.save(); g.globalAlpha = 0.45 + 0.55 * fade; g.strokeStyle = b.c; g.lineWidth = b.w || 5;
        g.lineJoin = "round"; g.lineCap = "round"; g.shadowColor = b.g || b.c; g.shadowBlur = 34;
        g.beginPath(); b.path.forEach((p, i) => (i ? g.lineTo(p[0], p[1]) : g.moveTo(p[0], p[1]))); g.stroke();
        g.shadowBlur = 0; g.strokeStyle = "#fff"; g.globalAlpha *= 0.5; g.lineWidth = (b.w || 5) * 0.35; g.stroke();
        g.restore();
      });
    };
  };

  FX.star = (color) => `<svg viewBox="-100 -100 200 200" width="100%" height="100%" style="overflow:visible"><defs><radialGradient id="sg${color.slice(1)}"><stop offset="0" stop-color="#fff"/><stop offset=".25" stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="${color}" stop-opacity="0"/></radialGradient></defs><circle r="92" fill="url(#sg${color.slice(1)})"/><path d="M0-100 2.5-4 100 0 2.5 4 0 100-2.5 4-100 0-2.5-4Z" fill="#fff"/></svg>`;

  FX.DISCORD = "M20.317 4.3698a19.7913 19.7913 0 00-4.8851-1.5152.0741.0741 0 00-.0785.0371c-.211.3753-.4447.8648-.6083 1.2495-1.8447-.2762-3.68-.2762-5.4868 0-.1636-.3933-.4058-.8742-.6177-1.2495a.077.077 0 00-.0785-.037 19.7363 19.7363 0 00-4.8852 1.515.0699.0699 0 00-.0321.0277C.5334 9.0458-.319 13.5799.0992 18.0578a.0824.0824 0 00.0312.0561c2.0528 1.5076 4.0413 2.4228 5.9929 3.0294a.0777.0777 0 00.0842-.0276c.4616-.6304.8731-1.2952 1.226-1.9942a.076.076 0 00-.0416-.1057c-.6528-.2476-1.2743-.5495-1.8722-.8923a.077.077 0 01-.0076-.1277c.1258-.0943.2517-.1923.3718-.2914a.0743.0743 0 01.0776-.0105c3.9278 1.7933 8.18 1.7933 12.0614 0a.0739.0739 0 01.0785.0095c.1202.099.246.1981.3728.2924a.077.077 0 01-.0066.1276 12.2986 12.2986 0 01-1.873.8914.0766.0766 0 00-.0407.1067c.3604.698.7719 1.3628 1.225 1.9932a.076.076 0 00.0842.0286c1.961-.6067 3.9495-1.5219 6.0023-3.0294a.077.077 0 00.0313-.0552c.5004-5.177-.8382-9.6739-3.5485-13.6604a.061.061 0 00-.0312-.0286zM8.02 15.3312c-1.1825 0-2.1569-1.0857-2.1569-2.419 0-1.3332.9555-2.4189 2.157-2.4189 1.2108 0 2.1757 1.0952 2.1568 2.419 0 1.3332-.9555 2.4189-2.1569 2.4189zm7.9748 0c-1.1825 0-2.1569-1.0857-2.1569-2.419 0-1.3332.9554-2.4189 2.1569-2.4189 1.2108 0 2.1757 1.0952 2.1568 2.419 0 1.3332-.946 2.4189-2.1568 2.4189Z";
  window.FX = FX;
})();
