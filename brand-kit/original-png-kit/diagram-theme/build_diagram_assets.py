"""Build deterministic Grethel Clean design previews and editable Excalidraw scenes.

The preview SVG/PNG is a design reference, not an export from excaliplant.
"""
from __future__ import annotations

import hashlib
import html
import json
import math
from pathlib import Path

import fitz
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

ROOT = Path(__file__).resolve().parent
W, H = 1600, 900
FONT_PATH = Path('/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf')
FONT = TTFont(FONT_PATH)
GLYPHS = FONT.getGlyphSet()
CMAP = FONT.getBestCmap()
UPM = FONT['head'].unitsPerEm

PALETTES = {
    'light': dict(canvas='#F7F8FA', surface='#FFFFFF', text='#111827',
                  textMuted='#526173', border='#64748B', edge='#64748B',
                  divider='#D4DAE2', accent='#117C70', accentFill='#E5F6F2',
                  brandAccent='#2DB8A8'),
    'dark': dict(canvas='#111827', surface='#192231', text='#F7F8FA',
                 textMuted='#B6C2D1', border='#7A8AA0', edge='#7A8AA0',
                 divider='#334155', accent='#2DB8A8', accentFill='#143A3B',
                 brandAccent='#2DB8A8'),
}

NODES = {
    'client': (96, 385, 208, 128, 'Client', 'Web / CLI'),
    'api': (472, 385, 232, 128, 'API', 'HTTP service'),
    'queue': (904, 260, 240, 128, 'Job Queue', 'Background jobs'),
    'worker': (1264, 260, 240, 128, 'Worker', 'Job processor'),
    'database': (904, 620, 240, 128, 'Database', 'Persistent store'),
}

# All source/target endpoints remain outside the node borders by 12px.
EDGES = [
    ('request', 'client', 'api', [(316,449),(460,449)], 'HTTPS', (388,414), False, [1,.5], [0,.5]),
    ('enqueue', 'api', 'queue', [(716,417),(798,417),(798,324),(892,324)], 'enqueue', (845,289), True, [1,.25], [0,.5]),
    ('run', 'queue', 'worker', [(1156,324),(1252,324)], 'run', (1204,289), True, [1,.5], [0,.5]),
    ('query', 'api', 'database', [(588,525),(588,684),(892,684)], 'read / write', (740,649), False, [.5,1], [0,.5]),
    ('persist', 'worker', 'database', [(1384,400),(1384,684),(1156,684)], 'persist', (1268,649), False, [.5,1], [1,.5]),
]

def text_width(text: str, size: float) -> float:
    return sum(GLYPHS[CMAP.get(ord(c), '.notdef')].width for c in text) * size / UPM

def svg_text(text: str, x: float, y: float, size: float, color: str, align='left') -> str:
    """Text top y; font outlines keep the image independent of installed fonts."""
    tw = text_width(text, size)
    if align == 'center':
        x -= tw / 2
    elif align == 'right':
        x -= tw
    pen = SVGPathPen(GLYPHS)
    cursor = 0
    for char in text:
        glyph = GLYPHS[CMAP.get(ord(char), '.notdef')]
        glyph.draw(TransformPen(pen, (1, 0, 0, 1, cursor, 0)))
        cursor += glyph.width
    baseline = y + size * .92
    scale = size / UPM
    return (f'<g aria-label="{html.escape(text, quote=True)}"><title>{html.escape(text)}</title>'
            f'<path d="{pen.getCommands()}" fill="{color}" '
            f'transform="translate({x:.3f},{baseline:.3f}) scale({scale:.7f},-{scale:.7f})"/></g>')

def base_element(id_: str, type_: str, x: float, y: float, width: float, height: float,
                 color: str, fill='transparent', groups=None) -> dict:
    seed = int(hashlib.sha256(id_.encode()).hexdigest()[:7],16)
    return dict(id=id_, type=type_, x=x, y=y, width=width, height=height,
                angle=0, strokeColor=color, backgroundColor=fill,
                fillStyle='solid', strokeWidth=2, strokeStyle='solid',
                roughness=0, opacity=100, groupIds=groups or [], frameId=None,
                roundness=None, seed=seed, version=1, versionNonce=seed,
                index=None, isDeleted=False, boundElements=None,
                updated=1795219200000, created=1795219200000,
                link=None, locked=False)

def text_element(id_, text, x, y, size, color, width=None, align='left', groups=None):
    width = width if width is not None else text_width(text,size)
    e = base_element(id_, 'text', x, y, width, size*1.25, color, groups=groups)
    e.update(fontSize=size,fontFamily=9,text=text,originalText=text,
             textAlign=align,verticalAlign='top',containerId=None,
             lineHeight=1.25,autoResize=False,baseline=size*.92,
             baseFontSize=None)
    return e

def build(mode: str):
    p = PALETTES[mode]
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
           f'<title>Grethel Clean {mode.title()} — architecture diagram theme</title>',
           '<desc>Client calls API. API enqueues jobs into Job Queue. Job Queue runs Worker. API reads and writes Database. Worker persists results to Database.</desc>',
           f'<rect width="{W}" height="{H}" fill="{p["canvas"]}"/>']
    elements=[]
    # Typography-led title area, small brand accent only.
    svg.append(f'<rect x="96" y="65" width="9" height="9" fill="{p["brandAccent"]}"/>')
    elements.append(base_element('brand-accent','rectangle',96,65,9,9,p['brandAccent'],p['brandAccent']))
    def add_text(id_,text,x,y,size,color,align='left',width=None,groups=None):
        svg.append(svg_text(text,x,y,size,color,align))
        tx = x if align=='left' else x-(width or text_width(text,size))/(2 if align=='center' else 1)
        elements.append(text_element(id_,text,tx,y,size,color,width,align,groups))
    add_text('brand','GRETHEL LABS',120,57,17,p['textMuted'])
    add_text('mode',mode.upper(),1504,57,17,p['textMuted'],'right')
    add_text('heading','Grethel Clean',96,101,42,p['text'])
    add_text('subtitle','Architektur · Beispiel für ein Diagramm-Thema',96,158,21,p['textMuted'])
    svg.append(f'<line x1="96" y1="211" x2="1504" y2="211" stroke="{p["divider"]}" stroke-width="1"/>')
    e=base_element('header-divider','line',96,211,1408,0,p['divider'])
    e.update(points=[[0,0],[1408,0]],startBinding=None,endBinding=None,startArrowhead=None,endArrowhead=None,polygon=False)
    e['strokeWidth']=1
    elements.append(e)

    # Draw paths before node boxes. Link labels sit away from the strokes.
    for eid, source, target, pts, label, label_pos, accent, sfp, tfp in EDGES:
        col=p['accent'] if accent else p['edge']
        d=' '.join(('M' if i==0 else 'L')+f'{x},{y}' for i,(x,y) in enumerate(pts))
        svg.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="2" stroke-linejoin="miter"/>')
        px,py=pts[-2]; x,y=pts[-1]
        theta=math.atan2(y-py,x-px)
        length=11; half=4.5
        ax=x-length*math.cos(theta); ay=y-length*math.sin(theta)
        l=(ax+half*math.sin(theta),ay-half*math.cos(theta))
        r=(ax-half*math.sin(theta),ay+half*math.cos(theta))
        svg.append(f'<path d="M{x},{y} L{l[0]:.2f},{l[1]:.2f} L{r[0]:.2f},{r[1]:.2f} Z" fill="{col}"/>')
        x0,y0=pts[0]
        e=base_element('edge-'+eid,'arrow',x0,y0,max(x for x,y in pts)-min(x for x,y in pts),max(y for x,y in pts)-min(y for x,y in pts),col)
        e.update(points=[[x-x0,y-y0] for x,y in pts],startArrowhead=None,endArrowhead='triangle',
                 startBinding=dict(elementId='node-'+source,fixedPoint=sfp,mode='orbit',focus=0,gap=12),
                 endBinding=dict(elementId='node-'+target,fixedPoint=tfp,mode='orbit',focus=0,gap=12),
                 elbowed=False)
        elements.append(e)
        add_text('label-'+eid,label,*label_pos,17,col if accent else p['textMuted'],'center')

    for nid,(x,y,w,h,name,sub) in NODES.items():
        col=p['accent'] if nid=='api' else p['border']
        fill=p['accentFill'] if nid=='api' else p['surface']
        svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{col}" stroke-width="2"/>')
        e=base_element('node-'+nid,'rectangle',x,y,w,h,col,fill,groups=['group-'+nid])
        e['roundness']={'type':3,'value':8}
        e['boundElements']=[{'id':'edge-'+ed[0],'type':'arrow'} for ed in EDGES if ed[1]==nid or ed[2]==nid]
        elements.append(e)
        add_text('node-title-'+nid,name,x+w/2,y+29,26,p['text'],'center',w-32,['group-'+nid])
        add_text('node-subtitle-'+nid,sub,x+w/2,y+70,17,p['textMuted'],'center',w-32,['group-'+nid])

    svg.append(f'<line x1="96" y1="802" x2="1504" y2="802" stroke="{p["divider"]}" stroke-width="1"/>')
    e=base_element('footer-divider','line',96,802,1408,0,p['divider'])
    e.update(points=[[0,0],[1408,0]],startBinding=None,endBinding=None,startArrowhead=None,endArrowhead=None,polygon=False)
    e['strokeWidth']=1
    elements.append(e)
    add_text('footer-style','Klare Konturen  /  2 px  /  Ohne Schraffur',96,829,17,p['textMuted'])
    add_text('footer-concept','THEME-ENTWURF',1504,829,15,p['textMuted'],'right')
    svg.append('</svg>')
    svg_path=ROOT/f'grethel-clean-{mode}.svg'
    svg_path.write_text('\n'.join(svg),encoding='utf-8')
    # MuPDF rasterizes the deterministic vector artwork at 2x resolution.
    doc=fitz.open(svg_path)
    pix=doc[0].get_pixmap(matrix=fitz.Matrix(2,2),alpha=False)
    pix.save(ROOT/f'grethel-clean-{mode}.png')
    scene={'type':'excalidraw','version':2,'source':'https://excalidraw.com',
           'elements':elements,'appState':{'viewBackgroundColor':p['canvas'],'gridSize':20,
              'gridModeEnabled':False,'theme':'light','exportWithDarkMode':False,
              'exportBackground':True,'exportScale':2,'currentItemStrokeColor':p['border'],
              'currentItemBackgroundColor':p['surface'],'currentItemFillStyle':'solid',
              'currentItemStrokeWidth':2,'currentItemStrokeStyle':'solid',
              'currentItemRoughness':0,'currentItemFontFamily':9,'currentItemFontSize':20,
              'currentItemRoundness':'round','zoom':{'value':1},'scrollX':0,'scrollY':0},
           'files':{}}
    (ROOT/f'grethel-clean-{mode}.excalidraw').write_text(json.dumps(scene,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return scene

def luminance(h):
    v=[int(h[i:i+2],16)/255 for i in (1,3,5)]
    v=[x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in v]
    return sum(a*b for a,b in zip(v,[.2126,.7152,.0722]))

def contrast(a,b):
    low,high=sorted([luminance(a),luminance(b)])
    return round((high+.05)/(low+.05),3)

def validate(scene):
    ids={e['id'] for e in scene['elements']}
    assert len(ids)==len(scene['elements'])
    for e in scene['elements']:
        assert e['roughness']==0 and e['fillStyle']=='solid'
        assert all(math.isfinite(e[k]) for k in ['x','y','width','height'])
        assert e['width']>=0 and e['height']>=0
        assert e['type'] in ['rectangle','text','arrow','line']
        for binding in ['startBinding','endBinding']:
            if e.get(binding): assert e[binding]['elementId'] in ids
        for bound in e.get('boundElements') or []: assert bound['id'] in ids
    edges=[e for e in scene['elements'] if e['type']=='arrow']
    assert len(edges)==5
    for e in edges:
        src=e['startBinding']['elementId']; dst=e['endBinding']['elementId']
        assert src!=dst

def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    summary={}
    for mode in PALETTES:
        scene=build(mode);validate(scene)
        summary[mode]={'elements':len(scene['elements']),'arrows':5,'png':[3200,1800],
                      'accentOnCanvasContrast':contrast(PALETTES[mode]['accent'],PALETTES[mode]['canvas']),
                      'textOnCanvasContrast':contrast(PALETTES[mode]['text'],PALETTES[mode]['canvas']),
                      'mutedOnCanvasContrast':contrast(PALETTES[mode]['textMuted'],PALETTES[mode]['canvas'])}
    tokens={'name':'Grethel Clean','version':'0.1.0','status':'proposed-design-tokens',
            'description':'Semantic design proposal. Not a currently supported excaliplant configuration schema.',
            'brand':{'ink':'#111827','offWhite':'#F7F8FA','teal':'#2DB8A8'},
            'modes':PALETTES,
            'geometry':{'strokeWidth':2,'roughness':0,'fillStyle':'solid','strokeStyle':'solid',
                        'nodeCornerRadius':8,'nodePadding':24,'minimumNodeGap':48},
            'typography':{'family':'Liberation Sans, Arial, sans-serif',
                          'excalidrawFontFamily':9,'nodeTitle':26,'nodeSubtitle':17,'edgeLabel':17,
                          'lineHeight':1.25},
            'rendering':{'useExplicitPalette':True,'applyAutomaticDarkFilter':False,
                         'notes':'The supplied Dark scene intentionally uses the light editor rendering mode to avoid automatic color inversion. The document palette is dark.'},
            'contrastChecks':summary,
            'sources':[
                'https://plus.excalidraw.com/docs/sdk/codebase/json-schema',
                'https://plus.excalidraw.com/docs/sdk/excalidraw/api/props/initialdata',
                'https://github.com/excalidraw/excalidraw/blob/master/packages/common/src/constants.ts',
                'https://github.com/excalidraw/excalidraw/blob/master/packages/element/src/types.ts']}
    (ROOT/'grethel-clean.tokens.json').write_text(json.dumps(tokens,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (ROOT/'README.txt').write_text('''Grethel Clean — Diagramm-Thema (Entwurf)\n\nDateien pro Modus: PNG (3200 × 1800), SVG (Vektor), .excalidraw (bearbeitbar).\nPNG und SVG sind deterministisch erzeugte Designreferenzen. Sie wurden nicht von excaliplant exportiert.\nDie JSON-Datei enthält vorgeschlagene semantische Tokens, keine bereits unterstützte excaliplant-Konfiguration.\n\n.excalidraw öffnen: Datei in Excalidraw importieren. Texte und Formen sind editierbar.\nKnoten und ihre Beschriftungen sind gruppiert; Pfeile verweisen auf die verbundenen Knoten.\nDie Dark-Datei verwendet absichtlich theme=light und exportWithDarkMode=false, damit\ndie explizite dunkle Farbpalette nicht durch den automatischen Dark-Filter invertiert wird.\n\nSchrift in der editierbaren Datei: Excalidraw Liberation Sans (fontFamily=9).\nSVG/PNG: Liberation Sans. Text ist im SVG als Pfad enthalten;\ndadurch benötigt die Bilddatei keine externen Schriftdateien.\nSchriftfamilie 9 entspricht dem aktuellen offiziellen Excalidraw-Schema. Ältere Versionen können abweichen.
Die gewünschte Rundung beträgt 8 px; die jeweilige Editor-Version kann adaptive Radien anders interpretieren.\n\nValidierung: JSON-Struktur, eindeutige Element-IDs, Verweise, fünf gerichtete Verbindungen,\nFarbkontraste sowie gerenderte PNG-Layouts geprüft. Kein Live-Importtest im Web-Editor.\n''',encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
