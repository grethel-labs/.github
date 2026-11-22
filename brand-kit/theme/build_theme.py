from pathlib import Path
import json
import html
import subprocess
import hashlib
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
BRAND = {"ink": "#111827", "off-white": "#F7F8FA", "teal": "#2DB8A8"}
UPSTREAM = json.loads((ROOT / "upstream-selected-colors.json").read_text())
SOURCES = [
    {"name": "Radix Colors: 12-step role structure", "url": "https://www.radix-ui.com/colors/docs/palette-composition/understanding-the-scale", "use": "Structure and role inspiration, not a promise that custom pairings inherit Radix contrast guarantees."},
    {"name": "Radix Colors light sRGB scales", "url": "https://github.com/radix-ui/colors/blob/main/src/light.ts", "raw_url": "https://raw.githubusercontent.com/radix-ui/colors/main/src/light.ts", "sha256": "1a9725486609d36b469caa3b84b8de4348b7f2f05d45905127637b988329acbd", "use": "Selected Green, Amber, Red, Blue, Violet and Orange scales."},
    {"name": "Radix Colors dark sRGB scales", "url": "https://github.com/radix-ui/colors/blob/main/src/dark.ts", "raw_url": "https://raw.githubusercontent.com/radix-ui/colors/main/src/dark.ts", "sha256": "d8599fe69a4454340b2bc82e003a210caa6b79082be9a1b7f13429ff03826c68", "use": "Selected Green, Amber, Red, Blue, Violet and Orange scales."},
    {"name": "Radix Colors MIT license", "url": "https://github.com/radix-ui/colors/blob/main/LICENSE", "use": "License for copied palette data; full notice included."},
    {"name": "WCAG 2.2 SC 1.4.3", "url": "https://www.w3.org/TR/WCAG22/#contrast-minimum", "use": "Normal text target 4.5:1."},
    {"name": "WCAG 2.2 SC 1.4.11", "url": "https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html", "use": "Essential controls and graphical objects target 3:1 against adjacent colors."},
]

CUSTOM_SCALES = {
    "light": {
        "neutral": ["#FFFFFF", "#F7F8FA", "#F0F3F6", "#E8EDF2", "#DCE4EB", "#D4DAE2", "#B3BFCD", "#8D9BAE", "#738196", "#66758A", "#526173", "#111827"],
        "teal": ["#F5FCFA", "#EDF9F6", "#E5F6F2", "#D0EEE7", "#C0E8DF", "#A1DBCE", "#7BD0C0", "#53C4B2", "#2DB8A8", "#117C70", "#0B6E63", "#073D39"],
    },
    "dark": {
        "neutral": ["#111827", "#151E2C", "#192231", "#202C3D", "#243247", "#334155", "#4C5E76", "#657993", "#7A8AA0", "#8DA0B8", "#B6C2D1", "#F7F8FA"],
        "teal": ["#0F1C24", "#11272D", "#143A3B", "#164749", "#195759", "#206A69", "#24847B", "#2A9F90", "#2DB8A8", "#4DCDBA", "#5CE0CC", "#C4F5EA"],
    },
}
RADIX_HUES = ("green", "amber", "red", "blue", "violet", "orange")
SCALES = {}
for mode in ("light", "dark"):
    SCALES[mode] = dict(CUSTOM_SCALES[mode])
    for hue in RADIX_HUES:
        SCALES[mode][hue] = [UPSTREAM[mode][hue][f"{hue.upper()}{n}"] for n in range(1, 13)]


def c(mode, hue, step):
    return SCALES[mode][hue][step - 1]


def make_semantics(mode):
    dark = mode == "dark"
    n = lambda s: c(mode, "neutral", s)
    t = lambda s: c(mode, "teal", s)
    # Every value resolves to a concrete sRGB hex color; semantic use is explicit.
    s = {
        "bg-canvas": BRAND["ink"] if dark else BRAND["off-white"],
        "bg-surface": n(3) if dark else n(1),
        "bg-raised": n(4) if dark else n(1),
        "bg-subtle": n(2) if dark else n(3),
        "bg-hover": n(4),
        "bg-active": n(5),
        "bg-inverse": BRAND["off-white"] if dark else BRAND["ink"],
        "text-primary": BRAND["off-white"] if dark else BRAND["ink"],
        "text-secondary": n(11),
        "text-muted": n(10) if dark else n(11),
        "text-inverse": BRAND["ink"] if dark else BRAND["off-white"],
        "text-on-brand": BRAND["ink"],
        "text-link": t(11),
        "text-link-hover": t(12),
        "text-placeholder": n(10) if dark else n(11),
        "border-subtle": n(6),
        "border-default": n(9),
        "border-strong": n(10) if dark else n(11),
        "border-focus": t(11),
        "accent-brand": BRAND["teal"],
        "accent-solid": t(9) if dark else t(10),
        "accent-hover": t(10) if dark else t(11),
        "accent-active": t(8) if dark else t(12),
        "accent-foreground": BRAND["ink"] if dark else "#FFFFFF",
        "accent-subtle": t(3),
        "accent-subtle-hover": t(4),
        "accent-subtle-active": t(5),
        "accent-text": t(11),
        "focus-ring": t(11),
        "focus-offset": BRAND["ink"] if dark else BRAND["off-white"],
        "selection-bg": t(4),
        "selection-text": t(12),
        "control-bg": n(3) if dark else n(1),
        "control-bg-hover": n(4) if dark else n(3),
        "control-bg-active": n(5) if dark else n(4),
        "control-border": n(9),
        "control-border-hover": n(10) if dark else n(11),
        "control-text": BRAND["off-white"] if dark else BRAND["ink"],
        "control-placeholder": n(10) if dark else n(11),
        "disabled-bg": n(4),
        "disabled-text": n(8) if dark else n(9),
        "disabled-border": n(6),
    }
    # Darkened light text values are Grethel-specific contrast adaptations.
    light_status_text = {"success": "#1A734B", "warning": "#915500", "danger": "#B8242A", "info": "#0B63B6"}
    for role, hue in (("success", "green"), ("warning", "amber"), ("danger", "red"), ("info", "blue")):
        s[f"{role}-bg"] = c(mode, hue, 3)
        s[f"{role}-border"] = c(mode, hue, 11)
        s[f"{role}-text"] = c(mode, hue, 11) if dark else light_status_text[role]
        s[f"{role}-solid"] = c(mode, hue, 11) if dark else (c(mode, hue, 9) if role == "warning" else c(mode, hue, 11))
        s[f"{role}-foreground"] = BRAND["ink"] if dark or role == "warning" else "#FFFFFF"
    s.update({
        "code-bg": n(2) if dark else n(3),
        "code-text": BRAND["off-white"] if dark else BRAND["ink"],
        "code-comment": n(10) if dark else n(11),
        "code-keyword": c(mode, "violet", 11),
        "code-string": c(mode, "green", 11) if dark else light_status_text["success"],
        "code-number": c(mode, "amber", 11) if dark else light_status_text["warning"],
        "code-function": c(mode, "blue", 11) if dark else light_status_text["info"],
        "code-punctuation": n(11),
        "chart-1": t(9) if dark else t(10),
        "chart-2": c(mode, "blue", 11),
        "chart-3": c(mode, "violet", 11),
        "chart-4": c(mode, "amber", 11),
        "chart-5": c(mode, "red", 11),
        "chart-6": c(mode, "green", 11),
        "chart-grid": n(6),
        "chart-axis": n(10) if dark else n(11),
        "overlay-scrim": "#090F1ECC" if dark else "#111827B8",
        "scrollbar-thumb": n(9),
    })
    return s


SEMANTICS = {mode: make_semantics(mode) for mode in ("light", "dark")}
assert set(SEMANTICS["light"]) == set(SEMANTICS["dark"])
assert len(SEMANTICS["light"]) == 80, len(SEMANTICS["light"])


def lum(h):
    parts = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in parts]
    return sum(v * w for v, w in zip(linear, (.2126, .7152, .0722)))


def contrast(fg, bg):
    low, high = sorted([lum(fg), lum(bg)])
    return (high + .05) / (low + .05)


def check_theme():
    rows = []
    def add(mode, foreground, background, threshold, kind):
        s = SEMANTICS[mode]
        f = s.get(foreground, foreground)
        b = s.get(background, background)
        value = contrast(f, b)
        rows.append({"mode": mode, "foreground_role": foreground, "background_role": background, "foreground": f, "background": b, "ratio": round(value, 4), "threshold": threshold, "pass": value >= threshold, "kind": kind})
    for mode in ("light", "dark"):
        for fg in ("text-primary", "text-secondary", "text-muted", "text-link"):
            for bg in ("bg-canvas", "bg-surface", "bg-raised"):
                add(mode, fg, bg, 4.5, "normal-text")
        for bg in ("accent-solid", "accent-hover", "accent-active"):
            add(mode, "accent-foreground", bg, 4.5, "button-label")
        for bg in ("accent-subtle", "accent-subtle-hover", "accent-subtle-active"):
            add(mode, "accent-text", bg, 4.5, "normal-text")
        add(mode, "selection-text", "selection-bg", 4.5, "selected-text")
        add(mode, "text-inverse", "bg-inverse", 4.5, "normal-text")
        for fg in ("control-text", "control-placeholder"):
            for bg in ("control-bg", "control-bg-hover", "control-bg-active"):
                add(mode, fg, bg, 4.5, "control-text")
        for fg in ("control-border", "control-border-hover", "focus-ring"):
            for bg in ("bg-canvas", "bg-surface", "bg-raised", "control-bg"):
                add(mode, fg, bg, 3, "essential-ui")
        for role in ("success", "warning", "danger", "info"):
            add(mode, f"{role}-text", f"{role}-bg", 4.5, "status-text")
            add(mode, f"{role}-foreground", f"{role}-solid", 4.5, "status-solid-label")
            add(mode, f"{role}-border", f"{role}-bg", 3, "status-border")
        for fg in ("code-text", "code-comment", "code-keyword", "code-string", "code-number", "code-function", "code-punctuation"):
            add(mode, fg, "code-bg", 4.5, "code-text")
        for fg in [f"chart-{i}" for i in range(1, 7)]:
            for bg in ("bg-canvas", "bg-surface", "bg-raised"):
                add(mode, fg, bg, 3, "chart-on-background")
    diagnostic = []
    for fg, bg, intended in [
        ("#111827", "#2DB8A8", "Use Ink text on the constant brand teal."),
        ("#FFFFFF", "#2DB8A8", "Do not use white normal-sized text on the constant brand teal."),
        ("#2DB8A8", "#F7F8FA", "Brand teal is a decorative accent on light canvas; use accent-text for small text."),
    ]:
        ratio = contrast(fg, bg)
        diagnostic.append({"foreground": fg, "background": bg, "ratio": round(ratio, 4), "normal_text_pass": ratio >= 4.5, "guidance": intended})
    report = {
        "method": "WCAG 2.2 sRGB relative luminance, (Llighter + 0.05)/(Ldarker + 0.05); full precision used for decisions.",
        "normal_text_target": 4.5,
        "essential_ui_target": 3.0,
        "test_count": len(rows),
        "pass_count": sum(row["pass"] for row in rows),
        "fail_count": sum(not row["pass"] for row in rows),
        "pairs": rows,
        "brand_diagnostics": diagnostic,
        "limits": [
            "Only the explicitly listed foreground/background pairings were checked. Arbitrary cross-token combinations are not guaranteed.",
            "No blanket WCAG conformance claim. Size, weight, focus area, keyboard behavior, semantics, interaction and assistive technology remain application responsibilities.",
            "Solid sRGB colors were checked. Images, gradients, transparency/compositing and browser anti-aliasing were not simulated.",
            "Decorative borders, gridlines and disabled controls are not included in pass counts. If a line conveys essential information, use an essential border/axis token.",
            "Chart colors are checked against their surfaces, not for every mutual pairing or color-vision deficiency. Add labels, marker shapes or line styles; separate touching regions.",
            "Focus color assumes an outer ring with a 2px gap filled by the current canvas/surface. Ring geometry and all adjacent colors still require real-UI verification.",
        ],
    }
    (ROOT / "contrast-report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    failed = [row for row in rows if not row["pass"]]
    if failed:
        print(json.dumps(failed, indent=2))
        raise RuntimeError(f"{len(failed)} intended pairings failed")
    return report


def write_tokens_css(report):
    raw = {}
    for mode in ("light", "dark"):
        raw[mode] = {
            hue: {str(i): value for i, value in enumerate(values, 1)}
            for hue, values in SCALES[mode].items()
        }
    document = {
        "format": "Grethel resolved color tokens",
        "name": "Grethel Clean",
        "version": "2.0",
        "retrieved_at": "2026-11-21",
        "color_space": "sRGB",
        "brand": BRAND,
        "raw_scales": raw,
        "semantic": SEMANTICS,
        "counts": {"modes": 2, "scales_per_mode": 8, "steps_per_scale": 12, "semantic_roles_per_mode": 80},
        "origin": {
            "neutral_and_teal": "Original Grethel-specific scales inspired by the Radix 12-step role architecture. They are not the stock Radix Slate/Teal palette.",
            "green_amber_red_blue_violet_orange": "Selected unmodified sRGB scales from Radix Colors; MIT license bundled.",
            "semantic_mapping": "Original Grethel role mappings. Some light status/code text values are darkened adaptations to meet the stated concrete contrast targets.",
            "light_contrast_adaptations": {"success_text": "#1A734B", "warning_text": "#915500", "danger_text": "#B8242A", "info_text": "#0B63B6"},
        },
        "sources": SOURCES,
    }
    (ROOT / "grethel-theme.tokens.json").write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n")
    def declarations(mode, indent="  "):
        d = [f"{indent}color-scheme: {mode};"]
        for hue, values in SCALES[mode].items():
            d.extend(f"{indent}--gl-{hue}-{i}: {color};" for i, color in enumerate(values, 1))
        d.append("")
        d.extend(f"{indent}--gl-{name}: {color};" for name, color in SEMANTICS[mode].items())
        return "\n".join(d)
    css = """/*
 * Grethel Clean 2.0
 * Brand-specific Neutral/Teal + selected Radix Colors functional scales.
 * Radix palette data: MIT, copyright Modulz / WorkOS.
 * See LICENSE-radix-colors.txt, sources.json and contrast-report.json.
 * This file declares tokens and sets color-scheme for native browser controls.
 * It does not reset or define application component styles.
 */

:root {
  --gl-brand-ink: #111827;
  --gl-brand-off-white: #F7F8FA;
  --gl-brand-teal: #2DB8A8;
}

:root,
[data-theme="light"] {
""" + declarations("light") + """
}

@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]):not([data-theme="dark"]) {
""" + declarations("dark", "    ") + """
  }
}

[data-theme="dark"] {
""" + declarations("dark") + """
}
"""
    (ROOT / "grethel-theme.css").write_text(css)
    (ROOT / "sources.json").write_text(json.dumps({"retrieved_at": "2026-11-21", "sources": SOURCES}, indent=2, ensure_ascii=False) + "\n")
    (ROOT / "README.txt").write_text(f"""GRETHEL CLEAN 2.0 — LIGHT / DARK

Umfang: 8 Skalen mit jeweils 12 Stufen pro Modus (192 Rohfarbwerte) und
80 semantische Rollen je Modus. Die Markenfarben bleiben unverändert:
Ink #111827, Off-White #F7F8FA, Teal #2DB8A8.

GRUNDLAGE
Die Rollenstruktur folgt Radix Colors. Grethel Neutral und Grethel Teal sind
eigene, markentreue Skalen. Die ausgewählten Skalen Green, Amber, Red, Blue,
Violet und Orange stammen aus den offiziellen Radix-sRGB-Quellen.
LICENSE-radix-colors.txt enthält die MIT-Lizenz. Herkunft und Anpassungen sind
in grethel-theme.tokens.json sowie sources.json dokumentiert.

DATEIEN
grethel-theme.css             CSS Custom Properties mit Präfix --gl-
grethel-theme.tokens.json     Rohskalen und konkret aufgelöste Rollen
contrast-report.json         {report['test_count']} konkret geprüfte Kontrastpaare
palette-light/dark.svg/png    Kerntokens, Statusfarben und UI-Beispiele
upstream-selected-colors.json Ausgewählte unveränderte Radix-Rohwerte
build_theme.py               Reproduzierbare Erstellung/Prüfung

VERWENDUNG
CSS einbinden. Ohne Attribut auf dem html-Element folgt der Modus automatisch
prefers-color-scheme. html[data-theme="light"] beziehungsweise
html[data-theme="dark"] erzwingt den Modus. Dieselben Attribute können einzelne
Teilbereiche überschreiben. Für Systemmodus das Attribut entfernen.
Die Datei deklariert Tokens und setzt color-scheme für native Browser-Steuerelemente.
Eigene Komponentenstile oder CSS-Resets enthält sie nicht.

Beispiel:
body {{ background: var(--gl-bg-canvas); color: var(--gl-text-primary); }}
.card {{ background: var(--gl-bg-surface); border: 1px solid var(--gl-border-subtle); }}
.button {{ background: var(--gl-accent-solid); color: var(--gl-accent-foreground); }}
.button:hover {{ background: var(--gl-accent-hover); }}
.button:active {{ background: var(--gl-accent-active); }}
.button:focus-visible {{ outline: 2px solid var(--gl-focus-ring); outline-offset: 2px; }}

BRAND UND BEDIENOBERFLÄCHE
Brand-Teal ist konstant und für Logos/Dekor geeignet. Auf hellem Grund sind
accent-text beziehungsweise text-link für Text vorgesehen. Primäre Buttons:
Light #117C70 mit weißer Schrift; Dark #2DB8A8 mit Ink-Schrift. Weiß auf dem
hellen Brand-Teal erreicht nur {contrast('#FFFFFF', '#2DB8A8'):.2f}:1; Ink darauf {contrast('#111827', '#2DB8A8'):.2f}:1.
border-subtle und chart-grid sind dekorativ. Wesentliche Grenzen erhalten
control-border/border-default; wichtige Diagrammlinien erhalten chart-axis.

GRENZEN
{report['pass_count']}/{report['test_count']} geprüfte Paarungen erreichen 4,5:1 für Normaltext beziehungsweise
3:1 für wesentliche UI-Informationen. Dies ist keine vollständige
WCAG-Konformitätsbewertung. Nicht beliebig Tokens kombinieren. Bilder, Alpha,
Fokus-Geometrie, alle Nachbarfarben und tatsächliches Rendering in der Anwendung
prüfen. Status und Diagrammserien zusätzlich beschriften oder durch Formen/
Linienstile unterscheiden; Farbe allein genügt nicht.

QUELLEN
""" + "\n".join(x["url"] for x in SOURCES) + "\n")


def svg_document(width, height, title, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{html.escape(title)}</title>
<desc id="desc">Exakte Farbwerte des Grethel Clean Themes. Alle Hexlabels entsprechen den dargestellten Vollfarben.</desc>
<g font-family="Liberation Sans, Arial, sans-serif">{body}</g>
</svg>'''


def rect(x, y, w, h, fill, stroke=None, radius=12, sw=1):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}"' + (f' stroke="{stroke}" stroke-width="{sw}"' if stroke else "") + "/>"


def text(x, y, value, size, color, weight=400, family=None, anchor=None):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}"' + (f' font-family="{family}"' if family else "") + (f' text-anchor="{anchor}"' if anchor else "") + f'>{html.escape(value)}</text>'


def line(x1, y1, x2, y2, stroke, width=1):
    return f'<path d="M{x1} {y1} H{x2}" stroke="{stroke}" stroke-width="{width}"/>' if y1 == y2 else f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{stroke}" stroke-width="{width}"/>'


def foreground_for(color):
    return "#111827" if contrast("#111827", color) >= contrast("#F7F8FA", color) else "#F7F8FA"


def palette_board(mode):
    s = SEMANTICS[mode]
    w, h = 1920, 1440
    b = rect(0, 0, w, h, s["bg-canvas"], radius=0)
    b += text(72, 96, "GRETHEL LABS", 27, s["text-secondary"], 700)
    b += text(72, 171, f"Grethel Clean / {mode.title()}", 64, s["text-primary"], 700)
    b += text(72, 214, "Markenfarben, Oberflächen und Zustände", 26, s["text-secondary"])
    b += text(1848, 100, "COLOR SYSTEM  2.0", 21, s["text-secondary"], 600, anchor="end")
    for i, (label, value) in enumerate([("Ink", BRAND["ink"]), ("Off-White", BRAND["off-white"]), ("Teal", BRAND["teal"])]):
        x = 72 + i * 600
        b += rect(x, 260, 576, 150, value, s["border-subtle"])
        fg = foreground_for(value)
        b += text(x + 28, 310, label, 26, fg, 600)
        b += text(x + 28, 372, value, 37, fg, 700, "Liberation Mono, monospace")
    b += text(72, 472, "OBERFLÄCHEN & TEXT", 23, s["text-secondary"], 700)
    roles = [
        ("Canvas", "bg-canvas"), ("Surface", "bg-surface"), ("Raised", "bg-raised"), ("Text", "text-primary"),
        ("Muted", "text-muted"), ("UI Border", "control-border"), ("Focus", "focus-ring"), ("UI Accent", "accent-solid"),
    ]
    for i, (label, token) in enumerate(roles):
        x = 72 + (i % 4) * 450
        y = 504 + (i // 4) * 124
        b += rect(x, y, 426, 104, s["bg-surface"], s["border-subtle"])
        b += rect(x + 20, y + 20, 64, 64, s[token], s["border-subtle"], radius=8)
        b += text(x + 108, y + 44, label, 26, s["text-primary"], 600)
        b += text(x + 108, y + 77, s[token], 24, s["text-secondary"], 400, "Liberation Mono, monospace")
    b += text(72, 799, "STATUSFARBEN", 23, s["text-secondary"], 700)
    for i, role in enumerate(("success", "warning", "danger", "info")):
        x = 72 + i * 450
        b += rect(x, 830, 426, 116, s[f"{role}-bg"], s[f"{role}-border"], sw=2)
        b += text(x + 24, 870, role.title(), 27, s[f"{role}-text"], 700)
        b += text(x + 24, 904, f"Text {s[role + '-text']}", 21, s[f"{role}-text"], 400, "Liberation Mono, monospace")
        b += text(x + 24, 931, f"Fläche {s[role + '-bg']}", 19, s[f"{role}-text"], 400, "Liberation Mono, monospace")
    b += text(72, 1010, "ANWENDUNG", 23, s["text-secondary"], 700)
    b += rect(72, 1042, 876, 254, s["bg-surface"], s["border-subtle"])
    b += text(100, 1093, "Bereit für den nächsten Build.", 30, s["text-primary"], 700)
    b += text(100, 1135, "Primäre Aktion und fokussiertes Eingabefeld", 23, s["text-secondary"])
    b += rect(100, 1175, 256, 70, s["accent-solid"], radius=9)
    b += text(228, 1219, "Build starten", 25, s["accent-foreground"], 700, anchor="middle")
    b += rect(390, 1171, 522, 78, s["bg-surface"], s["focus-ring"], radius=12, sw=2)
    b += rect(395, 1176, 512, 68, s["control-bg"], s["control-border"], radius=8, sw=2)
    b += text(419, 1219, "Repository auswählen", 25, s["control-placeholder"])
    b += text(1008, 1010, "GEPRÜFTE PAARUNGEN", 23, s["text-secondary"], 700)
    pairs = [
        ("Text / Canvas", "text-primary", "bg-canvas"),
        ("Button-Text / Accent", "accent-foreground", "accent-solid"),
        ("Fokus / Canvas", "focus-ring", "bg-canvas"),
    ]
    for i, (label, fg, bg) in enumerate(pairs):
        y = 1094 + i * 74
        b += text(1008, y, label, 25, s["text-primary"], 600)
        b += text(1848, y, f"{contrast(s[fg], s[bg]):.2f}:1", 30, s["accent-text"], 700, "Liberation Mono, monospace", anchor="end")
        b += line(1008, y + 20, 1848, y + 20, s["border-subtle"])
    b += text(72, 1361, "8 Skalen × 12 Stufen pro Modus  ·  80 semantische Rollen  ·  JSON + CSS", 23, s["text-secondary"])
    b += text(72, 1400, "Eigene Grethel-Neutral-/Teal-Skalen; ausgewählte Funktionsfarben aus Radix Colors (MIT).", 20, s["text-secondary"])
    path = ROOT / f"palette-{mode}.svg"
    path.write_text(svg_document(w, h, f"Grethel Clean {mode.title()} – Farbpalette", b))


def render_all():
    for mode in ("light", "dark"):
        svg = ROOT / f"palette-{mode}.svg"
        ET.parse(svg)
        subprocess.run(["inkscape", str(svg), "--export-type=png", "--export-width=2880", f"--export-filename={svg.with_suffix('.png')}"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


if __name__ == "__main__":
    report = check_theme()
    write_tokens_css(report)
    for mode in ("light", "dark"):
        palette_board(mode)
    render_all()
    print(json.dumps({"semantic_roles_per_mode": 80, "raw_values_total": 192, "contrast_tests": report["test_count"], "passes": report["pass_count"], "files": sorted(p.name for p in ROOT.iterdir() if p.is_file())}, indent=2))
