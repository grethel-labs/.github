"""Build exact, scalable Grethel technical backgrounds from the shared SVG master."""
from pathlib import Path
import json
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MASTER = json.loads((ROOT / 'svg' / 'master-paths.json').read_text())
MARK = MASTER['mark']

PALETTES = {
    'light': {'canvas': '#F7F8FA', 'grid': '#E6EBF1', 'body': '#E3EAF0', 'edge': '#CAD6E1', 'accent': '#2DB8A8'},
    'dark': {'canvas': '#111827', 'grid': '#1B283A', 'body': '#1D2C40', 'edge': '#2D425C', 'accent': '#2DB8A8'},
}

for mode, c in PALETTES.items():
    markup = f'''<svg xmlns="http://www.w3.org/2000/svg" width="3840" height="2160" viewBox="0 0 1920 1080" role="img" aria-labelledby="title desc">
  <title id="title">Grethel Labs technical background — {mode}</title>
  <desc id="desc">Quiet left content area; precise grid and an oversized flask-G on the right. Scalable vector artwork.</desc>
  <defs>
    <pattern id="grid" width="48" height="48" patternUnits="userSpaceOnUse"><path d="M 48 0 H 0 V 48" fill="none" stroke="{c['grid']}" stroke-width="1"/></pattern>
    <clipPath id="right"><rect x="1032" y="0" width="888" height="1080"/></clipPath>
  </defs>
  <rect width="1920" height="1080" fill="{c['canvas']}"/>
  <rect x="1032" width="888" height="1080" fill="url(#grid)"/>
  <g clip-path="url(#right)">
    <g transform="translate(1175 240) scale(1.25)">
      <path d="{MARK['base_path']}" fill="{c['body']}"/>
      <path d="{MARK['base_path']}" fill="none" stroke="{c['edge']}" stroke-width="1.25"/>
      <path d="{MARK['accent_path']}" fill="{c['accent']}"/>
    </g>
  </g>
  <path d="M 1080 168 h 40 M 1100 148 v 40 M 1776 960 h 48 v -48" stroke="{c['edge']}" stroke-width="2" fill="none"/>
  <path d="M 1784 72 h 64 v 64" stroke="{c['accent']}" stroke-opacity="0.55" stroke-width="2" fill="none"/>
</svg>'''
    svg = HERE / f'technical-grid-{mode}.svg'
    svg.write_text(markup + '\n')
    png = HERE / f'technical-grid-{mode}-4k.png'
    subprocess.run(['inkscape', str(svg), '--export-type=png', f'--export-filename={png}', '--export-width=3840', '--export-height=2160'], check=True, capture_output=True)
    print(png.name)
