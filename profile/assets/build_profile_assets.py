#!/usr/bin/env python3
"""Generate the Grethel Labs GitHub profile assets (dark + light) from the brand-kit master paths.

Usage: python3 build_profile_assets.py <brand-kit/svg/master-paths.json> <out-dir>
Only needs the Python standard library.
"""
import json, os, random, sys

MASTER, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
M = json.load(open(MASTER))
MARK_BASE = M["mark"]["base_path"]
MARK_ACCENT = M["mark"]["accent_path"]
WORD = M["wordmark"]["path"]

SANS = "ui-sans-serif, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"

THEMES = {
    "dark": dict(
        canvas="#111827", surface="#192231", raised="#202C3D", subtle="#151E2C",
        text="#F7F8FA", text2="#B6C2D1", muted="#8DA0B8", border="#334155", border2="#4C5E76",
        brand="#2DB8A8", accent="#5CE0CC", accent_subtle="#143A3B", mark="#F7F8FA",
        ok="#3DD68C", warn="#FFCA16", info="#70B8FF", kw="#BAA7FF", danger="#FF9592",
        glow=0.30, grid=0.55,
    ),
    "light": dict(
        canvas="#F7F8FA", surface="#FFFFFF", raised="#FFFFFF", subtle="#F0F3F6",
        text="#111827", text2="#526173", muted="#526173", border="#D4DAE2", border2="#B3BFCD",
        brand="#2DB8A8", accent="#0B6E63", accent_subtle="#E5F6F2", mark="#111827",
        ok="#1A734B", warn="#915500", info="#0B63B6", kw="#6550B9", danger="#B8242A",
        glow=0.22, grid=0.9,
    ),
}


def svg(w, h, title, desc, body, style=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d" fill="none">
<title id="t">{title}</title>
<desc id="d">{desc}</desc>
<style>
text {{ font-family: {SANS}; }}
.mono {{ font-family: {MONO}; }}
{style}
@media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
</style>
{body}
</svg>
'''


def mark(t, x, y, size, color=None, accent=None):
    s = size / 600
    return (f'<g transform="translate({x} {y}) scale({s:.6f})">'
            f'<path d="{MARK_BASE}" fill="{color or t["mark"]}"/>'
            f'<path d="{MARK_ACCENT}" fill="{accent or t["brand"]}"/></g>')


def wordmark(t, x, y, width, color=None):
    s = width / 951
    return f'<g transform="translate({x} {y}) scale({s:.6f})"><path d="{WORD}" fill="{color or t["mark"]}" fill-rule="{M["wordmark"].get("fill_rule", "nonzero")}"/></g>'


def grid_defs(t, w, h, pid="grid", step=40, fade=True):
    return f'''<defs>
<pattern id="{pid}" width="{step}" height="{step}" patternUnits="userSpaceOnUse">
<path d="M {step} 0 L 0 0 0 {step}" stroke="{t['border']}" stroke-width="1" opacity="{t['grid']}"/>
</pattern>
<pattern id="{pid}-major" width="{step*4}" height="{step*4}" patternUnits="userSpaceOnUse">
<path d="M {step*4} 0 L 0 0 0 {step*4}" stroke="{t['border2']}" stroke-width="1" opacity="{t['grid']*0.7:.2f}"/>
</pattern>
<radialGradient id="{pid}-fade" cx="50%" cy="45%" r="70%">
<stop offset="0" stop-color="#fff" stop-opacity="1"/><stop offset="0.75" stop-color="#fff" stop-opacity="0.35"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
</radialGradient>
<mask id="{pid}-mask"><rect width="{w}" height="{h}" fill="url(#{pid}-fade)"/></mask>
</defs>
<g mask="url(#{pid}-mask)"><rect width="{w}" height="{h}" fill="url(#{pid})"/><rect width="{w}" height="{h}" fill="url(#{pid}-major)"/></g>'''


def frame(t, w, h, r=24):
    return (f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="{r}" fill="{t["canvas"]}" stroke="{t["border"]}"/>')


def sketch_rect(x, y, w, h, stroke, fill, seed, sw=2.2):
    rnd = random.Random(seed)
    j = lambda: rnd.uniform(-2.2, 2.2)
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}"/>'
    for _ in range(2):
        pts = [(x + j(), y + j()), (x + w + j(), y + j()), (x + w + j(), y + h + j()), (x + j(), y + h + j())]
        d = f"M {pts[0][0]:.1f} {pts[0][1]:.1f} "
        for (ax, ay), (bx, by) in zip(pts, pts[1:] + pts[:1]):
            mx, my = (ax + bx) / 2 + j(), (ay + by) / 2 + j()
            d += f"Q {mx:.1f} {my:.1f} {bx:.1f} {by:.1f} "
        out += f'<path d="{d}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" fill="none"/>'
    return out


def sketch_line(x1, y1, x2, y2, stroke, seed, sw=2.2, arrow=True):
    rnd = random.Random(seed)
    out = ""
    for _ in range(2):
        mx = (x1 + x2) / 2 + rnd.uniform(-3, 3)
        my = (y1 + y2) / 2 + rnd.uniform(-3, 3)
        out += f'<path d="M {x1+rnd.uniform(-1,1):.1f} {y1+rnd.uniform(-1,1):.1f} Q {mx:.1f} {my:.1f} {x2:.1f} {y2:.1f}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" fill="none"/>'
    if arrow:
        import math
        a = math.atan2(y2 - y1, x2 - x1)
        for da in (2.6, -2.6):
            out += f'<path d="M {x2:.1f} {y2:.1f} L {x2+12*math.cos(a+da):.1f} {y2+12*math.sin(a+da):.1f}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round"/>'
    return out


# ---------------------------------------------------------------- hero
def hero(mode):
    t = THEMES[mode]
    W, H = 1280, 520
    ms, mx, my = 330, 96, 92          # mark size / position
    s = ms / 600
    bubbles = ""
    rnd = random.Random(7)
    for i in range(7):
        bx = mx + (300 + rnd.uniform(-14, 26)) * s
        r = rnd.uniform(4, 9)
        dur = rnd.uniform(3.8, 5.6)
        delay = -i * dur / 7
        bubbles += (f'<circle class="b" cx="{bx:.1f}" cy="{my + 330*s:.1f}" r="{r:.1f}" '
                    f'style="animation-duration:{dur:.2f}s;animation-delay:{delay:.2f}s"/>')
    style = f"""
.b {{ fill: {t['brand']}; opacity: 0; animation: rise linear infinite; transform-box: fill-box; }}
@keyframes rise {{ 0% {{ transform: translateY(0) scale(.6); opacity: 0 }} 12% {{ opacity: .9 }} 70% {{ opacity: .55 }} 100% {{ transform: translateY(-{(330-40)*s:.0f}px) scale(1.15); opacity: 0 }} }}
.cursor {{ animation: blink 1.1s steps(1) infinite; }}
@keyframes blink {{ 50% {{ opacity: 0 }} }}
.scan {{ animation: scan 6s ease-in-out infinite; }}
@keyframes scan {{ 0% {{ transform: translateX(-420px) }} 100% {{ transform: translateX({W}px) }} }}
.glow {{ animation: pulse 5s ease-in-out infinite; transform-origin: {mx+ms/2}px {my+ms/2}px; }}
@keyframes pulse {{ 50% {{ opacity: .55; transform: scale(1.06) }} }}
"""
    tx = 520
    chips = ""
    cx = tx
    for label in ["Open source", "Dev tools", "Diagrams", "Self-hosted", "Experiments"]:
        w = 22 + len(label) * 9.4
        chips += (f'<rect x="{cx}" y="414" width="{w:.0f}" height="34" rx="17" fill="{t["accent_subtle"]}" stroke="{t["brand"]}" stroke-opacity=".45"/>'
                  f'<text x="{cx + w/2:.1f}" y="436" text-anchor="middle" font-size="15" font-weight="600" fill="{t["accent"]}">{label}</text>')
        cx += w + 10
    body = f"""
<defs>
<clipPath id="c"><rect width="{W}" height="{H}" rx="28"/></clipPath>
<radialGradient id="g" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{t['brand']}" stop-opacity="{t['glow']}"/><stop offset="1" stop-color="{t['brand']}" stop-opacity="0"/></radialGradient>
<linearGradient id="s" x1="0" x2="1"><stop offset="0" stop-color="{t['brand']}" stop-opacity="0"/><stop offset=".5" stop-color="{t['brand']}"/><stop offset="1" stop-color="{t['brand']}" stop-opacity="0"/></linearGradient>
</defs>
<g clip-path="url(#c)">
<rect width="{W}" height="{H}" fill="{t['canvas']}"/>
{grid_defs(t, W, H, "hg")}
<circle class="glow" cx="{mx+ms/2}" cy="{my+ms/2+20}" r="300" fill="url(#g)"/>
<rect class="scan" x="0" y="0" width="420" height="3" fill="url(#s)"/>
{mark(t, mx, my, ms)}
{bubbles}
{wordmark(t, tx, 118, 640)}
<text x="{tx}" y="262" font-size="40" font-weight="700" fill="{t['text']}" letter-spacing="-0.5">Open-source tools</text>
<text x="{tx}" y="312" font-size="40" font-weight="700" fill="{t['text']}" letter-spacing="-0.5">and <tspan fill="{t['accent']}">experiments.</tspan></text>
<text class="mono" x="{tx}" y="372" font-size="19" fill="{t['muted']}"><tspan fill="{t['accent']}">~/lab</tspan> $ ls  <tspan fill="{t['text2']}">tools/  experiments/  ideas/</tspan><tspan class="cursor" fill="{t['accent']}"> ▌</tspan></text>
{chips}
</g>
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="28" stroke="{t['border']}"/>
"""
    return svg(W, H, "Grethel Labs", "Grethel Labs: a collection of open-source tools and experiments. Animated flask logo with rising bubbles.", body, style)


# ---------------------------------------------------------------- project cards
def card_excaliplant(mode):
    t = THEMES[mode]
    W, H = 640, 400
    code = [
        ("@startuml", t["kw"]),
        ("actor User", t["text2"]),
        ("User -> API : request", t["text2"]),
        ("API -> DB : query", t["text2"]),
        ("DB --> API : rows", t["text2"]),
        ("@enduml", t["kw"]),
    ]
    lines = "".join(f'<text class="mono" x="54" y="{150 + i*26}" font-size="15" fill="{c}">{l}</text>' for i, (l, c) in enumerate(code))
    sk = t["text"]
    # sketchy diagram on the right
    dia = (sketch_rect(400, 116, 84, 40, sk, t["accent_subtle"], 1) +
           f'<text x="442" y="142" text-anchor="middle" font-size="15" font-weight="600" fill="{t["text"]}">User</text>' +
           sketch_rect(510, 196, 84, 40, sk, t["surface"], 2) +
           f'<text x="552" y="222" text-anchor="middle" font-size="15" font-weight="600" fill="{t["text"]}">API</text>' +
           sketch_rect(400, 270, 84, 40, sk, t["surface"], 3) +
           f'<text x="442" y="296" text-anchor="middle" font-size="15" font-weight="600" fill="{t["text"]}">DB</text>' +
           sketch_line(474, 158, 520, 194, t["brand"], 4) +
           sketch_line(512, 236, 478, 268, t["brand"], 5))
    style = """
.draw { stroke-dasharray: 60 14; animation: flow 1.6s linear infinite; }
@keyframes flow { to { stroke-dashoffset: -74 } }
.pop { animation: pop 4s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }
@keyframes pop { 0%,100% { transform: rotate(-1.2deg) } 50% { transform: rotate(1.2deg) } }
"""
    body = f"""
{frame(t, W, H)}
<rect x="32" y="100" width="300" height="196" rx="14" fill="{t['subtle']}" stroke="{t['border']}"/>
<circle cx="52" cy="118" r="0"/>
<text class="mono" x="54" y="124" font-size="12" fill="{t['muted']}">sequence.puml</text>
{lines}
<path class="draw" d="M 338 206 L 386 206" stroke="{t['brand']}" stroke-width="3" stroke-linecap="round"/>
<path d="M 378 198 L 388 206 L 378 214" stroke="{t['brand']}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
<g class="pop">{dia}</g>
<text x="32" y="64" font-size="30" font-weight="800" fill="{t['text']}" letter-spacing="-0.4">excaliplant</text>
<rect x="210" y="40" width="186" height="30" rx="15" fill="{t['accent_subtle']}"/>
<text x="303" y="61" text-anchor="middle" font-size="14" font-weight="600" fill="{t['accent']}">PlantUML → Excalidraw</text>
<text x="32" y="340" font-size="17" fill="{t['text2']}">Turn PlantUML into editable Excalidraw diagrams.</text>
<text x="32" y="366" font-size="17" fill="{t['text2']}">Keep sketching, then export to <tspan fill="{t['text']}" font-weight="600">SVG</tspan> or <tspan fill="{t['text']}" font-weight="600">PNG</tspan>.</text>
"""
    return svg(W, H, "excaliplant", "excaliplant turns PlantUML into editable Excalidraw diagrams and exports SVG or PNG.", body, style)


def card_deploy(mode):
    t = THEMES[mode]
    W, H = 640, 400
    term = [
        (f'<tspan fill="{t["accent"]}">$</tspan> ansible-playbook deploy.yml', 0),
        (f'<tspan fill="{t["muted"]}">PLAY [app servers] ********</tspan>', 1),
        (f'<tspan fill="{t["ok"]}">ok:</tspan> [web-01]', 2),
        (f'<tspan fill="{t["warn"]}">changed:</tspan> [web-02]', 3),
        (f'<tspan fill="{t["ok"]}">ok:</tspan> [db-01]', 4),
        (f'<tspan fill="{t["ok"]}">recap: failed=0</tspan>', 5),
    ]
    lines = "".join(
        f'<text class="mono ln" x="54" y="{150 + i*26}" font-size="15" fill="{t["text2"]}" style="animation-delay:{d*0.45:.2f}s">{l}</text>'
        for l, d in [(x, i) for i, (x, _) in enumerate(term)] for i in [term.index((l, _)) for _ in [0]] if True
    ) if False else "".join(
        f'<text class="mono ln" x="54" y="{150 + i*26}" font-size="15" fill="{t["text2"]}" style="animation-delay:{i*0.45:.2f}s">{l}</text>'
        for i, (l, _) in enumerate(term))
    racks = ""
    for i, name in enumerate(["web-01", "web-02", "db-01"]):
        y = 112 + i * 64
        racks += (f'<rect x="408" y="{y}" width="196" height="50" rx="10" fill="{t["surface"]}" stroke="{t["border2"]}"/>'
                  f'<rect x="424" y="{y+14}" width="56" height="6" rx="3" fill="{t["border"]}"/>'
                  f'<rect x="424" y="{y+28}" width="40" height="6" rx="3" fill="{t["border"]}"/>'
                  f'<text class="mono" x="500" y="{y+31}" font-size="14" fill="{t["text"]}">{name}</text>'
                  f'<circle class="led" cx="584" cy="{y+25}" r="6" fill="{t["ok"]}" style="animation-delay:{1.2+i*0.45:.2f}s"/>')
    style = """
.ln { animation: type 6s steps(1) infinite; }
@keyframes type { 0% { opacity: 0 } 6% { opacity: 1 } 92% { opacity: 1 } 100% { opacity: 0 } }
.led { animation: led 1.4s ease-in-out infinite; }
@keyframes led { 50% { opacity: .25 } }
.pkt { animation: pkt 2.4s linear infinite; }
@keyframes pkt { from { stroke-dashoffset: 0 } to { stroke-dashoffset: -40 } }
"""
    body = f"""
{frame(t, W, H)}
<rect x="32" y="100" width="324" height="196" rx="14" fill="{t['subtle']}" stroke="{t['border']}"/>
<circle cx="52" cy="119" r="5" fill="{t['danger']}"/><circle cx="68" cy="119" r="5" fill="{t['warn']}"/><circle cx="84" cy="119" r="5" fill="{t['ok']}"/>
{lines}
<path class="pkt" d="M 360 200 C 380 200 384 137 404 137 M 360 200 L 404 200 M 360 200 C 380 200 384 265 404 265" stroke="{t['brand']}" stroke-width="2.5" stroke-dasharray="10 10" stroke-linecap="round"/>
<circle cx="360" cy="200" r="5" fill="{t['brand']}"/>
{racks}
<text x="32" y="64" font-size="30" font-weight="800" fill="{t['text']}" letter-spacing="-0.4">server-deploy-toolkit</text>
<rect x="364" y="40" width="160" height="30" rx="15" fill="{t['accent_subtle']}"/>
<text x="444" y="61" text-anchor="middle" font-size="14" font-weight="600" fill="{t['accent']}">Ansible → Linux</text>
<text x="32" y="340" font-size="17" fill="{t['text2']}">Deploy applications to your own Linux servers</text>
<text x="32" y="366" font-size="17" fill="{t['text2']}">with <tspan fill="{t['text']}" font-weight="600">Ansible</tspan>. No platform lock-in, just your hosts.</text>
"""
    return svg(W, H, "server-deploy-toolkit", "server-deploy-toolkit uses Ansible to deploy applications to your own Linux servers.", body, style)


# ---------------------------------------------------------------- workflow
def workflow(mode):
    t = THEMES[mode]
    W, H = 1280, 300
    nodes = [
        ("01", "Experiment", "Ideas start small, in the open", "status: experiment"),
        ("02", "Harden", "What proves useful gets tests &amp; docs", "status: tool"),
        ("03", "Share", "Versioned and open source", "use it · fork it"),
    ]
    bw, bh, y = 330, 196, 52
    xs = [40, 475, 910]
    icons = [
        lambda x, y: mark(t, x - 2, y - 1, 44, t["accent"], t["brand"]),
        # diagram
        lambda x, y: (f'<rect x="{x}" y="{y}" width="18" height="14" rx="3" stroke="{t["accent"]}" stroke-width="2.5"/>'
                      f'<rect x="{x+24}" y="{y+28}" width="18" height="14" rx="3" stroke="{t["accent"]}" stroke-width="2.5"/>'
                      f'<path d="M {x+9} {y+14} V {y+35} H {x+24}" stroke="{t["accent"]}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>'),
        lambda x, y: (f'<path d="M {x+21} {y} L {x+42} {y+10} V {y+32} L {x+21} {y+42} L {x} {y+32} V {y+10} Z M {x} {y+10} L {x+21} {y+20} L {x+42} {y+10} M {x+21} {y+20} V {y+42}" stroke="{t["accent"]}" stroke-width="2.5" stroke-linejoin="round"/>'),
    ]
    body = f'<rect width="{W}" height="{H}" rx="28" fill="{t["canvas"]}"/>{grid_defs(t, W, H, "wg", 32)}'
    for i, ((num, head, sub, tool), x) in enumerate(zip(nodes, xs)):
        body += (f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="18" fill="{t["surface"]}" stroke="{t["border"]}"/>'
                 f'<rect x="{x}" y="{y}" width="{bw}" height="4" rx="2" fill="{t["brand"]}" opacity="{0.35 + i*0.3:.2f}"/>'
                 f'<rect x="{x+24}" y="{y+28}" width="64" height="64" rx="14" fill="{t["accent_subtle"]}"/>'
                 + icons[i](x + 35, y + 39) +
                 f'<text class="mono" x="{x+bw-24}" y="{y+50}" text-anchor="end" font-size="15" fill="{t["muted"]}">{num}</text>'
                 f'<text x="{x+24}" y="{y+124}" font-size="26" font-weight="800" fill="{t["text"]}">{head}</text>'
                 f'<text x="{x+24}" y="{y+150}" font-size="16" fill="{t["text2"]}">{sub}</text>'
                 f'<text class="mono" x="{x+24}" y="{y+176}" font-size="15" font-weight="600" fill="{t["accent"]}">→ {tool}</text>')
    for x in (40 + bw, 475 + bw):
        x1, x2, cy = x + 8, x + 105 - 8, y + bh / 2
        body += (f'<path d="M {x1} {cy} H {x2}" stroke="{t["border2"]}" stroke-width="2" stroke-dasharray="4 6"/>'
                 f'<path d="M {x2-8} {cy-7} L {x2} {cy} L {x2-8} {cy+7}" stroke="{t["border2"]}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
                 f'<circle class="dot" cx="{x1}" cy="{cy}" r="6" fill="{t["brand"]}"/>')
    style = """
.dot { animation: travel 2.2s cubic-bezier(.5,0,.5,1) infinite; }
@keyframes travel { 0% { transform: translateX(0); opacity: 0 } 15% { opacity: 1 } 85% { opacity: 1 } 100% { transform: translateX(80px); opacity: 0 } }
"""
    body += f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="28" stroke="{t["border"]}"/>'
    return svg(W, H, "How the lab works", "Three steps: ideas start as open experiments, useful ones are hardened into tools, then shared as versioned open source.", body, style)


# ---------------------------------------------------------------- principles
def principles(mode):
    t = THEMES[mode]
    W, H = 1280, 230
    items = [
        ("Open by default", ["Code, issues and experiments", "live in public repositories."]),
        ("Small, sharp tools", ["Each tool does one job well", "and plays nicely with others."]),
        ("Your stack, your rules", ["Text formats, local-first,", "self-hostable where it matters."]),
    ]
    body = ""
    for i, (head, lines) in enumerate(items):
        x = 40 + i * 413
        body += (f'<rect x="{x}" y="20" width="373" height="190" rx="18" fill="{t["surface"]}" stroke="{t["border"]}"/>'
                 + mark(t, x + 28, 46, 44, t["mark"], t["brand"]) +
                 f'<text x="{x+28}" y="136" font-size="23" font-weight="800" fill="{t["text"]}">{head}</text>'
                 + "".join(f'<text x="{x+28}" y="{166 + j*24}" font-size="16" fill="{t["text2"]}">{l}</text>' for j, l in enumerate(lines)))
    return svg(W, H, "Lab principles", "Open by default. Small, sharp tools. Your stack, your rules.", body)


# ---------------------------------------------------------------- section header
def section(mode, slug, label, num):
    t = THEMES[mode]
    W, H = 1280, 90
    body = (f'<text class="mono" x="2" y="54" font-size="18" fill="{t["accent"]}">{num}</text>'
            f'<text x="56" y="58" font-size="34" font-weight="800" fill="{t["text"]}" letter-spacing="-0.6">{label}</text>'
            f'<path d="M {70 + len(label)*19.5:.0f} 46 H {W-60}" stroke="{t["border"]}" stroke-width="2"/>'
            f'<rect class="sweep" x="{70 + len(label)*19.5:.0f}" y="45" width="120" height="3" rx="1.5" fill="{t["brand"]}"/>'
            + mark(t, W - 46, 26, 40))
    end = W - 60 - 120 - (70 + len(label) * 19.5)
    style = f""".sweep {{ animation: sweep 5s ease-in-out infinite alternate; }}
@keyframes sweep {{ to {{ transform: translateX({end:.0f}px) }} }}"""
    return svg(W, H, label, f"Section: {label}", body, style)


# ---------------------------------------------------------------- footer
def footer(mode):
    t = THEMES[mode]
    W, H = 1280, 200
    body = f"""
<rect width="{W}" height="{H}" rx="28" fill="{t['canvas']}"/>
{grid_defs(t, W, H, "fg", 32)}
{mark(t, 596, 30, 88)}
<text x="640" y="152" text-anchor="middle" font-size="20" font-weight="700" fill="{t['text']}">Built in the lab. Shared in the open.</text>
<text class="mono" x="640" y="180" text-anchor="middle" font-size="14" fill="{t['muted']}">github.com/grethel-labs</text>
"""
    return svg(W, H, "Grethel Labs", "Grethel Labs footer: Built in the lab. Shared in the open.", body)


def bench(mode):
    t = THEMES[mode]
    W, H = 1280, 210
    rnd = random.Random(3)
    bub = "".join(f'<circle class="b" cx="{118 + rnd.uniform(-6, 10):.1f}" cy="128" r="{rnd.uniform(3,6):.1f}" style="animation-delay:{-i*0.7:.1f}s"/>' for i in range(5))
    style = f"""
.b {{ fill: {t['brand']}; opacity: 0; animation: rise 3.5s linear infinite; }}
@keyframes rise {{ 0% {{ transform: translateY(0); opacity: 0 }} 15% {{ opacity: .9 }} 100% {{ transform: translateY(-110px); opacity: 0 }} }}
.bar {{ animation: load 4s cubic-bezier(.6,0,.3,1) infinite; }}
@keyframes load {{ 0% {{ width: 0 }} 80%,100% {{ width: 360px }} }}
"""
    body = f"""
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="24" fill="{t['canvas']}" stroke="{t['border2']}" stroke-width="2" stroke-dasharray="10 8"/>
{mark(t, 48, 40, 130)}
{bub}
<text x="230" y="88" font-size="30" font-weight="800" fill="{t['text']}" letter-spacing="-0.4">More on the bench</text>
<text x="230" y="122" font-size="17" fill="{t['text2']}">New tools and experiments land in this organization first.</text>
<text class="mono" x="230" y="166" font-size="15" fill="{t['muted']}">next experiment</text>
<rect x="380" y="154" width="360" height="14" rx="7" fill="{t['accent_subtle']}"/>
<rect class="bar" x="380" y="154" width="240" height="14" rx="7" fill="{t['brand']}"/>
<text class="mono" x="760" y="166" font-size="15" fill="{t['accent']}">brewing…</text>
"""
    return svg(W, H, "More on the bench", "New tools and experiments land in the Grethel Labs organization first.", body, style)


SECTIONS = [("projects", "Featured tools", "01"), ("index", "Lab index", "02"), ("workflow", "How the lab works", "03"), ("principles", "Principles", "04"), ("brand", "Brand", "05")]

for mode in THEMES:
    files = {
        f"hero-{mode}.svg": hero(mode),
        f"card-excaliplant-{mode}.svg": card_excaliplant(mode),
        f"card-server-deploy-toolkit-{mode}.svg": card_deploy(mode),
        f"workflow-{mode}.svg": workflow(mode),
        f"principles-{mode}.svg": principles(mode),
        f"footer-{mode}.svg": footer(mode),
        f"bench-{mode}.svg": bench(mode),
    }
    for slug, label, num in SECTIONS:
        files[f"section-{slug}-{mode}.svg"] = section(mode, slug, label, num)
    for name, content in files.items():
        with open(os.path.join(OUT, name), "w") as f:
            f.write(content)
print("ok", len(os.listdir(OUT)))
