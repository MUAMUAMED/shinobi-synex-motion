"""Versão 2: coreografia da recriação do Voltz (keyframes originais) com o conteúdo do Shinobi Synex."""
import json
import pathlib
import re

RAIZ = pathlib.Path(__file__).resolve().parents[1]
C = RAIZ / "compositions"

CORAL, VERDE, VERM = "#ff5a26", "#2ee89f", "#ff3030"
CURSOR = '<svg width="74" height="108" viewBox="0 0 30 44" style="overflow:visible;display:block"><path d="M1 1V35L10 27 16 41 23 38 17 24H29Z" fill="#fff" stroke="#111" stroke-width="2" stroke-linejoin="round"/></svg>'
BASE_P = json.loads((RAIZ / "assets" / "audio" / "palavras_base.json").read_text(encoding="utf-8"))
NOVA_P = json.loads((RAIZ / "assets" / "audio" / "tomadas" / "aw1.json").read_text(encoding="utf-8"))
NOVA_P = [p for i, p in enumerate(NOVA_P) if not (p["w"] == "Mas" and NOVA_P[i + 1]["w"] == "foi")]
assert len(BASE_P) == len(NOVA_P)
MAPA = [[0, 0]]
for a_, b_ in zip(BASE_P, NOVA_P):
    if a_["s"] > MAPA[-1][0] and b_["s"] > MAPA[-1][1]:
        MAPA.append([a_["s"], b_["s"]])
MAPA.append([BASE_P[-1]["e"], NOVA_P[-1]["e"]])


def T(t):
    for (a0, b0), (a1, b1) in zip(MAPA, MAPA[1:]):
        if t <= a1:
            return b0 + (t - a0) * (b1 - b0) / (a1 - a0)
    return t + MAPA[-1][1] - MAPA[-1][0]


(RAIZ / "assets" / "words.js").write_text(
    "window.WORDS=" + json.dumps([{"s": p["s"], "e": p["e"]} for p in BASE_P]) + ";window.TMAP=" + json.dumps(MAPA) + ";", encoding="utf-8")
DUR = 58.6
CENAS = [("a", 0, 7.62), ("b", 7.62, 10.7), ("c", 10.7, 15.5), ("d", 15.5, 24.0), ("e", 24.0, 30.35),
         ("f", 30.35, 40.0), ("g", 40.0, 50.55), ("h", 50.55, DUR)]

fx = (RAIZ / "assets" / "fx.js").read_text(encoding="utf-8")
if "FX.pk" not in fx:
    fx = fx.replace("  window.FX = FX;", """  // Keyframes em frames do Voltz, remapeados para o tempo da narracao e para 16:9.
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
  window.FX = FX;""")
    (RAIZ / "assets" / "fx.js").write_text(fx, encoding="utf-8")

BASE = f"""
#root {{ position:absolute; inset:0; background:#000; overflow:hidden; font-family:"Outfit",sans-serif; color:#fff; }}
#root .a {{ position:absolute; left:0; top:0; }}
#root .ab {{ position:absolute; }}
#root .t {{ white-space:nowrap; letter-spacing:-.015em; line-height:1.05; }}
#root .t span {{ display:inline-block; }}
#root .t span + span {{ margin-left:.14em; }}
#root .co {{ color:{CORAL}; }} #root .ve {{ color:{VERDE}; }}
#root canvas {{ position:absolute; left:0; top:0; }}
#root .chibi {{ position:absolute; left:0; top:0; width:100%; height:100%; }}
#root .full {{ position:absolute; inset:0; }}
"""


def chibi(cena, pares, tam=620, wid=None):
    wid = wid or f"{cena}-ch"
    imgs = "".join(
        f'<img id="{cena}{p}f" class="chibi" src="assets/chibi/{p}f.png" alt=""/>'
        f'<img id="{cena}{p}a" class="chibi" src="assets/chibi/{p}a.png" alt=""/>' for p in pares)
    return f'<div id="{wid}" class="a" style="width:{tam}px;height:{tam}px" data-layout-allow-overflow data-layout-allow-overlap>{imgs}</div>'


def w(prefixo, lista, inicio=0, classes=None):
    classes = classes or {}
    return " ".join(f'<span id="{prefixo}{i + inicio}"{" class=" + chr(34) + classes[i] + chr(34) if i in classes else ""}>{p}</span>' for i, p in enumerate(lista))


def cv(i):
    return f'<canvas id="{i}" width="1920" height="1080" data-layout-ignore></canvas>'


def cena(id_, css, html, js):
    (C / f"{id_}.html").write_text(f"""<template>
  <style>{BASE}{css}</style>
  <div id="root" data-composition-id="{id_}" data-width="1920" data-height="1080">
{html}
  </div>
  <script>
    (function () {{
      const S = {dict((c[0], c[1]) for c in CENAS)[id_]}, tl = FX.tl(S), center = {{ xPercent: -50, yPercent: -50 }};
      const faixa = (s, a, b) => {{ gsap.set(s, {{ opacity: 0 }}); tl.set(s, {{ opacity: 1 }}, Math.max(a - S, 0.001)); tl.set(s, {{ opacity: 0 }}, b - S); }};
{js}
      window.__timelines["{id_}"] = tl;
    }})();
  </script>
</template>
""", encoding="utf-8")


ESTRELA = "M0-100 14-58 48-88 42-44 86-52 58-16 100 0 58 16 86 52 42 44 48 88 14 58 0 100-14 58-48 88-42 44-86 52-58 16-100 0-58-16-86-52-42-44-48-88-14-58Z"
RAIOS = "".join(f'<line x1="0" y1="0" x2="{x}" y2="{y}"/>' for x, y in [(60, -520), (470, -300), (540, 60), (360, 460), (-30, 560), (-420, 370), (-500, -140)])

# ---------- A: Sério / convite genérico / cartões iguais ----------
def carta_gen(i):
    return (f'<div id="a-k{i}" class="a kg"><div class="av">RP</div><div class="nm">RP | Genérico</div>'
            f'<div id="a-s{i}" class="sh"></div></div>')


cena("a", f"""
#root .co {{ color:{VERM}; }}
#a-glow {{ width:1400px; height:1400px; border-radius:50%; background:radial-gradient(#7a0d0066,#0000 68%); }}
#a-big line {{ stroke:{VERM}; stroke-width:112; stroke-linecap:round; }}
#a-grid {{ background-image:linear-gradient(#ffffff0c 3px,transparent 3px),linear-gradient(90deg,#ffffff0c 3px,transparent 3px); background-size:92px 92px; }}
#a-card {{ width:760px; height:500px; border-radius:50px; background:linear-gradient(160deg,#3c3c3f,#232326 70%); border:3px solid #5a5a5d; overflow:hidden; text-align:center; }}
#a-v {{ position:absolute; left:320px; top:44px; width:120px; height:120px; border-radius:24px; background:linear-gradient(#7c7c82,#55555a); display:flex; align-items:center; justify-content:center; font-size:62px; font-weight:700; }}
#a-inv {{ position:absolute; left:0; width:100%; top:182px; font-size:25px; color:#8f8f93; font-weight:500; }}
#a-title {{ position:absolute; left:0; width:100%; top:214px; font-size:62px; font-weight:600; letter-spacing:-.02em; }}
#a-stat {{ position:absolute; left:0; width:100%; top:292px; font-size:25px; color:#c9c9cc; }}
#a-btn {{ position:absolute; left:60px; top:354px; width:640px; height:92px; border-radius:12px; background:#5a5a60; font-size:30px; font-weight:600; display:flex; align-items:center; justify-content:center; overflow:hidden; }}
#a-shine {{ position:absolute; top:0; height:100%; width:420px; background:linear-gradient(90deg,#fff0,#fffc 60%,#e6e6ee); }}
#a-cap {{ font-size:56px; font-weight:400; color:#e4e4e6; text-align:center; }}
#root .kg {{ width:500px; height:170px; border-radius:30px; background:linear-gradient(120deg,#6c6c70,#44444a); overflow:hidden; display:flex; align-items:center; gap:22px; padding-left:26px; }}
#root .kg .av {{ width:112px; height:112px; border-radius:50%; background:#2b2b2f; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:38px; color:#9a9aa0; }}
#root .kg .nm {{ font-size:38px; font-weight:500; color:#d6d6da; white-space:nowrap; }}
#root .sh {{ position:absolute; inset:0; background:linear-gradient(90deg,#fffffff5 0%,#ffffffee 48%,#fff0 66%); }}
#a-warm {{ background:radial-gradient(ellipse at 50% 70%,#ffd0d0b0,#d6505055 40%,#8c1a1a44 70%,#0000); mix-blend-mode:screen; }}
#a-pink {{ background:radial-gradient(ellipse at 50% 62%,#ffc0c055,#c830304d 50%,#0000 88%); mix-blend-mode:screen; }}
#root .zz {{ fill:none; stroke-width:15; stroke-linejoin:round; stroke-linecap:round; }}
""", f"""
    <div id="a-intro" class="full" data-layout-allow-overflow data-layout-allow-overlap>
      <div id="a-glow" class="a" data-layout-ignore></div>
      <svg id="a-big" class="a" width="1200" height="1200" viewBox="-600 -600 1200 1200" style="overflow:visible;filter:blur(13px)" data-layout-ignore><circle r="130" fill="{VERM}"/>{RAIOS}</svg>
      <svg id="a-small" class="a" width="330" height="330" viewBox="-100 -100 200 200" style="filter:blur(1.5px)" data-layout-ignore><path fill="{VERM}" d="{ESTRELA}"/></svg>
      {chibi("a", ["19"], 640)}
      <div id="a-nome" class="a t co" style="font-size:112px;font-weight:600">Sério...</div>
    </div>
    <div id="a-stage" class="full" data-layout-allow-overflow data-layout-allow-overlap>
      <div id="a-grid" class="full" data-layout-ignore></div>
      {cv("a-conf")}
      <div id="a-card" class="a" data-layout-allow-overflow>
        <div id="a-v">RP</div><div id="a-inv">Você foi convidado para entrar</div><div id="a-title">RP de Naruto</div>
        <div id="a-stat">igualzinho a todos os outros</div><div id="a-btn">Aceitar convite<div id="a-shine"></div></div>
      </div>
      <div id="a-cap" class="a t">{w("a-p", ["Tá", "todo", "mundo", "cansado", "daqueles", "RPs", "genéricos", "de", "Naruto"], 0, {5: "co", 6: "co", 8: "co"})}</div>
      {cv("a-conf2")}
    </div>
    <div id="a-st2" class="full" data-layout-allow-overflow data-layout-allow-overlap>
      <div id="a-warm" class="full" data-layout-ignore></div><div id="a-pink" class="full" data-layout-ignore></div>
      {cv("a-dust")}
      <div id="a-txt" class="a t" style="font-size:66px;font-weight:600">{w("a-q", ["são", "sempre", "as", "mesmas", "coisas"], 0, {1: "co", 3: "co", 4: "co"})}</div>
      {carta_gen(0)}{carta_gen(1)}{carta_gen(2)}
      <svg id="a-z1" class="a" width="110" height="190" viewBox="0 0 110 190" data-layout-ignore><path class="zz" stroke="#b9b9b9" d="M95 40 62 12 30 60 65 76 12 110 50 140 28 178 70 160"/></svg>
      {cv("a-bolt")}
    </div>
    <div id="a-end" class="a t" style="font-size:66px;font-weight:600">{w("a-e", ["e", "nenhuma", "inovação.."], 0)}</div>
""", """
      // Abertura: estrela borrada e narradora
      FX.talk(tl, S, [["a19", 0, 1.02]]);
      const m0 = { f0: 0, t0: 0, r: 1.05 / 24 };
      FX.pk(tl, "#a-glow", S, m0, [[8, { ...center, x: 900, y: 150, opacity: 0 }], [14, { opacity: 1 }], [20, { opacity: 0.8 }], [24, { opacity: 0 }]]);
      FX.pk(tl, "#a-big", S, m0, [[1, { ...center, x: -240, y: 1950, rotation: 20, scale: 0.5 }], [4, { y: 1560, rotation: 6, scale: 0.9 }, "power3.out"], [10, { x: -200, y: 1400, rotation: -3, scale: 1 }, "power2.out"], [22, { y: 1340, rotation: -14, opacity: 1 }], [24, { opacity: 0 }]]);
      FX.pk(tl, "#a-small", S, m0, [[2, { ...center, x: 1160, y: 330, scale: 0.6, rotation: -30 }], [10, { x: 940, y: 590, scale: 1, rotation: 0 }, "power3.out"], [20, { x: 925, y: 610, rotation: 18, opacity: 1 }], [24, { opacity: 0, x: 860 }]]);
      FX.k(tl, "#a-ch", S, [[0, { ...center, x: 960, y: 900, scale: 0.5, opacity: 0, filter: "blur(10px)" }], [0.1, { opacity: 1 }], [0.34, { y: 440, scale: 1, filter: "blur(0px)" }, "expo.out"], [0.9, { y: 420 }], [1.05, { y: 380, opacity: 0, filter: "blur(8px)" }]]);
      FX.k(tl, "#a-nome", S, [[0.1, { ...center, x: 960, y: 900, opacity: 0, filter: "blur(8px)" }], [0.3, { opacity: 1, filter: "blur(0px)" }], [0.9, { y: 885 }], [1.05, { y: 860, opacity: 0, filter: "blur(8px)" }]]);
      faixa("#a-intro", 0, 1.06); faixa("#a-stage", 1.05, 4.75); faixa("#a-st2", 4.7, 7.0);
      // Cartao de convite sobe girando em 3D (frames do Voltz 24 a 90)
      gsap.set("#a-card", { transformPerspective: 1500 });
      const m1 = { f0: 24, t0: 1.05, r: 3.65 / 66 };
      FX.pk(tl, "#a-card", S, m1, [[24, { ...center, x: 640, y: 1800, scale: 0.34, rotationY: 74, rotation: -2, filter: "blur(10px)", opacity: 0.2 }], [29, { x: 540, y: 1340, scale: 0.72, rotationY: 28, opacity: 0.9, filter: "blur(4px)" }, "power2.out"], [33, { x: 540, y: 1020, scale: 0.88, rotationY: -10, rotation: -2, opacity: 1, filter: "blur(1px)" }, "power2.out"], [40, { y: 900, scale: 1, rotationY: -2, rotation: -1.5, filter: "blur(0px)" }, "power2.out"], [60, { y: 850, rotationY: 0, rotation: 0 }], [80, { y: 845, scale: 0.94 }], [83, { y: 835, scale: 0.86, filter: "blur(1px)" }], [86, { y: 800, scale: 0.72, filter: "blur(5px)" }, "power1.in"], [88, { y: 790, scale: 0.42, filter: "blur(8px)" }, "power2.in"], [89, { scale: 0.14 }], [90, { scale: 0, opacity: 0 }]]);
      FX.pk(tl, "#a-cap", S, m1, [[34, { ...center, x: 540, y: 1560, opacity: 0 }], [36, { opacity: 1 }], [42, { y: 1400 }], [60, { y: 1305 }], [80, { y: 1310, scale: 0.95 }], [86, { y: 1230, scale: 0.72, filter: "blur(5px)" }, "power1.in"], [88, { y: 1140, scale: 0.4, opacity: 0 }]]);
      [[0, 1.1], [1, 1.3], [2, 1.55], [3, 1.85], [4, 2.4], [5, 2.8], [6, 3.41], [7, 4.04], [8, 4.15]].forEach(([i, t]) => FX.w(tl, "#a-p" + i, S, t, 0.24));
      FX.pk(tl, "#a-shine", S, Object.assign({}, m1, { dx: 0, dy: 0 }), [[32, { x: -560 }], [50, { x: 900 }, "power1.inOut"]]);
      FX.pk(tl, "#a-grid", S, m1, [[34, { opacity: 0, scale: 1.1 }], [44, { opacity: 1 }], [84, { opacity: 0.8, scale: 1 }], [89, { opacity: 0 }]]);
      const CC = ["#c81e1e", "#ff3030", "#8c1010"];
      const C1 = FX.jato(document.getElementById("a-conf"), { seed: 5, n: 240, colors: CC, x: 960, y: 1120, spread: 1.5, speed: 2300, t0: 1.12 });
      const C2 = FX.jato(document.getElementById("a-conf2"), { seed: 9, n: 70, colors: CC, x: 960, y: 1100, spread: 1.3, speed: 1700, t0: 1.2 });
      FX.drive(tl, S, 1.05, 4.75, (t) => { C1(t); C2(t); });
      FX.pk(tl, "#a-conf", S, Object.assign({}, m1, { dx: 0, dy: 0 }), [[58, { opacity: 1 }], [80, { opacity: 0.35 }], [86, { opacity: 0 }]]);
      FX.pk(tl, "#a-conf2", S, Object.assign({}, m1, { dx: 0, dy: 0 }), [[54, { opacity: 0.95 }], [76, { opacity: 0 }]]);
      // Tres cartoes identicos sobem do mesmo ponto
      gsap.set("#a-txt", { ...center, x: 960, y: 200 });
      [[0, 4.72], [1, 4.99], [2, 5.36], [3, 5.5], [4, 5.9]].forEach(([i, t]) => FX.w(tl, "#a-q" + i, S, t, 0.2));
      [[0, 4.95, 400], [1, 5.32, 960], [2, 5.72, 1520]].forEach(([i, t, x]) => {
        FX.k(tl, "#a-k" + i, S, [[t - 0.01, { ...center, x: x, y: 980, scale: 0.08, rotation: -20, opacity: 0, transformPerspective: 1500 }], [t, { opacity: 1 }], [t + 0.1, { y: 800, scale: 0.8, rotation: -6 }, "power2.out"], [t + 0.2, { y: 660, scale: 1.2, rotation: 6 }, "power2.out"], [t + 0.34, { y: 560, scale: 1.04, rotation: 2 }, "power1.out"], [t + 0.5, { y: 520, scale: 1, rotation: -2 }, "power2.out"], [6.9, { y: 500, rotation: 0 }]]);
        FX.k(tl, "#a-s" + i, S, [[t + 0.1, { x: -640 }], [t + 0.34, { x: -200 }], [t + 0.5, { x: 100 }], [t + 0.7, { x: 620 }]]);
      });
      FX.k(tl, "#a-z1", S, [[5.4, { x: 90, y: 400, opacity: 0, scale: 0.4 }], [5.5, { opacity: 1, scale: 1 }, "back.out(2)"], [6.4, { rotation: 8 }]]);
      FX.k(tl, "#a-warm", S, [[4.95, { opacity: 0 }], [5.02, { opacity: 1 }], [5.25, { opacity: 0 }]]);
      FX.k(tl, "#a-pink", S, [[5.3, { opacity: 0 }], [5.4, { opacity: 1 }], [5.6, { opacity: 0.1 }], [5.72, { opacity: 0.1 }], [5.8, { opacity: 1 }], [6.0, { opacity: 0 }]]);
      const Y = "#ff6a6a", P = "#ff3030";
      const B = FX.bolts(document.getElementById("a-bolt"), [
        { t: 5.0, d: 0.07, c: Y, w: 8, pts: [[0, 240], [210, 420], [330, 560]] }, { t: 5.08, d: 0.07, c: Y, w: 7, pts: [[650, 120], [520, 330], [420, 500]] },
        { t: 5.4, d: 0.07, c: P, w: 8, pts: [[700, 1080], [860, 800], [960, 560]] }, { t: 5.48, d: 0.07, c: P, w: 6, pts: [[1300, 200], [1100, 380], [980, 500]] },
        { t: 5.8, d: 0.07, c: P, w: 9, pts: [[1920, 300], [1700, 420], [1560, 500]] }, { t: 5.88, d: 0.07, c: P, w: 6, pts: [[1200, 1000], [1400, 760], [1500, 560]] }], 88);
      const D = FX.dust(document.getElementById("a-dust"), { seed: 12, n: 70, color: "#e9e4dc", alpha: 0.7 });
      FX.drive(tl, S, 4.7, 7.0, (t) => { B(t); D(t); });
      FX.k(tl, "#a-st2", S, [[6.25, { scale: 1, filter: "blur(0px)", transformOrigin: "50% 40%" }], [6.34, { filter: "blur(7px)" }], [6.42, { scale: 0.96, filter: "blur(24px)" }]]);
      tl.to("#a-st2", { autoAlpha: 0, duration: 0.05, immediateRender: false }, 6.42 - S);
      // "e nenhuma inovacao.." encolhe ate virar um ponto
      gsap.set("#a-end", { ...center, x: 960, y: 530 });
      [[0, 6.44], [1, 6.56], [2, 6.97]].forEach(([i, t]) => FX.w(tl, "#a-e" + i, S, t, 0.2));
      FX.k(tl, "#a-end", S, [[7.3, { scale: 1 }], [7.42, { scale: 1.1 }, "power2.out"], [7.5, { scale: 0.96 }], [7.56, { scale: 0.5 }], [7.61, { scale: 0.05, opacity: 0 }]]);
""")

# ---------- B: Voltz composição b ----------
cena("b", f"""
#b-side {{ background:linear-gradient(90deg,#5a0808,#2c0404 16%,#0000 34%,#0000 66%,#2c0404 84%,#5a0808); }}
#b-org {{ background:radial-gradient(ellipse at 50% 45%,#f26c0a,#c95405 52%,#8c3a03); }}
#b-box {{ width:360px; height:360px; border-radius:64px; background:linear-gradient(145deg,#ff7f3f,#ee4d12); box-shadow:-16px 18px 0 #c84608,-20px 22px 8px #0005; display:flex; align-items:center; justify-content:center; font-size:230px; font-weight:800; }}
#b-disc {{ width:720px; height:720px; border-radius:50%; background:#e0641c; }}
""", f"""
    <div id="b-side" class="full" data-layout-ignore></div>
    <div id="b-txt" class="a t" style="font-size:64px;font-weight:400;color:#eee">{w("b-p", ["Foi", "fugindo", "dessa", "moda", "que", "surgiu", "o"])}</div>
    <div id="b-org" class="full" data-layout-ignore></div>
    {cv("b-dust")}
    <div id="b-disc" class="a" data-layout-ignore></div>
    <div id="b-box" class="a" data-layout-allow-overflow>S</div>
    {cv("b-bolt")}
    <svg id="b-arcs" class="a" width="1920" height="1080" viewBox="0 0 1920 1080" fill="none" stroke="#e8631a" stroke-width="5" stroke-linecap="round" data-layout-ignore><path id="b-a1" pathLength="1" d="M1940 80C1500 180 1400 500 1900 760"/><path id="b-a2" pathLength="1" d="M1060 800 1300 680 1400 780M1060 800C1200 960 1400 1020 1620 1050"/></svg>
    <div id="b-nome" class="a t" style="font-size:110px;font-weight:600">{w("b-n", ["Shinobi", "Synex"], 0, {1: "co"})}</div>
    <div id="b-cur" class="a">{CURSOR}</div>
""", """
      const m = { f0: 92, t0: 7.62, r: 3.08 / 54 };
      FX.pk(tl, "#b-txt", S, { f0: 92, t0: 7.62, r: 1.74 / 22 }, [[92, { ...center, x: 540, y: 1050, opacity: 1, scale: 1 }], [97, { y: 975 }, "power2.out"], [109, { y: 958 }], [110, { scale: 0.97 }], [111, { scale: 0.86 }, "power2.in"], [112, { scale: 0.66 }], [113, { scale: 0.36 }], [114, { scale: 0.05, opacity: 0 }]]);
      [[0, 7.65], [1, 7.84], [2, 8.3], [3, 8.58], [4, 8.88], [5, 9.0], [6, 9.38]].forEach(([i, t]) => FX.w(tl, "#b-p" + i, S, t - 0.02, 0.18));
      FX.k(tl, "#b-side", S, [[7.65, { opacity: 0 }], [8.3, { opacity: 0.35 }], [9.3, { opacity: 0.7 }]]);
      // O flash e a virada acontecem sobre "Shinobi"
      const n = { f0: 112, t0: 9.34, r: 0.98 / 34 };
      FX.pk(tl, "#b-org", S, Object.assign({}, n, { dx: 0, dy: 0 }), [[112, { opacity: 0 }], [113, { opacity: 0.75 }], [114, { opacity: 1 }], [116, { opacity: 0.85 }], [118, { opacity: 0.45 }], [120, { opacity: 0.32 }], [124, { opacity: 0.4 }], [127, { opacity: 0.75 }], [130, { opacity: 0.75 }], [133, { opacity: 0.35 }], [136, { opacity: 0.1 }], [140, { opacity: 0 }]]);
      gsap.set("#b-box", { transformPerspective: 1200 });
      FX.pk(tl, "#b-box", S, n, [[113, { ...center, x: 540, y: 980, scale: 0.7, rotation: -30, rotationY: 80, rotationX: 30, opacity: 0, filter: "blur(16px)" }], [115, { opacity: 0.8, rotation: -28, rotationY: 80, filter: "blur(10px)" }], [116, { rotation: 0, rotationY: 82, filter: "blur(6px)", opacity: 1 }], [118, { rotation: 10, rotationY: 45, rotationX: 10, filter: "blur(1px)", scale: 0.85 }, "power1.out"], [120, { rotation: -6, rotationY: 22, filter: "blur(0px)", scale: 1 }, "power2.out"], [124, { rotation: 0, rotationY: 6, rotationX: 0, y: 950 }, "power2.out"], [128, { scale: 0.65, y: 950, filter: "blur(0px) brightness(1.5) saturate(0.6)" }, "power2.out"], [132, { scale: 0.62 }], [134, { scale: 0.7, filter: "blur(3px)", rotationX: 18, y: 940 }], [136, { scale: 0.66, filter: "blur(9px)", rotationX: 55, y: 930 }], [138, { scale: 0.4, opacity: 0, filter: "blur(16px)" }]]);
      FX.pk(tl, "#b-disc", S, n, [[123, { ...center, x: 540, y: 950, scale: 0.2, opacity: 0 }], [124, { scale: 1, opacity: 0.55 }], [126, { scale: 0.56, opacity: 1, backgroundColor: "#ea5f10" }, "power2.out"], [128, { scale: 0.36, backgroundColor: "#f2b417" }, "power2.out"], [130, { scale: 0.46, backgroundColor: "#ef7a12" }], [133, { scale: 0.53, backgroundColor: "#a84a10", opacity: 0.8 }], [136, { opacity: 0 }]]);
      const fr = (f) => n.t0 + (f - n.f0) * n.r;
      const B = FX.bolts(document.getElementById("b-bolt"), [
        { t: fr(128), d: 0.09, c: "#ff6a14", w: 7, pts: [[300, 300], [640, 180], [760, 0]] }, { t: fr(129), d: 0.09, c: "#ff7a1a", w: 5, pts: [[0, 460], [840, 460], [1300, 200], [1920, 180]] },
        { t: fr(131), d: 0.09, c: "#ff6a14", w: 5, pts: [[0, 460], [1040, 460], [1300, 220], [1500, 120]] }, { t: fr(141), d: 0.13, c: "#f1560e", w: 40, pts: [[300, 800], [700, 780], [900, 600], [1100, 860], [1120, 1080]] },
        { t: fr(143), d: 0.09, c: "#f1560e", w: 34, pts: [[0, 800], [560, 960], [1300, 780], [1920, 700]] }, { t: fr(144), d: 0.09, c: "#d84c0a", w: 8, pts: [[0, 830], [420, 980], [700, 1080]] }], 21);
      const D = FX.dust(document.getElementById("b-dust"), { seed: 4, n: 110, color: "#ff7a2a", alpha: 0.8 });
      FX.drive(tl, S, 9.34, 10.7, (t) => { B(t); D(t); });
      FX.k(tl, "#b-dust", S, [[9.36, { opacity: 0 }], [9.6, { opacity: 0.9 }]]);
      FX.pk(tl, "#b-a1", S, Object.assign({}, n, { dx: 0, dy: 0 }), [[136, { strokeDasharray: 1, strokeDashoffset: 1 }], [139, { strokeDashoffset: 0.25 }], [146, { strokeDashoffset: -0.9 }]]);
      FX.pk(tl, "#b-a2", S, Object.assign({}, n, { dx: 0, dy: 0 }), [[133, { strokeDasharray: 1, strokeDashoffset: 1 }], [136, { strokeDashoffset: 0 }, "power2.out"], [140, { strokeDashoffset: -1 }]]);
      FX.clique(tl, "#b-cur", S, [1560, 1100], [1010, 570], [1700, 1200], 9.6, 9.69, 9.86);
      gsap.set("#b-nome", { ...center, x: 960, y: 530, opacity: 0 });
      tl.to("#b-nome", { opacity: 1, duration: 0.01, immediateRender: false }, 10.0 - S);
      FX.k(tl, "#b-nome", S, [[10.01, { scale: 1 }], [10.7, { scale: 1.05 }]]);
      gsap.set("#b-nome", { opacity: 0 });
      FX.w(tl, "#b-n0", S, 10.02, 0.2); FX.w(tl, "#b-n1", S, 10.14, 0.2);
""")

# ---------- C: mundo de blocos (Voltz d) com as gameplays ----------
blocos = "".join(f'<div id="c-t{i}" class="ab bl" style="left:{x}px;top:{y}px;width:{w_}px;height:{h}px"></div>' for i, (x, y, w_, h) in enumerate(
    [(150, 120, 520, 340), (980, 420, 420, 190), (1550, 120, 460, 300), (260, 760, 560, 360), (1200, 800, 620, 300), (1900, 640, 380, 300), (650, 40, 240, 120), (40, 500, 300, 160)]))
cena("c", f"""
#c-mundo {{ position:absolute; left:-180px; top:-120px; width:2280px; height:1320px; }}
#root .bl {{ border-radius:60px; background:radial-gradient(circle at 40% 45%,#ff6a2a,#e0500c 70%,#b5440a); filter:blur(4px); }}
#c-fog {{ background:#2f3d52; }} #c-base {{ background:#3a475b; }}
#c-esc {{ background:#000; }} #c-flash {{ background:radial-gradient(ellipse at 70% 40%,#f8bf72,#c8aa90 55%,#9b9a98); filter:blur(10px); }}
#root .pv {{ width:880px; height:600px; border-radius:48px; overflow:hidden; border:5px solid #ffffffd0; background:#000; box-shadow:0 30px 80px #000a; }}
#c-rdr, #c-kcd {{ width:100%; height:100%; object-fit:cover; display:block; }}
#root .lb {{ font-size:48px; font-weight:600; }}
""", f"""
    <div id="c-base" class="full" data-layout-ignore></div>
    <div id="c-mundo" data-layout-allow-overflow data-layout-allow-overlap data-layout-ignore>{blocos}</div>
    <div id="c-fog" class="full" data-layout-ignore></div>
    <div id="c-txt" class="a t" style="font-size:72px;font-weight:600">{w("c-p", ["Inspirado", "nas", "mecânicas", "de"])}</div>
    <svg id="c-sq" class="a" width="1920" height="1080" viewBox="0 0 1920 1080" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round" data-layout-ignore><path id="c-pth" pathLength="1" d="M1000 610C1040 585 1060 585 1090 603S1140 620 1190 590"/></svg>
    <div id="c-p1" class="a pv" data-layout-allow-overflow><video id="c-rdr" class="clip" data-start="{T(12.15) - T(10.7):.3f}" data-duration="{T(15.5) - T(12.15):.3f}" data-track-index="2" src="assets/video/rdr.mp4" muted playsinline></video></div>
    <div id="c-p2" class="a pv" data-layout-allow-overflow><video id="c-kcd" class="clip" data-start="{T(13.45) - T(10.7):.3f}" data-duration="{T(15.5) - T(13.45):.3f}" data-track-index="3" src="assets/video/kcd.mp4" muted playsinline></video></div>
    <div id="c-l1" class="a t lb">Red Dead Redemption</div>
    <div id="c-l2" class="a t lb">Kingdom Come: Deliverance</div>
    <div id="c-flash" class="full" data-layout-ignore></div>
    <div id="c-esc" class="full" data-layout-ignore></div>
""", """
      // Estrobo de entrada: cada par e a opacidade do escuro naquele frame do Voltz
      const dt = 1 / 30, T0 = 10.7;
      FX.k(tl, "#c-flash", S, [[T0, { opacity: 1 }], [T0 + 2 * dt, { opacity: 1 }], [T0 + 2.1 * dt, { opacity: 0 }]]);
      const dark = [[2, 1], [3, 0.15], [4, 0.85], [5, 0.92], [6, 0.05], [7, 0.1], [8, 0.8], [9, 0.7], [11, 0.6], [12, 0.1], [13, 0], [15, 0.2], [16, 0.5], [17, 0.2], [19, 0]];
      gsap.set("#c-esc", { opacity: 1 });
      dark.forEach(([f, o], i) => { if (i) tl.fromTo("#c-esc", { opacity: dark[i - 1][1] }, { opacity: o, duration: (f - dark[i - 1][0]) * dt, ease: "none", immediateRender: false }, T0 + dark[i - 1][0] * dt - S); });
      const fim = [[0, 0], [4, 0.97], [5, 1]];
      tl.fromTo("#c-esc", { opacity: 0 }, { opacity: 1, duration: 5 * dt, ease: "power2.in", immediateRender: false }, 15.5 - 5 * dt - S);
      FX.k(tl, "#c-mundo", S, [[10.75, { scale: 1.9, y: 120, rotation: 0, filter: "blur(20px)", transformOrigin: "50% 50%" }], [10.95, { scale: 1.15, y: 40, filter: "blur(4px)" }, "power3.out"], [11.6, { scale: 1, y: 0, filter: "blur(0px)" }, "power1.out"], [12.4, { rotation: 7, scale: 1.04, filter: "blur(3px)" }], [13.4, { rotation: 15, scale: 1.34, filter: "blur(10px)" }], [15.5, { rotation: 22, scale: 1.6, filter: "blur(18px)" }]]);
      FX.k(tl, "#c-fog", S, [[10.75, { opacity: 0 }], [11.3, { opacity: 0.42 }], [12.2, { opacity: 0.62 }], [15.5, { opacity: 0.72 }]]);
      gsap.set("#c-txt", { ...center, x: 960, y: 540 });
      [[0, 10.72], [1, 11.34], [2, 11.52], [3, 12.05]].forEach(([i, t]) => FX.w(tl, "#c-p" + i, S, t, 0.2));
      FX.k(tl, "#c-pth", S, [[11.75, { strokeDasharray: 1, strokeDashoffset: 1 }], [11.95, { strokeDashoffset: 0 }, "power2.out"], [12.12, { strokeDashoffset: 0, opacity: 1 }], [12.2, { opacity: 0 }]]);
      FX.k(tl, "#c-txt", S, [[12.1, { scaleX: 1, opacity: 1, filter: "blur(0px)" }], [12.16, { scaleX: 1.4, filter: "blur(4px)", opacity: 0.8 }], [12.22, { scaleX: 2.6, filter: "blur(9px)", x: 1200, opacity: 0.5 }], [12.27, { opacity: 0, x: 1800 }]]);
      gsap.set("#c-p1,#c-p2", { transformPerspective: 1100 });
      // Cada gameplay entra girando, como a pilula do Voltz
      FX.k(tl, "#c-p1", S, [[12.2, { ...center, x: 960, y: 500, rotationY: 86, scale: 0.8, opacity: 0 }], [12.24, { opacity: 1 }], [12.34, { rotationY: 60, scale: 1.05 }], [12.46, { rotationY: 18 }, "power2.out"], [12.6, { rotationY: -3, scale: 1.08 }, "power2.out"], [13.34, { rotationY: 0, scale: 1.02 }], [13.62, { x: 500, scale: 1, rotationY: 8, rotation: -2 }, "expo.out"], [15.25, { x: 490, rotationY: 5, rotation: -1, scale: 0.98 }], [15.46, { x: 960, y: 530, scale: 0.04, opacity: 0, rotation: 30 }, "power3.in"]]);
      FX.k(tl, "#c-p2", S, [[13.5, { ...center, x: 1420, y: 500, rotationY: -86, scale: 0.8, opacity: 0 }], [13.54, { opacity: 1 }], [13.64, { rotationY: -60, scale: 1.05 }], [13.76, { rotationY: -18 }, "power2.out"], [13.92, { rotationY: 3, scale: 1.04 }, "power2.out"], [14.1, { rotationY: -8, rotation: 2, scale: 1 }], [15.25, { x: 1430, rotationY: -5, rotation: 1, scale: 0.98 }], [15.46, { x: 960, y: 530, scale: 0.04, opacity: 0, rotation: -30 }, "power3.in"]]);
      FX.k(tl, "#c-l1", S, [[12.5, { ...center, x: 960, y: 880, opacity: 0, filter: "blur(8px)" }], [12.7, { opacity: 1, filter: "blur(0px)" }], [13.5, { x: 960 }], [13.68, { x: 500 }, "expo.out"], [15.2, { opacity: 1 }], [15.3, { opacity: 0 }]]);
      FX.k(tl, "#c-l2", S, [[13.75, { ...center, x: 1420, y: 880, opacity: 0, filter: "blur(8px)" }], [13.95, { opacity: 1, filter: "blur(0px)" }], [15.2, { opacity: 1 }], [15.3, { opacity: 0 }]]);
""")

# ---------- D: mosaico e odômetro (Voltz j) + cartões subindo (Voltz c) ----------
mos = "".join(f'<img class="cd" src="assets/cards/c{i * 5 % 48:02d}.jpg" alt=""/>' for i in range(42))
cena("d", f"""
#d-m {{ display:grid; grid-template-columns:repeat(7,430px); gap:16px; position:absolute; left:-590px; top:-470px; }}
#root .cd {{ width:430px; height:242px; object-fit:cover; border-radius:18px; display:block; }}
#d-wh {{ background:#fff; }} #d-esc {{ background:#000; }}
#d-n {{ color:{VERDE}; font-size:230px; font-weight:800; overflow:hidden; height:230px; line-height:230px; white-space:nowrap; text-shadow:0 8px 40px #000; }}
#d-n span {{ display:inline-block; vertical-align:top; }}
#d-n i {{ display:block; font-style:normal; height:230px; line-height:230px; text-align:center; }}
#d-pp {{ font-size:64px; font-weight:600; color:#d6f4d6; text-shadow:0 4px 24px #000; }}
#root .kc {{ width:420px; border-radius:30px; overflow:hidden; }}
#root .kc img {{ width:100%; height:236px; object-fit:cover; display:block; }}
#root .kc b {{ display:block; text-align:center; padding:16px 0 18px; font-size:42px; font-weight:600; background:#101014; white-space:nowrap; }}
#root .sh {{ position:absolute; inset:0; background:linear-gradient(90deg,#fffffff5 0%,#ffffffee 48%,#fff0 66%); }}
#d-pink {{ background:radial-gradient(ellipse at 50% 62%,#ffe0e866,#d78aa24d 50%,#0000 88%); mix-blend-mode:screen; }}
#d-t {{ font-size:58px; font-weight:600; text-shadow:0 4px 30px #000; }}
""", f"""
    <div id="d-m" data-layout-allow-overflow data-layout-ignore>{mos}</div>
    <div id="d-esc" class="full" data-layout-ignore></div>
    <div id="d-pink" class="full" data-layout-ignore></div>
    {chibi("d", ["05"], 660)}
    <div id="d-t" class="a t">{w("d-p", ["o", "Shinobi", "Synex", "conta", "com", "mais", "de"], 0, {1: "co", 2: "co"})}</div>
    <div id="d-n" class="a"><span>+</span><span id="d-a" style="width:.5em"><i>0</i><i>1</i></span><span id="d-b"><i>7</i><i>4</i><i>2</i></span><span id="d-c"><i>3</i><i>9</i><i>5</i><i>0</i></span></div>
    <div id="d-pp" class="a t">NPCs</div>
    <div id="d-k0" class="a kc"><img src="assets/cards/c12.jpg" alt=""/><b>rotinas</b><div id="d-s0" class="sh"></div></div>
    <div id="d-k1" class="a kc"><img src="assets/cards/c20.jpg" alt=""/><b>personalidades</b><div id="d-s1" class="sh"></div></div>
    <div id="d-k2" class="a kc"><img src="assets/cards/c27.jpg" alt=""/><b>histórias</b><div id="d-s2" class="sh"></div></div>
    <div id="d-k3" class="a kc"><img src="assets/cards/c33.jpg" alt=""/><b>vidas</b><div id="d-s3" class="sh"></div></div>
    {cv("d-bolt")}
    <div id="d-dif" class="a t" style="font-size:66px;font-weight:600">{w("d-e", ["completamente", "diferentes!"], 0, {1: "co"})}</div>
    <svg id="d-ln" class="a" width="1920" height="1080" viewBox="0 0 1920 1080" fill="none" stroke="#ffc9a8" stroke-width="7" stroke-linecap="round" data-layout-ignore><path id="d-l1" pathLength="1" d="M620 985C700 950 900 960 1020 975S1240 1000 1320 965"/></svg>
    <div id="d-bola" class="a" style="width:150px;height:150px;border-radius:50%;background:#fff" data-layout-ignore></div>
    <div id="d-wh" class="full" data-layout-ignore></div>
""", """
      FX.talk(tl, S, [["d05", 15.5, 19.3]]);
      FX.k(tl, "#d-wh", S, [[15.5, { opacity: 1 }], [15.53, { opacity: 0.85 }], [15.57, { opacity: 0.6 }], [15.6, { opacity: 0.4 }], [15.67, { opacity: 0.18 }], [15.83, { opacity: 0.04 }], [15.9, { opacity: 0 }]]);
      // Mosaico perto ate o numero fechar, corte seco para aberto
      FX.k(tl, "#d-m", S, [[15.5, { transformOrigin: "50% 50%", scale: 1.76, x: 90, y: 60, filter: "blur(12px)" }], [15.63, { scale: 1.72, x: 40, y: 20, filter: "blur(7px)" }, "power2.out"], [15.73, { scale: 1.68, x: 0, y: 0, filter: "blur(3px)" }, "power2.out"], [15.9, { scale: 1.64, x: -20, y: -20, filter: "blur(1px)" }], [18.5, { scale: 1.5, x: -60, y: -40, filter: "blur(0px)" }], [18.52, { scale: 1.5 }], [18.54, { scale: 1.02, x: 0, y: 0 }], [19.3, { scale: 1, y: -14 }], [24, { scale: 0.96, y: -40, filter: "blur(4px)" }]]);
      FX.k(tl, "#d-esc", S, [[15.5, { opacity: 0.2 }], [16, { opacity: 0.42 }], [18.54, { opacity: 0.45 }], [19.25, { opacity: 0.5 }], [19.45, { opacity: 0.74 }]]);
      FX.k(tl, "#d-ch", S, [[15.5, { ...center, x: 620, y: 1100, scale: 0.7, filter: "blur(8px)" }], [15.82, { y: 720, scale: 1, filter: "blur(0px)" }, "expo.out"], [18.54, { y: 700 }], [19.2, { y: 690, scale: 1 }], [19.34, { scale: 0.05, opacity: 0 }, "power3.in"]]);
      gsap.set("#d-t", { ...center, x: 960, y: 150 });
      [[0, 15.52], [1, 15.64], [2, 16.09], [3, 16.58], [4, 16.92], [5, 17.14], [6, 17.45]].forEach(([i, t]) => FX.w(tl, "#d-p" + i, S, t, 0.2));
      FX.k(tl, "#d-t", S, [[19.1, { opacity: 1 }], [19.28, { opacity: 0, filter: "blur(8px)" }]]);
      // Odometro
      FX.k(tl, "#d-n", S, [[17.58, { ...center, x: 1240, y: 680, scale: 1.4, opacity: 0, filter: "blur(6px)" }], [17.68, { y: 640, opacity: 0.8, filter: "blur(4px)" }], [17.8, { y: 500, opacity: 1, filter: "blur(1px)" }], [17.97, { y: 470, filter: "blur(0px)" }], [18.5, { y: 470, scale: 1.42 }], [18.54, { y: 430, scale: 1 }], [19.2, { y: 420, opacity: 1 }], [19.3, { opacity: 0, filter: "blur(6px)" }]]);
      FX.k(tl, "#d-a", S, [[17.62, { y: 0 }], [17.95, { y: -230 }, "power1.inOut"]]);
      FX.k(tl, "#d-b", S, [[17.62, { y: 0 }], [17.85, { y: -230 }, "power1.inOut"], [18.12, { y: -460 }, "power1.inOut"]]);
      FX.k(tl, "#d-c", S, [[17.62, { y: 0 }], [17.8, { y: -230 }, "power1.inOut"], [18.0, { y: -460 }, "power1.inOut"], [18.3, { y: -690 }, "power1.inOut"]]);
      FX.k(tl, "#d-pp", S, [[18.54, { ...center, x: 1240, y: 590, opacity: 0, color: "#6bf06a" }], [18.64, { opacity: 1 }], [18.84, { color: "#d6f4d6" }], [19.2, { y: 580, opacity: 1 }], [19.3, { opacity: 0 }]]);
      // Quatro cartoes sobem do mesmo jeito dos bots do Voltz
      [[0, 19.34, 270], [1, 19.98, 730], [2, 21.04, 1190], [3, 21.9, 1650]].forEach(([i, t, x]) => {
        FX.k(tl, "#d-k" + i, S, [[t - 0.01, { ...center, x: x, y: 1040, scale: 0.08, rotation: -4, opacity: 0 }], [t, { opacity: 0.5 }], [t + 0.1, { y: 900, scale: 0.55, opacity: 1 }, "power2.out"], [t + 0.17, { y: 780, scale: 1.1, rotation: -5 }, "power2.out"], [t + 0.24, { y: 700, scale: 1.26, rotation: -7 }], [t + 0.4, { y: 560, scale: 1.02, rotation: -3 }], [t + 0.6, { y: 490, scale: 0.98, rotation: 2 }], [t + 0.85, { y: 470, scale: 0.96, rotation: 0 }, "power2.out"], [23.7, { y: 455 }], [23.97, { x: 960, y: 900, scale: 0.05, rotation: 25, opacity: 0.4 }, "power3.in"], [23.99, { opacity: 0 }]]);
        FX.k(tl, "#d-s" + i, S, [[t + 0.2, { x: -640 }], [t + 0.28, { x: -420 }], [t + 0.38, { x: -230 }], [t + 0.55, { x: -110 }], [t + 0.75, { x: 620 }]]);
      });
      FX.k(tl, "#d-pink", S, [[19.5, { opacity: 0 }], [19.58, { opacity: 0.9 }], [19.78, { opacity: 0 }], [20.15, { opacity: 0 }], [20.22, { opacity: 0.9 }], [20.42, { opacity: 0 }], [21.2, { opacity: 0 }], [21.28, { opacity: 0.9 }], [21.48, { opacity: 0 }], [22.08, { opacity: 0 }], [22.15, { opacity: 0.9 }], [22.35, { opacity: 0 }]]);
      const Y = "#ffe6a8", P = "#f3a9c0";
      const B = FX.bolts(document.getElementById("d-bolt"), [
        { t: 19.55, d: 0.07, c: Y, w: 8, pts: [[0, 200], [200, 400], [280, 620]] }, { t: 19.62, d: 0.07, c: Y, w: 7, pts: [[560, 120], [420, 360], [300, 520]] },
        { t: 20.2, d: 0.07, c: P, w: 7, pts: [[720, 1080], [700, 800], [730, 620]] }, { t: 20.28, d: 0.07, c: P, w: 6, pts: [[1000, 130], [860, 320], [760, 500]] },
        { t: 21.26, d: 0.07, c: Y, w: 8, pts: [[1400, 1080], [1260, 800], [1200, 620]] }, { t: 21.34, d: 0.07, c: Y, w: 6, pts: [[920, 130], [1060, 320], [1180, 500]] },
        { t: 22.1, d: 0.07, c: P, w: 9, pts: [[1920, 260], [1780, 420], [1660, 520]] }, { t: 22.18, d: 0.07, c: P, w: 7, pts: [[1400, 960], [1540, 780], [1640, 620]] }], 44);
      FX.drive(tl, S, 19.3, 22.4, (t) => B(t));
      gsap.set("#d-dif", { ...center, x: 960, y: 900 });
      FX.w(tl, "#d-e0", S, 22.24, 0.2); FX.w(tl, "#d-e1", S, 23.2, 0.2);
      FX.k(tl, "#d-dif", S, [[23.68, { opacity: 1 }], [23.8, { opacity: 0, filter: "blur(8px)" }]]);
      FX.k(tl, "#d-ln", S, [[23.68, { opacity: 1 }], [23.8, { opacity: 0 }]]);
      FX.k(tl, "#d-bola", S, [[23.82, { ...center, x: 960, y: 900, scale: 0.02, opacity: 0 }], [23.84, { opacity: 1 }], [24.0, { scale: 0.2 }, "power2.out"]]);
      FX.k(tl, "#d-l1", S, [[23.25, { strokeDasharray: 1, strokeDashoffset: 1 }], [23.5, { strokeDashoffset: 0 }, "power2.out"], [24, { strokeDashoffset: 0 }]]);
""")

# ---------- E: bola > pílula > + > vidro > cartão largo (Voltz e) ----------
CORACAO = '<path d="M0 34C-46-2-34-36-14-36-5-36 0-28 0-24 0-28 5-36 14-36 34-36 46-2 0 34Z" fill="currentColor"/>'
cena("e", f"""
#e-pur {{ background:linear-gradient(90deg,#2a0a3c,#0000 32%,#0000 68%,#2a0a3c),linear-gradient(#0000 70%,#1c0a2c); }}
#e-lav {{ background:radial-gradient(ellipse at 50% 45%,#a3a2b5,#b4b1d4 62%,#7d79ad); }}
#e-blu {{ background:radial-gradient(ellipse at 50% 58%,#151a20,#24344a 95%); }}
#e-grn {{ background:linear-gradient(90deg,#103f0c,#000 26%,#000 74%,#103f0c); }}
#e-rosa {{ background:radial-gradient(ellipse at 50% 50%,#ff8fb4,#d84f86 45%,#5e0f35 85%); }}
#e-ball {{ width:150px; height:150px; border-radius:50%; background:#fff; }}
#e-pill {{ width:820px; height:290px; border-radius:80px; background:linear-gradient(#ff7a33,#f25412); box-shadow:0 -8px 0 #ffd5b2,7px 8px 0 #ffd5b2; font-size:92px; font-weight:600; display:flex; align-items:center; justify-content:center; gap:30px; white-space:nowrap; letter-spacing:-.02em; }}
#e-pill img {{ width:170px; height:170px; }}
#e-plus {{ width:240px; height:262px; border-radius:52px; background:#fff; display:flex; align-items:center; justify-content:center; color:#f05d10; font-size:170px; font-weight:800; line-height:1; }}
#e-gl {{ width:780px; height:760px; border-radius:64px; background:linear-gradient(170deg,#ffffff40,#ffffff22); border:6px solid #ffffff99; text-align:center; overflow:hidden; }}
#e-ic {{ position:absolute; left:40px; top:60px; width:688px; height:360px; display:flex; align-items:center; justify-content:center; gap:6px; }}
#e-ic img {{ width:220px; height:220px; }} #e-ic img:nth-child(2) {{ width:290px; height:290px; }}
#e-gt {{ position:absolute; left:0; width:100%; top:450px; font-size:48px; font-weight:500; white-space:nowrap; }}
#e-gb {{ position:absolute; left:90px; top:540px; width:588px; height:130px; border-radius:26px; background:#f05de8; font-size:44px; font-weight:500; display:flex; align-items:center; justify-content:center; white-space:nowrap; }}
#e-wide {{ width:1120px; height:560px; border-radius:52px; background:#111; border:4px solid #aaa; overflow:hidden; }}
#e-wi2 {{ position:absolute; left:0; top:0; width:100%; height:350px; display:flex; align-items:center; justify-content:center; gap:40px; background:linear-gradient(120deg,#2a0d55,#6b1d0c); }}
#e-wi2 img {{ width:210px; height:210px; }} #e-wi2 img:nth-child(2) {{ width:290px; height:290px; }}
#e-wb {{ position:absolute; left:120px; top:360px; width:880px; height:166px; border-radius:34px; background:#fff; display:flex; align-items:center; justify-content:center; font-size:76px; font-weight:500; color:#55555a; white-space:nowrap; }}
#e-wb i {{ font-style:normal; color:{CORAL}; margin-left:.25em; }}
#e-burst {{ width:1000px; height:1000px; }}
#e-ring1, #e-ring2 {{ border-radius:50%; border:26px dotted #ffe4ee; width:980px; height:980px; }}
""", f"""
    <div id="e-pur" class="full" data-layout-ignore></div><div id="e-lav" class="full" data-layout-ignore></div><div id="e-blu" class="full" data-layout-ignore></div><div id="e-grn" class="full" data-layout-ignore></div>
    {cv("e-c1")}
    <div id="e-int" class="a t" style="font-size:60px;font-weight:500">{w("e-p", ["Você", "pode", "fazer"])}</div>
    <div id="e-ball" class="a" data-layout-ignore></div>
    <div id="e-pill" class="a" data-layout-allow-overflow><img src="assets/png/handshake.png" alt=""/>amizade<img src="assets/png/heart.png" alt=""/></div>
    <div id="e-plus" class="a" data-layout-allow-overflow>+</div>
    <div id="e-gl" class="a" data-layout-allow-overflow><div id="e-ic"><img src="assets/png/fire.png" alt=""/><img src="assets/png/scroll.png" alt=""/><img src="assets/png/bolt.png" alt=""/></div><div id="e-gt">Novo ensinamento</div><div id="e-gb">Aprender Jutsus</div></div>
    <div id="e-burst" class="a" data-layout-ignore></div>
    <div id="e-cur" class="a">{CURSOR}</div>
    <div id="e-wide" class="a" data-layout-allow-overflow><div id="e-wi2"><img src="assets/png/sparkles.png" alt=""/><img src="assets/png/eye.png" alt=""/><img src="assets/png/bolt.png" alt=""/></div><div id="e-wb">Receber<i id="e-wi">poderes</i></div></div>
    {cv("e-bolt")}
    {cv("e-c2")}
    <div id="e-rosa" class="full" data-layout-ignore></div>
    <div id="e-ring1" class="a" data-layout-ignore></div><div id="e-ring2" class="a" data-layout-ignore></div>
    {cv("e-c3")}
    <img id="e-an" class="a" src="assets/png/ring.png" width="240" height="240" alt=""/><img id="e-co1" class="a" src="assets/png/heart.png" width="170" height="170" alt=""/><img id="e-co2" class="a" src="assets/png/heart.png" width="120" height="120" alt=""/>
    {chibi("e", ["09", "08"], 700)}
    <div id="e-c" class="a t" style="font-size:64px;font-weight:600">{w("e-q", ["até", "mesmo", "se", "casar", "com", "eles!"])}</div>
""", """
      document.getElementById("e-burst").innerHTML = FX.starSvg("#d8ffee");
      gsap.set("#e-int", { ...center, x: 960, y: 200 });
      [[0, 24.03], [1, 24.29], [2, 24.56]].forEach(([i, t]) => FX.w(tl, "#e-p" + i, S, t, 0.2));
      FX.k(tl, "#e-int", S, [[25.6, { opacity: 1 }], [25.72, { opacity: 0 }]]);
      gsap.set("#e-int", { opacity: 1 });
      // Bola sobe e vira lasca, a lasca vira pilula
      const a = { f0: 386, t0: 24.0, r: 0.85 / 16 };
      FX.pk(tl, "#e-ball", S, a, [[386, { ...center, x: 540, y: 1320, scale: 0.2, scaleX: 0.2, backgroundColor: "#ffffff" }], [387, { x: 520, y: 1340, scale: 0.28, scaleX: 0.28 }], [389, { x: 510, y: 1300, scale: 0.5, scaleX: 0.5 }, "power1.out"], [392, { x: 608, y: 1200, scale: 0.72, scaleX: 0.72 }], [394, { x: 580, y: 1120, scale: 0.65, scaleX: 0.6 }], [396, { x: 551, y: 1060, scale: 0.6, scaleX: 0.45, backgroundColor: "#ffdac8" }], [398, { x: 540, y: 1000, scale: 0.72, scaleX: 0.2, backgroundColor: "#f89665" }], [400, { y: 960, scale: 1.2, scaleX: 0.18, backgroundColor: "#ff5a26", borderRadius: "30px", opacity: 1 }], [400.5, { opacity: 0 }]]);
      gsap.set("#e-pill,#e-plus,#e-gl,#e-wide", { transformPerspective: 1100 });
      const b = { f0: 399, t0: 24.8, r: 1.3 / 27 };
      FX.pk(tl, "#e-pur", S, Object.assign({}, b, { dx: 0, dy: 0 }), [[388, { opacity: 0 }], [402, { opacity: 0.8 }], [412, { opacity: 1 }], [424, { opacity: 0.8 }], [432, { opacity: 0.3 }], [445, { opacity: 0.2 }]]);
      FX.pk(tl, "#e-pill", S, b, [[399, { ...center, x: 540, y: 960, rotationY: 86, scale: 0.8, opacity: 0 }], [400, { opacity: 1 }], [403, { rotationY: 70, scale: 1.05 }], [405, { rotationY: 26, y: 950, scale: 1 }, "power2.out"], [407, { rotationY: -2, scale: 1.05, y: 945, scaleY: 0.72 }, "power2.out"], [410, { rotationY: 0, scale: 1, scaleY: 1, y: 935 }, "power2.out"], [416, { rotation: -1, y: 930, scale: 0.94 }], [418, { rotation: -5 }, "power1.in"], [420, { rotation: -14, x: 530, y: 950 }, "power1.in"], [422, { rotation: -21, scale: 0.84, backgroundColor: "#f7966a" }], [424, { rotation: -22, scale: 0.6, rotationY: 28, backgroundColor: "#fbc2a4" }], [425, { scale: 0.38, rotationY: 40, opacity: 0.9 }], [426, { opacity: 0 }]]);
      const c = { f0: 424, t0: 25.96, r: 0.14 / 8 };
      FX.pk(tl, "#e-plus", S, c, [[424, { ...center, x: 540, y: 930, scale: 0.92, rotation: -12, rotationY: 50, opacity: 0, color: "#ffffff" }], [425, { opacity: 1, rotation: -8, scale: 1.05, rotationY: 30 }], [428, { rotation: 4, rotationY: 44, scale: 0.86 }], [431, { rotation: 6, rotationY: 14, scale: 0.7, color: "#f05d10" }], [432, { opacity: 0 }]]);
      // Vidro com confete sobre "aprender Jutsus"
      const g = { f0: 447, t0: 26.1, r: 1.27 / 51 };
      FX.pk(tl, "#e-gl", S, g, [[447, { ...center, x: 540, y: 950, scale: 0.3, rotation: -8, rotationY: 28, opacity: 0, skewY: 8 }], [448, { opacity: 1, scale: 0.5 }], [451, { scale: 0.9, rotation: 0, rotationY: 8, skewY: 2 }, "power2.out"], [453, { scale: 1.2, skewY: -6, rotationY: -6 }, "power2.out"], [456, { scale: 1.22, skewY: -9, rotation: 2 }], [460, { scale: 1, skewY: -8, rotation: 0 }, "power1.out"], [464, { scale: 0.98, skewY: 0 }], [468, { scale: 1, skewY: 6, rotationY: -8 }], [474, { scale: 1, skewY: 7, rotationY: -6 }], [481, { scale: 1, skewY: 3, rotationY: 8, y: 955 }], [486, { scale: 1, skewY: 0, rotationY: 4, y: 945 }], [489, { scale: 0.95, rotationY: 12, skewX: 2 }], [491, { scale: 0.83, skewX: 3, rotation: 3, rotationY: 25 }, "power1.in"], [493, { scale: 0.54, rotation: 8, rotationX: 22 }, "power1.in"], [495, { scale: 0.12, rotation: 16, rotationY: 40 }, "power2.in"], [497, { scale: 0.06, opacity: 0.9 }], [498, { opacity: 0 }]]);
      const g0 = Object.assign({}, g, { dx: 0, dy: 0 });
      FX.pk(tl, "#e-gb", S, g0, [[452, { backgroundColor: "#ff7c7c", rotation: -8 }], [456, { backgroundColor: "#f28bff", rotation: -9 }], [461, { backgroundColor: "#f55de8", rotation: -5 }], [466, { backgroundColor: "#a56eff", rotation: 3 }], [470, { backgroundColor: "#6f9dff", rotation: 6 }], [474, { backgroundColor: "#62d5ff", rotation: 4 }], [478, { backgroundColor: "#8bf2bf", rotation: 2, color: "#ffffff" }], [482, { backgroundColor: "#c8ffc4", rotation: 0 }], [487, { backgroundColor: "#ffffff", color: "#333333" }]]);
      FX.pk(tl, "#e-burst", S, g, [[451, { ...center, x: 540, y: 880, scale: 0.3, opacity: 0, rotation: 8 }], [453, { scale: 1, opacity: 1 }], [456, { scale: 1.4, opacity: 1 }], [460, { scale: 0.5, opacity: 0.5, y: 860 }], [464, { scale: 0.1, opacity: 0 }]]);
      FX.pk(tl, "#e-lav", S, g0, [[446, { opacity: 0 }], [450, { opacity: 0.7 }], [454, { opacity: 1 }], [461, { opacity: 0.9 }], [468, { opacity: 0 }]]);
      FX.pk(tl, "#e-blu", S, g0, [[458, { opacity: 0 }], [465, { opacity: 1 }], [476, { opacity: 0.5 }], [484, { opacity: 0 }]]);
      FX.clique(tl, "#e-cur", S, [1560, 1200], [1000, 770], [1600, 1250], 26.95, 27.08, 27.2);
      const col = ["#ff5fb2", "#68e6ff", "#ffc65a", "#b777ff", "#61ec8e", "#ff7a7a", "#fff"];
      const C1 = FX.jato(document.getElementById("e-c1"), { seed: 31, n: 260, colors: col, x: 960, y: 1100, spread: 1.9, speed: 2500, t0: 26.08 });
      const C2 = FX.jato(document.getElementById("e-c2"), { seed: 42, n: 110, colors: col, x: 960, y: 1100, spread: 1.6, speed: 2200, t0: 26.14 });
      FX.k(tl, "#e-c1", S, [[26.1, { opacity: 1 }], [27.0, { opacity: 0.6 }], [27.5, { opacity: 0.3 }], [28.4, { opacity: 0 }]]);
      FX.k(tl, "#e-c2", S, [[26.14, { opacity: 0.9 }], [27.0, { opacity: 0.2 }], [27.4, { opacity: 0 }]]);
      // Cartao largo com o olho
      const h = { f0: 497, t0: 27.34, r: 1.08 / 26 };
      FX.pk(tl, "#e-wide", S, h, [[497, { ...center, x: 540, y: 950, scale: 0.08, rotation: 16, rotationX: 34, opacity: 0 }], [498, { opacity: 1 }], [500, { scale: 0.22, rotation: 8, rotationX: 28 }], [502, { scale: 0.48, rotation: 5, rotationX: 14 }, "power1.out"], [504, { scale: 0.96, rotation: -5, rotationX: 0 }, "power2.out"], [506, { scale: 1.1, rotation: -5 }, "power1.out"], [509, { scale: 1.02, rotation: -1 }], [512, { scale: 0.98, rotation: 0.5, y: 975 }, "power1.out"], [516, { scale: 0.92, rotation: 0, y: 950, opacity: 1, filter: "blur(0.5px)" }], [519, { filter: "blur(3px)", opacity: 0.75 }], [522, { scale: 0.8, y: 930, filter: "blur(9px)", opacity: 0.25 }], [523, { opacity: 0 }]]);
      FX.pk(tl, "#e-grn", S, Object.assign({}, h, { dx: 0, dy: 0 }), [[488, { opacity: 0 }], [498, { opacity: 0.4 }], [506, { opacity: 1 }], [513, { opacity: 0.8 }], [522, { opacity: 0 }]]);
      FX.pk(tl, "#e-wi", S, Object.assign({}, h, { dx: 0, dy: 0 }), [[500, { color: "#62d5ff" }], [504, { color: "#38d09a" }], [508, { color: "#ff5a26" }]]);
      const B = FX.bolts(document.getElementById("e-bolt"), [
        { t: 27.55, d: 0.09, c: "#ff5a26", w: 9, pts: [[0, 180], [260, 300], [420, 420]] }, { t: 27.66, d: 0.09, c: "#fff", w: 6, pts: [[1920, 760], [1650, 600], [1500, 520]] }], 8);
      // Casamento: rosa, aneis girando e a narradora
      FX.k(tl, "#e-rosa", S, [[28.38, { opacity: 0 }], [28.46, { opacity: 1 }], [30.2, { opacity: 1 }], [30.33, { opacity: 0.4 }]]);
      FX.k(tl, "#e-ring1", S, [[28.4, { ...center, x: 1650, y: 60, rotation: 0, opacity: 0 }], [28.42, { opacity: 0.8 }], [30.35, { rotation: 90, x: 1590 }]]);
      FX.k(tl, "#e-ring2", S, [[28.4, { ...center, x: 240, y: 1030, rotation: 0, opacity: 0, scale: 0.8 }], [28.42, { opacity: 0.7 }], [30.35, { rotation: -90, x: 300 }]]);
      FX.talk(tl, S, [["e09", 28.42, 29.75], ["e08", 29.75, 30.35]]);
      FX.k(tl, "#e-ch", S, [[28.42, { ...center, x: 960, y: 700, scale: 0.15, rotation: -40, opacity: 0, filter: "blur(10px)" }], [28.46, { opacity: 1 }], [28.68, { y: 470, scale: 1.06, rotation: 4, filter: "blur(0px)" }, "expo.out"], [28.9, { scale: 1, rotation: 0 }, "power2.out"], [30.2, { y: 450, scale: 1.03 }], [30.34, { scale: 0.05, rotation: 60, opacity: 0 }, "power3.in"]]);
      FX.k(tl, "#e-an", S, [[28.5, { ...center, x: 1420, y: 300, scale: 0.1, rotation: -40, opacity: 0 }], [28.75, { scale: 1.1, rotation: 8, opacity: 1 }, "back.out(2)"], [30.2, { y: 270, rotation: -6, scale: 1, opacity: 1 }], [30.34, { opacity: 0 }]]);
      FX.k(tl, "#e-co1", S, [[28.6, { ...center, x: 480, y: 420, scale: 0.1, opacity: 0, rotation: 20 }], [28.85, { scale: 1, opacity: 1, rotation: -8 }, "back.out(2)"], [30.2, { y: 370, rotation: 6, opacity: 1 }], [30.34, { opacity: 0 }]]);
      FX.k(tl, "#e-co2", S, [[28.9, { ...center, x: 1500, y: 680, scale: 0.1, opacity: 0, rotation: -20 }], [29.1, { scale: 1, opacity: 1, rotation: 10 }, "back.out(2)"], [30.2, { y: 630, rotation: -8, opacity: 1 }], [30.34, { opacity: 0 }]]);
      gsap.set("#e-c", { ...center, x: 960, y: 900 });
      [[0, 28.57], [1, 28.78], [2, 29.08], [3, 29.21], [4, 29.54], [5, 29.78]].forEach(([i, t]) => FX.w(tl, "#e-q" + i, S, t, 0.18));
      FX.k(tl, "#e-c", S, [[30.15, { opacity: 1 }], [30.3, { opacity: 0, filter: "blur(8px)" }]]);
      const C3 = FX.jato(document.getElementById("e-c3"), { seed: 3, n: 170, colors: ["#fff", "#ffd0dc", "#ff4d7e", "#ffe6a8"], x: 960, y: 1120, spread: 2, speed: 2300, t0: 28.44 });
      FX.drive(tl, S, 24, 30.35, (t) => { C1(t); C2(t); B(t); C3(t); });
""")

# ---------- F: recorte (mantém a cena, com palco parecido com a referência) ----------
f_html = (C / "f.html").read_text(encoding="utf-8")
if "f-quad" not in f_html:
    canto = '<svg id="f-quad" class="a" width="1920" height="1080" viewBox="0 0 1920 1080" data-layout-ignore><path d="M0 0H1920V1080H0ZM74 56V1024H1846V56Z" fill="#0b0b0d" fill-rule="evenodd"/><path d="M40 20H230L190 74H74V170L40 210ZM1880 20H1690L1730 74H1846V170L1880 210ZM40 1060H230L190 1006H74V910L40 870ZM1880 1060H1690L1730 1006H1846V910L1880 870Z" fill="#c9302c"/></svg>'
    f_html = f_html.replace('<div id="f-c1" class="a">', canto + '\n    <div id="f-c1" class="a">', 1)
    (C / "f.html").write_text(f_html, encoding="utf-8")

# ---------- G: palavras + linha, peça girando, pílula, cartão (Voltz f), azul (Voltz h), digitação (Voltz i) ----------
nums = "".join(f'<div id="g-n{i}" class="ab n">{n}</div>' for i, n in enumerate([7, 13, 3, 20]))
cena("g", f"""
#g-gray {{ background:radial-gradient(ellipse at 50% 42%,#3d3d3d,#161616 58%,#000 88%); }}
#g-grn {{ background:radial-gradient(ellipse at 50% 18%,#1f6a1f,#0a260a 45%,#0000 72%); }}
#g-blue {{ background:radial-gradient(ellipse at 50% 30%,#2f8cff,#14408f 55%,#061436); }}
#g-red {{ background:radial-gradient(ellipse at 50% 50%,#54210a,#000 62%); }}
#g-cal {{ width:520px; height:500px; border-radius:90px; background:radial-gradient(ellipse at 42% 42%,#fff 18%,#cfcfcf 82%,#9c9c9c); color:#6e6e6e; text-align:center; overflow:hidden; }}
#g-cal .d {{ position:absolute; left:0; width:100%; top:30px; color:#e01e45; font-size:80px; font-weight:500; }}
#root .n {{ left:0; width:100%; top:120px; font-size:280px; font-weight:400; line-height:1.1; letter-spacing:-.02em; }}
#g-fl {{ width:620px; height:620px; border-radius:50%; background:radial-gradient(#fff 3%,#ffd59a 14%,#d24a1d55 40%,#0000 68%); mix-blend-mode:screen; }}
#g-pill {{ width:820px; height:210px; border-radius:60px; background:radial-gradient(ellipse at 50% 60%,#fff 42%,#c7c7c7); color:#333; font-size:80px; font-weight:500; display:flex; align-items:center; justify-content:center; white-space:nowrap; letter-spacing:-.02em; }}
#g-tr {{ width:640px; height:760px; border-radius:66px; background:radial-gradient(ellipse at 50% 50%,#fff 38%,#bebebe 82%,#8f8f8f); color:#555; text-align:center; overflow:hidden; }}
#g-ic {{ position:absolute; left:36px; top:36px; width:568px; height:320px; border-radius:34px; background:linear-gradient(135deg,#0f3a2c,#176b4a); display:flex; align-items:center; justify-content:center; gap:10px; }}
#g-ic img {{ width:240px; height:240px; }}
#g-ok {{ position:absolute; left:270px; top:376px; width:100px; height:100px; border-radius:50%; background:#27d832; color:#fff; font-size:62px; font-weight:800; line-height:100px; }}
#g-t1 {{ position:absolute; left:0; width:100%; top:492px; font-size:62px; font-weight:600; }}
#g-t2 {{ position:absolute; left:0; width:100%; top:568px; font-size:36px; color:#777; }}
#g-bar {{ position:absolute; left:70px; top:640px; width:500px; height:32px; border-radius:16px; background:#00000022; overflow:hidden; }}
#g-bi {{ height:100%; background:#27d832; border-radius:16px; transform-origin:0 50%; }}
#g-mis {{ width:820px; height:520px; border-radius:46px; background:linear-gradient(170deg,#101a30,#0a1224); border:4px solid #6fa9ff; overflow:hidden; text-align:center; }}
#g-mt {{ position:absolute; left:0; width:100%; top:44px; font-size:98px; font-weight:700; color:#79b4ff; }}
#g-ms {{ position:absolute; left:0; width:100%; top:164px; font-size:40px; color:#b7c8e8; }}
#g-mb {{ position:absolute; left:110px; top:350px; width:600px; height:110px; border-radius:22px; background:#27b45c; display:flex; align-items:center; justify-content:center; font-size:46px; font-weight:600; white-space:nowrap; }}
#g-dado {{ width:300px; height:300px; }}
#g-dado div {{ left:0; top:0; width:100%; height:100%; display:flex; align-items:center; justify-content:center; font-size:92px; font-weight:800; padding-top:8px; }}
#g-tipo {{ position:absolute; left:0; top:0; font-weight:500; white-space:nowrap; letter-spacing:-.02em; font-size:300px; line-height:1; }}
#g-car {{ width:14px; height:300px; background:{VERDE}; }}
#g-peq {{ font-size:62px; font-weight:500; white-space:nowrap; font-family:"Inter",sans-serif; }}
#root .gl {{ position:absolute; background:#fff; }}
""", f"""
    <div id="g-gray" class="full" data-layout-ignore></div><div id="g-grn" class="full" data-layout-ignore></div>
    <div id="g-blue" class="full" data-layout-ignore></div><div id="g-red" class="full" data-layout-ignore></div>
    {cv("g-dust")}
    {cv("g-c1")}
    <div id="g-s" class="a t" style="font-size:78px;font-weight:500">Além disso,</div>
    <div id="g-s2" class="a t" style="font-size:78px;font-weight:500">Synex possui</div>
    <svg id="g-ln" class="a" width="1920" height="1080" viewBox="0 0 1920 1080" fill="none" stroke="#ffc9a8" stroke-width="7" stroke-linecap="round" data-layout-ignore><path id="g-l1" pathLength="1" d="M520 640C500 560 680 560 900 580S1320 620 1420 590"/><path id="g-l2" pathLength="1" stroke="#fff" d="M980 600C1160 620 1270 570 1300 480 1330 380 1230 260 1120 230 1040 200 960 260 950 300"/></svg>
    <div id="g-fl" class="a" data-layout-ignore></div>
    <div id="g-cal" class="a" data-layout-allow-overflow><div class="d">D20</div>{nums}</div>
    <div id="g-pill" class="a" data-layout-allow-overflow><img src="assets/png/swords.png" alt="" style="width:140px;height:140px;margin-right:18px"/>Combate dinâmico</div>
    {cv("g-bolt")}
    <div id="g-tr" class="a" data-layout-allow-overflow><div id="g-ic"><img src="assets/png/biceps.png" alt=""/><img src="assets/png/trophy.png" alt=""/></div><div id="g-ok">✓</div><div id="g-t1">Treinos</div><div id="g-t2">que realmente te desafiam</div><div id="g-bar"><div id="g-bi"></div></div></div>
    <div id="g-mis" class="a" data-layout-allow-overflow><img src="assets/png/scroll.png" alt="" style="position:absolute;left:40px;top:34px;width:130px;height:130px"/><img src="assets/png/map.png" alt="" style="position:absolute;right:40px;top:34px;width:130px;height:130px"/><div id="g-mt">Missões</div><div id="g-ms">funcionam exatamente como</div><div id="g-mb">um RPG de mesa</div></div>
    <div id="g-dado" class="a" data-layout-allow-overflow><svg viewBox="-100 -100 200 200" width="100%" height="100%" style="overflow:visible"><path d="M0-92 80-46V46L0 92-80 46V-46Z" fill="{CORAL}" stroke="#fff" stroke-width="8" stroke-linejoin="round"/><path d="M0-92 46 22H-46ZM-80-46-46 22-80 46M80-46 46 22 80 46M-46 22 0 92 46 22" fill="none" stroke="#ffffff88" stroke-width="4"/></svg><div id="g-v0" class="ab">9</div><div id="g-v1" class="ab">14</div><div id="g-v2" class="ab">2</div><div id="g-v3" class="ab">20</div></div>
    <div id="g-cur" class="a">{CURSOR}</div>
    {cv("g-c2")}
    <div id="g-mask" class="a" style="width:1500px;height:1080px;overflow:hidden" data-layout-ignore><div id="g-tipo" data-layout-allow-overflow data-layout-bleed="true">vários outros sistemas inovadores</div></div>
    <div id="g-car" class="a" data-layout-ignore></div>
    <div id="g-peq" class="a">vários outros sistemas inovadores..</div>
    <div id="g-g1" class="gl" style="left:120px;top:400px;width:1680px;height:300px" data-layout-ignore></div>
    <div id="g-g2" class="gl" style="left:0;top:90px;width:1300px;height:300px" data-layout-ignore></div>
    <div id="g-g3" class="gl" style="left:400px;top:690px;width:1520px;height:320px" data-layout-ignore></div>
""", """
      // Duas frases se encontram sobre a linha (Voltz "Sendo sorteios")
      const a = { f0: 525, t0: 40.0, r: 1.72 / 22, dx: 420, dy: -420 };
      FX.pk(tl, "#g-s", S, a, [[525, { ...center, x: 300, y: 1290, opacity: 0, filter: "blur(8px)", color: "#c0541c" }], [527, { y: 1148, opacity: 0.9, filter: "blur(1px)", color: "#ee8a56" }], [529, { y: 1085, opacity: 1, filter: "blur(0px)", color: "#fbb68c" }], [531, { y: 1045 }], [535, { y: 1000 }], [538, { y: 989, color: "#d0d0d0" }], [540, { opacity: 0.65, color: "#a0a0a0" }], [546, { opacity: 0.2, filter: "blur(5px)" }], [547, { opacity: 0 }]]);
      FX.pk(tl, "#g-s2", S, a, [[527, { ...center, x: 790, y: 1420, opacity: 0, filter: "blur(7px)", color: "#c0541c" }], [531, { opacity: 0 }], [533, { y: 1188, opacity: 0.9, filter: "blur(1px)" }], [535, { y: 1102, opacity: 1, filter: "blur(0px)" }], [538, { y: 1046, color: "#ffd9c2" }], [541, { y: 1000, color: "#ffffff" }], [545, { y: 985, opacity: 0.8 }], [547, { opacity: 0 }]]);
      const a0 = Object.assign({}, a, { dx: 0, dy: 0 });
      FX.pk(tl, "#g-l1", S, a0, [[526, { strokeDasharray: 1, strokeDashoffset: 1 }], [530, { strokeDashoffset: 0.4 }], [536, { strokeDashoffset: -0.3 }], [541, { strokeDashoffset: -0.62, opacity: 1, stroke: "#fff" }], [543, { strokeDashoffset: -0.68, opacity: 0 }]]);
      FX.pk(tl, "#g-l2", S, a0, [[542, { strokeDasharray: 1, strokeDashoffset: 1, opacity: 0 }], [543, { strokeDashoffset: 0.75, opacity: 1 }], [546, { strokeDashoffset: 0.15 }], [548, { strokeDashoffset: -0.25 }], [550, { strokeDashoffset: -0.95 }], [550.5, { opacity: 0 }]]);
      // Dado branco gira e troca o numero (Voltz calendario)
      gsap.set("#g-cal,#g-pill,#g-tr,#g-mis", { transformPerspective: 1100 });
      const b = { f0: 547, t0: 41.72, r: 0.68 / 21 };
      FX.pk(tl, "#g-gray", S, Object.assign({}, b, { dx: 0, dy: 0 }), [[547, { opacity: 0 }], [550, { opacity: 0.6 }], [566, { opacity: 0.85 }], [572, { opacity: 1 }], [590, { opacity: 1 }]]);
      FX.pk(tl, "#g-cal", S, b, [[547, { ...center, x: 540, y: 620, scale: 0.05, rotation: -50, opacity: 0 }], [548, { opacity: 1 }], [549, { scale: 0.28, rotation: -30, y: 640 }], [550, { x: 300, y: 790, scale: 0.46, rotation: 90, filter: "blur(1px)" }, "power1.out"], [551, { x: 400, y: 800, scale: 0.75, rotation: 60, filter: "blur(3px)" }, "power1.out"], [552, { x: 500, y: 860, scale: 1.1, rotation: 30, filter: "blur(4px)" }, "power1.out"], [553, { x: 520, y: 900, scale: 1.2, rotation: 0, filter: "blur(4px)" }], [555, { x: 580, y: 880, scale: 1.05, rotation: -22, filter: "blur(2px)" }], [557, { x: 540, y: 890, scale: 0.92, rotation: -42, filter: "blur(1px)" }], [559, { x: 560, y: 895, scale: 0.88, rotation: -30 }], [561, { x: 540, y: 930, scale: 0.84, rotation: -3, filter: "blur(1px)" }, "power1.out"], [563, { x: 540, y: 950, scale: 0.8, rotation: 0, filter: "blur(0px)" }], [565, { scaleY: 0.76, scale: 0.85, skewY: 1 }], [566, { scaleY: 0.5, y: 950, scale: 0.9 }], [567, { scaleY: 0.26, y: 1010, scale: 0.92 }], [568, { opacity: 0 }]]);
      FX.swap(tl, ["#g-n0", "#g-n1", "#g-n2", "#g-n3"], S, 41.72, 0.11);
      FX.pk(tl, "#g-fl", S, b, [[548, { ...center, x: 560, y: 760, scale: 0.15, opacity: 0 }], [550, { x: 500, y: 830, scale: 0.8, opacity: 1 }], [553, { x: 820, y: 800, scale: 1.2 }], [556, { x: 660, y: 780, scale: 1 }], [560, { x: 760, y: 790, scale: 0.65, opacity: 0.8 }], [564, { opacity: 0 }]]);
      const c = { f0: 567, t0: 42.38, r: 0.62 / 14 };
      FX.pk(tl, "#g-pill", S, c, [[567, { ...center, x: 540, y: 960, scaleX: 1.3, scaleY: 0.18, rotation: 3, opacity: 0, color: "#555555" }], [568, { opacity: 1 }], [571, { scaleX: 1, scaleY: 0.38, y: 950, rotation: 1 }], [573, { scaleX: 0.9, scaleY: 0.88, rotation: 0 }, "power2.out"], [576, { scaleX: 0.95, scaleY: 0.9, color: "#222222" }], [579, { scaleX: 1, y: 985, color: "#aaaaaa" }], [581, { scaleX: 1, scaleY: 0.92, y: 985, opacity: 1 }], [581.5, { opacity: 0 }]]);
      // Cartao branco de treino
      const d = { f0: 581, t0: 43.0, r: 1.88 / 14.5 };
      FX.pk(tl, "#g-tr", S, d, [[581, { ...center, x: 540, y: 985, scaleX: 0.68, scaleY: 0.2, opacity: 0 }], [581.5, { opacity: 1, scaleX: 0.72, scaleY: 0.42, y: 970 }], [582, { scaleX: 0.78, scaleY: 0.62, y: 975 }, "power1.out"], [582.5, { scaleX: 0.86, scaleY: 0.82, y: 965 }, "power1.out"], [583, { scaleX: 1.04, scaleY: 1, y: 960, rotation: 1 }, "power1.out"], [589, { scaleX: 1.02, scaleY: 1, y: 955, rotation: 3.5 }], [592, { scaleX: 1, scaleY: 1, y: 950, rotation: 6 }], [594, { scale: 0.9, rotation: 40, filter: "blur(4px)", y: 945, backgroundColor: "#e8c8ee" }, "power1.in"], [595.5, { opacity: 0 }]]);
      FX.k(tl, "#g-bi", S, [[43.2, { scaleX: 0.04 }], [44.1, { scaleX: 0.86 }, "power2.out"], [44.22, { scaleX: 0.55 }, "power3.in"], [44.75, { scaleX: 0.92 }, "power2.out"]]);
      FX.k(tl, "#g-grn", S, [[43.0, { opacity: 0 }], [43.3, { opacity: 1 }], [44.8, { opacity: 0.6 }], [44.9, { opacity: 0 }]]);
      FX.k(tl, "#g-gray", S, [[44.78, { opacity: 1 }], [44.92, { opacity: 0 }]]);
      // Azul com confete: missoes
      FX.k(tl, "#g-blue", S, [[44.7, { opacity: 0 }], [44.71, { opacity: 1 }], [48.0, { opacity: 1 }], [48.2, { opacity: 0 }]]);
      FX.iris(tl, "#g-blue", S, 44.72, 0.2, 50, 50);
      FX.k(tl, "#g-mis", S, [[44.88, { ...center, x: 960, y: 1300, scale: 0.34, rotationY: 74, rotation: -2, filter: "blur(10px)", opacity: 0.2 }], [45.05, { y: 900, scale: 0.72, rotationY: 28, opacity: 0.9, filter: "blur(4px)" }, "power2.out"], [45.2, { y: 660, scale: 0.9, rotationY: -10, opacity: 1, filter: "blur(1px)" }, "power2.out"], [45.45, { y: 570, scale: 1, rotationY: -2, rotation: -1.5, filter: "blur(0px)" }, "power2.out"], [47.9, { y: 550, x: 800, rotationY: 6, rotation: 0 }], [48.08, { scale: 0.7, filter: "blur(5px)" }, "power1.in"], [48.22, { scale: 0.05, opacity: 0, filter: "blur(10px)" }, "power2.in"]]);
      FX.k(tl, "#g-mb", S, [[46.17, { scale: 1, backgroundColor: "#27b45c" }], [46.27, { scale: 1.12, backgroundColor: "#ffc34d", color: "#222222" }, "back.out(2)"], [46.47, { scale: 1 }]]);
      FX.clique(tl, "#g-cur", S, [1560, 1200], [930, 720], [1600, 1250], 46.0, 46.15, 46.4);
      FX.k(tl, "#g-dado", S, [[46.2, { ...center, x: 2100, y: -200, rotation: 0, opacity: 1 }], [47.25, { x: 1540, y: 560, rotation: 1080 }, "bounce.out"], [47.95, { rotation: 1095, scale: 1.08 }], [48.2, { scale: 0.05, opacity: 0 }, "power3.in"]]);
      FX.swap(tl, ["#g-v0", "#g-v1", "#g-v2", "#g-v3"], S, 46.2, 0.33);
      const col = ["#ffffff", "#79b4ff", "#ffc34d", "#2ee89f", "#ff5a26"];
      const C1 = FX.jato(document.getElementById("g-c1"), { seed: 17, n: 240, colors: col, x: 960, y: 1120, spread: 1.9, speed: 2600, t0: 44.92 });
      const C2 = FX.jato(document.getElementById("g-c2"), { seed: 27, n: 90, colors: col, x: 960, y: 1120, spread: 1.6, speed: 2200, t0: 47.25 });
      FX.k(tl, "#g-c1", S, [[44.9, { opacity: 1 }], [47.8, { opacity: 0.5 }], [48.2, { opacity: 0 }]]);
      FX.k(tl, "#g-c2", S, [[47.25, { opacity: 1 }], [47.9, { opacity: 0.7 }], [48.2, { opacity: 0 }]]);
      // Digitacao gigante: a camera acompanha (Voltz i)
      FX.k(tl, "#g-red", S, [[48.14, { opacity: 0 }], [48.3, { opacity: 0.7 }], [50.0, { opacity: 0.3 }], [50.1, { opacity: 0 }]]);
      FX.k(tl, "#g-tipo", S, [[48.3, { x: 1500, y: 390, opacity: 1 }], [49.8, { x: -3200 }], [49.95, { x: -3300 }], [49.97, { opacity: 0 }]]);
      FX.k(tl, "#g-car", S, [[48.28, { x: 1500, y: 390, opacity: 0 }], [48.3, { opacity: 1 }], [49.95, { opacity: 1 }], [49.97, { opacity: 0 }]]);
      FX.k(tl, "#g-peq", S, [[49.95, { ...center, x: 960, y: 540, opacity: 0, color: "#46f04a" }], [49.97, { opacity: 1 }], [50.2, { color: "#ffffff" }], [50.36, { y: 548, filter: "blur(1px)" }], [50.42, { opacity: 0.7 }], [50.48, { opacity: 0.25, scaleY: 1.3, filter: "blur(3px)", y: 525 }], [50.54, { opacity: 0 }]]);
      FX.k(tl, "#g-g1", S, [[50.41, { opacity: 0 }], [50.44, { opacity: 1 }], [50.47, { opacity: 0 }]]);
      FX.k(tl, "#g-g2", S, [[50.44, { opacity: 0 }], [50.47, { opacity: 1 }], [50.51, { opacity: 0 }]]);
      FX.k(tl, "#g-g3", S, [[50.5, { opacity: 0 }], [50.52, { opacity: 1 }], [50.55, { opacity: 0 }]]);
      const D = FX.dust(document.getElementById("g-dust"), { seed: 7, n: 90, color: "#ffffff", alpha: 0.5 });
      const B = FX.bolts(document.getElementById("g-bolt"), [
        { t: 42.42, d: 0.1, c: "#ff5a26", w: 10, pts: [[0, 150], [420, 300], [620, 460]] }, { t: 42.5, d: 0.1, c: "#fff", w: 6, pts: [[1920, 800], [1560, 640], [1340, 560]] },
        { t: 42.68, d: 0.1, c: "#ff5a26", w: 8, pts: [[1800, 0], [1500, 260], [1360, 440]] }], 21);
      FX.drive(tl, S, 40, 50.55, (t) => { C1(t); C2(t); D(t); B(t); });
""")

# ---------- H: final (Voltz j) ----------
letras = "".join(f'<span id="h-l{i}">{c}</span>' for i, c in enumerate("Shinobi"))
letras2 = "".join(f'<span id="h-m{i}" class="co">{c}</span>' for i, c in enumerate("Synex"))
cena("h", f"""
#h-g {{ background:linear-gradient(115deg,#000 42%,#2a1004); }}
#h-nome span + span {{ margin-left:0; }}
#h-nome {{ font-size:160px; font-weight:600; letter-spacing:-.03em; }}
#h-plus {{ font-size:64px; color:{CORAL}; font-weight:600; }}
""", f"""
    <div id="h-g" class="full" data-layout-ignore></div>
    {cv("h-conf")}
    <div id="h-t0" class="a t" style="font-size:80px;font-weight:600">{w("h-p", ["Mas", "a", "próxima", "inovação"])}</div>
    <div id="h-t1" class="a t" style="font-size:80px;font-weight:600">será <span class="co" id="h-v" style="font-size:150px;font-weight:800">você</span></div>
    <div id="h-t2" class="a t" style="font-size:60px;font-weight:500">{w("h-q", ["que", "vai", "fazer", "nessa", "história"], 0, {4: "co"})}</div>
    {chibi("h", ["02"], 640)}
    <div id="h-t3" class="a t" style="font-size:66px;font-weight:500;font-family:'Inter',sans-serif">seja bem-vindo ao</div>
    <div id="h-nome" class="a t">{letras}<span style="width:.28em"></span>{letras2}</div>
    <div id="h-plus" class="a">✦</div>
""", """
      FX.k(tl, "#h-g", S, [[50.55, { opacity: 0 }], [51.4, { opacity: 0.6 }], [52.2, { opacity: 1 }], [53.82, { opacity: 0.4 }], [55.0, { opacity: 0 }]]);
      gsap.set("#h-t0", { ...center, x: 960, y: 540 });
      [[0, 50.6], [1, 50.82], [2, 50.91], [3, 51.29]].forEach(([i, t]) => FX.w(tl, "#h-p" + i, S, t, 0.2));
      FX.k(tl, "#h-t0", S, [[51.9, { y: 540, opacity: 1, filter: "blur(0px)" }], [51.98, { y: 515, filter: "blur(2px)", opacity: 0.8 }], [52.05, { y: 480, filter: "blur(5px)", opacity: 0.5 }], [52.12, { y: 450, filter: "blur(7px)", opacity: 0 }]]);
      FX.k(tl, "#h-t1", S, [[51.95, { ...center, x: 960, y: 500, opacity: 0, filter: "blur(6px)" }], [52.05, { opacity: 1, filter: "blur(0px)" }], [53.65, { y: 480 }], [53.8, { opacity: 0, y: 440, filter: "blur(6px)" }]]);
      FX.hit(tl, "#h-v", S, 52.22, { from: 2, dur: 0.26, blur: 22 });
      gsap.set("#h-t2", { ...center, x: 960, y: 660 });
      [[0, 52.6], [1, 52.71], [2, 52.84], [3, 53.1], [4, 53.29]].forEach(([i, t]) => FX.w(tl, "#h-q" + i, S, t, 0.16));
      FX.k(tl, "#h-t2", S, [[53.65, { opacity: 1 }], [53.8, { opacity: 0, filter: "blur(6px)" }]]);
      FX.talk(tl, S, [["h02", 53.82, 55.0]]);
      FX.k(tl, "#h-ch", S, [[53.82, { ...center, x: 960, y: 700, scale: 0.2, opacity: 0, filter: "blur(10px)" }], [53.86, { opacity: 1 }], [54.08, { y: 440, scale: 1, filter: "blur(0px)" }, "expo.out"], [54.72, { y: 425, rotation: 0 }], [54.8, { rotation: -14 }], [54.88, { rotation: -46, scale: 0.75, filter: "blur(2px)" }, "power1.in"], [54.96, { rotation: -100, scale: 0.4, x: 1020, y: 380 }], [55.04, { rotation: -150, scale: 0.08, x: 1120, y: 320, opacity: 0 }]]);
      FX.k(tl, "#h-t3", S, [[53.86, { ...center, x: 960, y: 860, opacity: 0, filter: "blur(5px)" }], [54.02, { opacity: 1, filter: "blur(0px)", y: 840 }, "power1.out"], [54.78, { rotation: 0 }], [54.86, { rotation: -14 }], [54.96, { rotation: -50, scale: 0.5, y: 760, opacity: 0.6 }, "power1.in"], [55.02, { opacity: 0 }]]);
      gsap.set("#h-nome", { ...center, x: 960, y: 530 });
      "0123456".split("").forEach((c, i) => FX.k(tl, "#h-l" + i, S, [[55.07 + i * 0.045, { opacity: 0, y: 34, color: "#ffffff", filter: "blur(6px)" }], [55.2 + i * 0.045, { opacity: 1, y: 0, filter: "blur(0px)" }, "power2.out"]]));
      "01234".split("").forEach((c, i) => FX.k(tl, "#h-m" + i, S, [[55.5 + i * 0.05, { opacity: 0, y: 34, color: "#ffffff", filter: "blur(6px)" }], [55.64 + i * 0.05, { opacity: 1, y: 0, color: "#ff5a26", filter: "blur(0px)" }, "power2.out"]]));
      FX.k(tl, "#h-nome", S, [[55.05, { scale: 1 }], [57.7, { scale: 1.05, opacity: 1, filter: "blur(0px)" }], [58.3, { opacity: 0, filter: "blur(8px)" }]]);
      FX.k(tl, "#h-plus", S, [[56.0, { ...center, x: 1540, y: 455, scale: 0.2, opacity: 0, rotation: -30 }], [56.12, { scale: 1, opacity: 1, rotation: 0 }, "back.out(2)"], [57.7, { rotation: 40, opacity: 1 }], [58.2, { opacity: 0 }]]);
      const F = FX.jato(document.getElementById("h-conf"), { seed: 5, n: 230, colors: ["#d9540f", "#ff6a2a", "#b8430a", "#ffffff"], x: 960, y: 1130, spread: 1.6, speed: 2500, t0: 55.5 });
      FX.drive(tl, S, 55, 58.6, (t) => F(t));
      FX.k(tl, "#h-conf", S, [[55.5, { opacity: 1 }], [57, { opacity: 0.7 }], [58.2, { opacity: 0 }]]);
""")

# ---------- Som e raiz ----------
efeitos = [("woosh", t) for t in (1.05, 4.95, 9.34, 12.2, 13.5, 15.5, 24.8, 26.1, 27.36, 28.42, 30.35, 41.72, 43.0, 44.88, 48.3, 53.82)]
efeitos += [("impacto", t) for t in (9.97, 26.16, 42.42, 52.22, 55.5)]
efeitos += [("pop", t) for t in (5.15, 5.5, 5.9, 18.54, 19.5, 20.14, 21.2, 22.06, 25.1, 36.92, 37.26, 37.1, 39.5, 47.25)]
efeitos += [("clique", t) for t in (9.69, 27.08, 31.18, 34.55, 36.72, 37.05, 38.0, 46.15)]
efeitos += [("facada", 38.1), ("facada", 38.44)]
PICO = {"woosh": 0.755, "impacto": 0.031, "pop": 0.283, "clique": 0.1, "facada": 0.14}
TAM = {"woosh": 2.62, "impacto": 2.0, "pop": 0.34, "clique": 0.26, "facada": 0.6}
VOL = {"woosh": 0.34, "impacto": 0.55, "pop": 0.42, "clique": 0.6, "facada": 0.55}
sons = [f'      <audio id="sfx{i}" src="assets/sfx/{n}.mp3" data-start="{max(T(t) + 0.033 - PICO[n], 0):.3f}" data-duration="{TAM[n]}" data-volume="{VOL[n]}" data-track-index="{20 + i % 8}"></audio>'
        for i, (n, t) in enumerate(sorted(efeitos, key=lambda e: e[1]))]
hosts = "\n".join(
    f'      <div id="{c}" data-composition-id="{c}" data-composition-src="compositions/{c}.html" data-start="{T(a):.3f}" data-duration="{T(b) - T(a):.3f}" data-track-index="1" data-track-kind="graphics" data-width="1920" data-height="1080"></div>'
    for c, a, b in CENAS)
(RAIZ / "index.html").write_text(f"""<!doctype html>
<html lang="pt-BR" data-resolution="landscape">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <script src="assets/words.js"></script>
    <script src="assets/fx.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: #000; }}
      #root {{ width: 100%; height: 100%; background: #000; font-family: "Outfit", sans-serif; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{T(DUR):.3f}" data-width="1920" data-height="1080">
      <audio id="narracao" src="assets/audio/narracao.mp3" data-start="0" data-duration="{NOVA_P[-1][chr(101)] + 0.1:.2f}" data-volume="1" data-track-index="10"></audio>
{chr(10).join(sons)}
{hosts}
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
""", encoding="utf-8")
print("ok", len(sons))
