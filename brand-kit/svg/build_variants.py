"""Rebuild native SVG variants from the self-contained master-paths.json.

Uses only Python's standard library. All lettering is outlined vector geometry.
"""
from pathlib import Path
import json
from html import escape

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / 'master-paths.json').read_text())
INK, PAPER, TEAL = DATA['colors']['ink'], DATA['colors']['off_white'], DATA['colors']['teal']
MARK = DATA['mark']['base_path']
ACCENT = DATA['mark']['accent_path']
WORD = DATA['wordmark']['path']
WORD_WIDTH = DATA['wordmark']['viewBox'][2]
WORD_HEIGHT = DATA['wordmark']['viewBox'][3]

def mark(x=0, y=0, size=600, color=INK, accent=TEAL, outline=False):
    if outline:
        body = f'<path d="{MARK}" fill="none" stroke="{color}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>'
    else:
        body = f'<path d="{MARK}" fill="{color}" fill-rule="nonzero"/>'
    if accent is not None:
        body += f'\n<path d="{ACCENT}" fill="{accent}"/>'
    return f'<g transform="translate({x:g} {y:g}) scale({size / 600:.8f})">\n{body}\n</g>'

def wordmark(x, y, width, color=INK):
    return f'<path d="{WORD}" fill="{color}" fill-rule="nonzero" transform="translate({x:g} {y:g}) scale({width / WORD_WIDTH:.8f})"/>'

def write(name, w, h, content, label, desc, background=None):
    ident=name.replace('.svg','').replace('_','-')
    bg=f'<rect width="{w:g}" height="{h:g}" fill="{background}"/>\n' if background else ''
    svg=f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w:g}" height="{h:g}" viewBox="0 0 {w:g} {h:g}" role="img" aria-labelledby="{ident}-title {ident}-desc">
<title id="{ident}-title">{escape(label)}</title>
<desc id="{ident}-desc">{escape(desc)}</desc>
{bg}{content}
</svg>
'''
    (ROOT/name).write_text(svg)

base_desc='Grethel Labs: a geometric laboratory flask whose open body and crossbar form a capital G. Native vector paths; no raster images or external fonts.'
write('master-mark.svg',600,600,mark(),'Grethel Labs master signet',base_desc)
write('signet-color.svg',600,600,mark(),'Grethel Labs color signet',base_desc)
write('signet-mono.svg',600,600,mark(accent=None),'Grethel Labs monochrome signet',base_desc)
write('signet-inverse.svg',600,600,mark(color=PAPER),'Grethel Labs inverse signet',base_desc+' Off-white and teal for dark surfaces.')
write('signet-outline.svg',600,600,mark(outline=True),'Grethel Labs outline signet',base_desc+' Decorative outlined rendition for larger sizes.')
write('wordmark-ink.svg',WORD_WIDTH,WORD_HEIGHT,wordmark(0,0,WORD_WIDTH),'Grethel Labs wordmark', 'The Grethel Labs wordmark as outlined vector lettering with no font dependency.')
write('wordmark-inverse.svg',WORD_WIDTH,WORD_HEIGHT,wordmark(0,0,WORD_WIDTH,PAPER),'Grethel Labs inverse wordmark', 'The Grethel Labs wordmark in off-white outlined vector lettering for dark surfaces.')

for mode, fg, bg in [('light',INK,PAPER),('dark',PAPER,INK)]:
    # Transparent logo variants: the mode describes the intended underlying surface.
    stacked=mark(300,240,610,fg)+ '\n' +wordmark(152,899,951,fg)
    write(f'logo-stacked-{mode}.svg',1254,1254,stacked,f'Grethel Labs stacked logo — {mode}',base_desc+' Transparent background; symbol above the outlined wordmark.')
    horizontal=mark(40,40,400,fg)+'\n'+wordmark(500,180,1050,fg)
    write(f'logo-horizontal-{mode}.svg',1600,480,horizontal,f'Grethel Labs horizontal logo — {mode}',base_desc+' Transparent background; symbol beside the outlined wordmark.')
    write(f'avatar-{mode}.svg',1000,1000,mark(190,190,620,fg),f'Grethel Labs avatar — {mode}',base_desc+' Centered square profile image with circular-crop safety margin.',bg)
    banner=mark(160,185,430,fg)+'\n'+wordmark(700,334,1050,fg)
    write(f'banner-{mode}.svg',2400,800,banner,f'Grethel Labs banner — {mode}',base_desc+' Wide 3:1 banner with a horizontal wordmark and generous free space.',bg)

# Decorative construction drawing, retaining the exact foreground master.
guides=[]
for x in [300,519,584,669,736,887]:
    guides.append(f'<path d="M {x} 160 V 1090"/>')
for y in [265,324,596,662,762,834,900,1019]:
    guides.append(f'<path d="M 140 {y} H 1120"/>')
guides.append('<path d="M 280 750 L 580 325 M 670 325 L 950 700"/>')
guides.append('<circle cx="627" cy="556" r="385"/>')
guides_xml='<g fill="none" stroke="#A7B5C5" stroke-width="1.2" stroke-dasharray="7 7" opacity="0.6">'+''.join(guides)+'</g>'
corners='<path d="M 70 110 V 70 H 110 M 1144 70 H 1184 V 110 M 70 1144 V 1184 H 110 M 1144 1184 H 1184 V 1144" fill="none" stroke="#2DB8A8" stroke-width="3"/>'
foreground=mark(300,240,610)+wordmark(152,899,951)
write('logo-construction.svg',1254,1254,guides_xml+'\n'+corners+'\n'+foreground,'Grethel Labs construction variant',base_desc+' Decorative geometry guides for large editorial use, not a dimensional engineering specification.',PAPER)

print(json.dumps({'svg_files':sorted(p.name for p in ROOT.glob('*.svg')),'total':len(list(ROOT.glob('*.svg')))}))
