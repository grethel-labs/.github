GRETHEL CLEAN 2.0 — LIGHT / DARK

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
contrast-report.json         150 konkret geprüfte Kontrastpaare
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
body { background: var(--gl-bg-canvas); color: var(--gl-text-primary); }
.card { background: var(--gl-bg-surface); border: 1px solid var(--gl-border-subtle); }
.button { background: var(--gl-accent-solid); color: var(--gl-accent-foreground); }
.button:hover { background: var(--gl-accent-hover); }
.button:active { background: var(--gl-accent-active); }
.button:focus-visible { outline: 2px solid var(--gl-focus-ring); outline-offset: 2px; }

BRAND UND BEDIENOBERFLÄCHE
Brand-Teal ist konstant und für Logos/Dekor geeignet. Auf hellem Grund sind
accent-text beziehungsweise text-link für Text vorgesehen. Primäre Buttons:
Light #117C70 mit weißer Schrift; Dark #2DB8A8 mit Ink-Schrift. Weiß auf dem
hellen Brand-Teal erreicht nur 2.46:1; Ink darauf 7.21:1.
border-subtle und chart-grid sind dekorativ. Wesentliche Grenzen erhalten
control-border/border-default; wichtige Diagrammlinien erhalten chart-axis.

GRENZEN
150/150 geprüfte Paarungen erreichen 4,5:1 für Normaltext beziehungsweise
3:1 für wesentliche UI-Informationen. Dies ist keine vollständige
WCAG-Konformitätsbewertung. Nicht beliebig Tokens kombinieren. Bilder, Alpha,
Fokus-Geometrie, alle Nachbarfarben und tatsächliches Rendering in der Anwendung
prüfen. Status und Diagrammserien zusätzlich beschriften oder durch Formen/
Linienstile unterscheiden; Farbe allein genügt nicht.

QUELLEN
https://www.radix-ui.com/colors/docs/palette-composition/understanding-the-scale
https://github.com/radix-ui/colors/blob/main/src/light.ts
https://github.com/radix-ui/colors/blob/main/src/dark.ts
https://github.com/radix-ui/colors/blob/main/LICENSE
https://www.w3.org/TR/WCAG22/#contrast-minimum
https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html
