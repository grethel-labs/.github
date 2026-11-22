# Grethel Clean: Light/Dark-Designpresets für Excalidraw-, SVG- und PNG-Diagramme

**Ziel-Repository:** [grethel-labs/excaliplant](https://github.com/grethel-labs/excaliplant)

## Problem und Ziel

Das neue Grethel-Labs-Branding verwendet eine reduzierte Formensprache, neutrale Sans-Serif-Typografie und Dunkelblau, Off-White sowie einen sparsamen Teal-Akzent. Diagramme sollen dieselbe Gestaltung übernehmen und als editierbare Excalidraw-Szenen sowie als SVG/PNG konsistent aussehen.

Gewünscht sind zwei zusätzliche Presets: **Grethel Clean Light** und **Grethel Clean Dark**. Beide sollen dieselben Diagramminhalte, Formen und semantischen Beziehungen darstellen. Nur die Farbvariante wechselt. Vorhandene Themes und das bisherige Standardverhalten bleiben erhalten.

Es geht um die Gestaltung der erzeugten Diagramme, nicht um ein neues Farbschema für die Excalidraw-Bedienoberfläche.

## Ausgangspunkt im vorhandenen Code

Referenzstand: Commit [`714be18084842730a5630ec33cd98a80fd25ea5a`](https://github.com/grethel-labs/excaliplant/commit/714be18084842730a5630ec33cd98a80fd25ea5a).

- [`src/draw/theme.mjs`](https://github.com/grethel-labs/excaliplant/blob/714be18084842730a5630ec33cd98a80fd25ea5a/src/draw/theme.mjs) enthält bereits `THEMES`, `THEME_NAMES`, rollenbasierte Farben sowie `roughness`, `edgeRoughness`, `strokeWidth`, `fillStyle` und eine Serienpalette.
- [`src/core/pipeline.mjs`](https://github.com/grethel-labs/excaliplant/blob/714be18084842730a5630ec33cd98a80fd25ea5a/src/core/pipeline.mjs) wählt das Theme über `options.theme` beziehungsweise `!theme` und wendet anschließend `skinparam`-/`<style>`-Werte an. `sketch: false` ist bereits vorhanden.
- Eine andere Schrift ist noch keine vollständige Theme-Eigenschaft: [`Canvas.text`](https://github.com/grethel-labs/excaliplant/blob/714be18084842730a5630ec33cd98a80fd25ea5a/src/draw/canvas.mjs) verwendet derzeit Excalifont beziehungsweise eine Monospace-Schrift; [`src/render/svg.mjs`](https://github.com/grethel-labs/excaliplant/blob/714be18084842730a5630ec33cd98a80fd25ea5a/src/render/svg.mjs) und [`src/render/font.mjs`](https://github.com/grethel-labs/excaliplant/blob/714be18084842730a5630ec33cd98a80fd25ea5a/src/render/font.mjs) sind ebenfalls auf Excalifont ausgerichtet. Die [Architektur](https://github.com/grethel-labs/excaliplant/blob/714be18084842730a5630ec33cd98a80fd25ea5a/docs/architecture.md) beschreibt die Textvermessung mit dessen Metriken.

Die Umsetzung sollte dieses Theme-System erweitern. Ein zusätzlicher, paralleler Styling-Mechanismus ist nicht erforderlich.

## Gewünschte Presets und Bedienung

Vorgeschlagene Preset-Namen:

- `grethel-clean-light`
- `grethel-clean-dark`

Die folgenden Beispiele beschreiben den **Soll-Zustand**. Die neuen Presets sind noch nicht implementiert; die verwendeten API- und CLI-Einstiegspunkte existieren bereits.

```js
import { render } from "@grethel-labs/excaliplant";

const result = await render(source, { theme: "grethel-clean-light" });
const scene = result.excalidraw;
const svg = await result.toSvg();
const png = await result.toPng({ width: 1600 });
```

```sh
npx excaliplant diagram.puml --theme grethel-clean-dark -o diagram.svg
```

```plantuml
@startuml
!theme grethel-clean-light
participant Client
participant API
Client -> API : Anfrage
API --> Client : Antwort
@enduml
```

Die neuen Presets verwenden bereits standardmäßig gerade Linien; ein zusätzliches `--clean` ist dafür nicht nötig.

## Verbindliche Farbwerte

Die ersten drei Markenfarben sind `#111827`, `#F7F8FA` und `#2DB8A8`. Die weiteren Werte sind funktionale Abstufungen für lesbare Diagramme, keine zusätzlichen Markenakzente.

| Funktion | Grethel Clean Light | Grethel Clean Dark |
| --- | --- | --- |
| Zeichenfläche | `#F7F8FA` | `#111827` |
| Knotenfläche | `#FFFFFF` | `#192231` |
| Haupttext | `#111827` | `#F7F8FA` |
| Sekundärtext | `#526173` | `#B6C2D1` |
| Knotenrand / neutrale Verbindung | `#64748B` | `#7A8AA0` |
| Untergeordnete Trennlinie | `#D4DAE2` | `#334155` |
| Akzent für lesbaren Text / Pfeile | `#117C70` | `#2DB8A8` |
| Zurückhaltende Akzentfläche | `#E5F6F2` | `#143A3B` |
| Dekorativer Markenakzent | `#2DB8A8` | `#2DB8A8` |

Auf hellem Grund wird für kleine Akzentbeschriftungen und wesentliche dünne Kanten das dunklere Teal verwendet. Das helle Marken-Teal bleibt dort auf dekorative Elemente beschränkt. Bedeutung wird zusätzlich durch Beschriftung, Form oder Linientyp vermittelt.

### Rollen und Gestaltung

- Standardknoten, Klassen, Komponenten und Teilnehmer: neutrale Fläche, kontrastreicher Text, dezenter Rand.
- Hervorgehobene Elemente: Akzentfläche und Akzentrand; sparsam einsetzen. Standardmäßig nicht jeden Knoten hervorheben.
- Verbindungen: neutrale Linien; Akzent nur für ausdrücklich hervorgehobene Pfade. Gestrichelte Rückgaben, Abhängigkeiten und Lebenslinien behalten ihre semantische Darstellung.
- Gruppen, Packages und Frames: transparenter oder neutraler Hintergrund; untergeordnete Linien und klare Überschrift.
- Notizen: neutrale oder helle Akzentfläche; kein automatisch gelber Haftnotizzettel-Stil.
- Serien und Äste: zurückhaltende, deterministische Palette aus den definierten Abstufungen. Bei mehreren Kategorien helfen zusätzlich Labels, Marker oder Linienstile.
- Keine Schraffuren, Schatten, Verläufe, Illustrationen oder automatischen Logos/Wasserzeichen im Diagramminhalt.

## Geometrie und Typografie

- `roughness: 0` und `edgeRoughness: 0` als Preset-Standard.
- `fillStyle: "solid"`; solide Standardkonturen, sofern der Diagrammtyp oder die Quelle keinen anderen Linientyp verlangt.
- Knotenränder und Hauptverbindungen: 2 px; untergeordnete Trennlinien: 1 px.
- Dezente Rechteckrundung. Die Designreferenz verwendet 8 px; eine feste Radiussteuerung ist gegebenenfalls eine Erweiterung, da der aktuelle Theme-Stil nur `rounded` als Boolean anbietet. Excalidraw- und SVG-Ergebnis müssen hierbei übereinstimmen.
- Vorhandenes semantisches Layout und typabhängige Formen erhalten. Ein Theme darf zum Beispiel keine Entscheidungsraute in eine gewöhnliche Box verwandeln.
- Neutrale Sans-Serif-Schrift statt Handschrift. Zielschrift: **Liberation Sans**; die offizielle Excalidraw-Zuordnung ist `FONT_FAMILY["Liberation Sans"]` (derzeit `9`). Beispielgröße für Knoten: 20 px, sekundäre Angaben: 16 px. Titelgrößen sollen die vorhandene Rollen-Hierarchie erhalten.

**Schriftunterstützung gehört zum Umfang dieses Issues:** Theme-Auswahl, Textvermessung, Zeilenumbruch, Canvas-Text, SVG-Schrifteinbettung und PNG-Rasterisierung müssen dieselbe Schrift und passende Metriken verwenden. Eine Änderung nur am SVG-CSS oder nur an `fontFamily` im JSON reicht nicht aus. Die Schrift muss mit passender Lizenz lokal verfügbar sein; der Renderpfad darf dafür keine Netzwerkverbindung benötigen. Die Excalifont-Voreinstellungen der bisherigen Themes bleiben bestehen.

Referenz für die offiziellen Familien: [Excalidraw-Konstanten](https://github.com/excalidraw/excalidraw/blob/master/packages/common/src/constants.ts).

## Priorität und Excalidraw-Dark-Mode

Die bestehende Auswahlpriorität beibehalten: explizites API-/CLI-Theme vor `!theme`, danach der bisherige Default. `skinparam`, `<style>` und explizite Elementstile sollen die unterstützten Preset-Werte weiterhin überschreiben können. Entsprechende Konfliktfälle testen, statt ein neues, undokumentiertes Prioritätssystem einzuführen.

`sketch: false` muss weiterhin glatte Konturen erzwingen; ein explizites `sketch: true` soll das bereits vorhandene Verhalten beibehalten. Die Presets selbst sind standardmäßig clean.

Für Dark-Diagramme sind die tatsächlichen Elementfarben und `viewBackgroundColor` maßgeblich. Excalidraw besitzt zusätzlich einen UI-Dark-Mode mit Farbfilter. Eine bereits dunkle Palette darf nicht unbeabsichtigt nochmals invertiert werden. Die Referenzdateien verwenden deshalb eine explizite dunkle Szene mit `appState.theme: "light"` und `exportWithDarkMode: false`. Diese Unterscheidung dokumentieren und im unterstützten Excalidraw-Frontend prüfen.

## Umsetzung und Nachweise

1. Beide Presets in `src/draw/theme.mjs` ergänzen, einschließlich aller bestehenden semantischen Rollen und einer geeigneten Serienpalette. `THEME_NAMES`, die CLI-Hilfe und die Zuordnung von `!theme` müssen sie korrekt aufführen beziehungsweise auflösen.
2. Font-Unterstützung in Theme-/Canvas-/Layout-/Renderpfad gemeinsam ergänzen; sonstige Themes unverändert lassen. Neue Konfigurationsfelder als neue API dokumentieren.
3. Beispielquellen für Component/Deployment, Sequence, Class und Activity in `examples/` ergänzen oder vorhandene geeignete Beispiele wiederverwenden; beide Farbvarianten in der Galerie zeigen.
4. Vorhandene Tests in `test/api.test.mjs`, `test/cli.test.mjs` und `test/examples.test.mjs` gezielt erweitern. Für Layout und Export die vorhandenen visuellen Tests der jeweiligen Diagrammfamilie ergänzen.

### Akzeptanzkriterien

- [ ] Beide Presets sind über JavaScript, CLI und `!theme` auswählbar; unbekannte Namen dürfen nicht versehentlich als erfolgreicher Grethel-Render durchgehen.
- [ ] Light und Dark verwenden die oben festgelegten Farben und dieselbe Geometrie, Schrift und Informationshierarchie.
- [ ] Ein ungestyltes Referenzdiagramm enthält glatte Konturen ohne Schraffuren; semantische Strichelungen und Pfeilspitzen bleiben korrekt.
- [ ] Formen, Beschriftungen und gebundene Pfeile bleiben in der exportierten `.excalidraw`-Datei editierbar.
- [ ] Knoten- und Kantenbeschriftungen werden mit der tatsächlich verwendeten Sans-Schrift vermessen; lange deutsche Labels, Umlaute, Mehrzeiler und Monospace-Abschnitte passen ohne Clipping.
- [ ] `.excalidraw`, SVG und PNG zeigen dieselbe Palette, Schrift, Rundung, Zeilenumbrüche und Diagrammstruktur; Light und Dark werden jeweils geprüft.
- [ ] Der Dark-Export wird beim vorgesehenen Import-/Exportpfad nicht doppelt invertiert.
- [ ] Explicit Theme, `!theme`, `skinparam`, `<style>`, Inline-Stile und `sketch` sind mit mindestens einem gezielten Konfliktfall abgedeckt.
- [ ] Gleiche Quelle, Optionen und Seed liefern weiterhin deterministische Ergebnisse; vorhandene Themes und bisherige Default-Ausgaben bleiben unverändert.
- [ ] Dokumentation, Galerie und Schriftlizenz-Hinweise sind aktualisiert; `npm run check` besteht.

## Designreferenzen

Die separat gelieferten Light-/Dark-Diagrammvorschauen und editierbaren Beispielszenen sind die visuelle Referenz. Die zusätzliche Token-Datei beschreibt die Sollwerte; sie ist keine bereits unterstützte excaliplant-Konfigurationsdatei.

Bei Veröffentlichung dieses Issues die beiden PNG-Vorschauen sowie Token- und Beispieldateien anhängen oder durch dauerhafte Repository-Links ersetzen.
