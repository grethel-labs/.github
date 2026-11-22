GRETHEL LABS — BRAND GUIDELINES V2

1. MARKENZEICHEN

Das Kolben-G verbindet den Laborbezug mit dem Anfangsbuchstaben der Marke. Hals, schräge Schulter, offene rechte Kontur und innerer Querbalken bilden ein gemeinsames Zeichen. Der Teal-Akzent sitzt am inneren Ende des Querbalkens. Diese Beziehungen sollen in allen Anwendungen erhalten bleiben.

Die Vektorversionen normalisieren die Konturen der freigegebenen Rastervorlage. Kleine Unterschiede bei Kurven, Kanten und Abständen sind dabei möglich. Für neue skalierbare Anwendungen dienen die SVG-Master als konsistente Grundlage; die bisherigen PNG-Motive bleiben als ursprüngliche Bildvarianten erhalten.

2. DATEIFORMATE UND VARIANTEN

SVG eignet sich für Websites, Dokumentation und skalierbare Druckvorlagen. Die Logos enthalten echte Vektorpfade. Auch die Wortmarke wird als Pfad dargestellt, damit ihre Erscheinung nicht von einer lokal installierten Schrift abhängt. Sie ist dadurch keine normal editierbare Textzeile. Farbänderungen erfolgen an den Füllungen der vorgesehenen Varianten.

svg/master-mark.svg ist die gemeinsame Signet-Grundlage. svg/master-paths.json enthält die wiederverwendbaren Pfaddaten. Die Wortmarke wurde aus der akzeptierten Bildvorlage vektorisiert; sie wird nicht durch eine andere Schrift ersetzt.

Das gefüllte farbige Signet ist die Standardversion. Die einfarbige Version eignet sich für Anwendungen mit nur einer Druck- oder Zeichenfarbe und als Ausgangspunkt für kleine Icons. Outline- und Konstruktionsvarianten sind für größere, dekorative Flächen gedacht. Ihre zusätzlichen Linien sollen nicht in kleinen UI-Symbolen verschwinden.

Die Wort-/Bildmarke mit „Grethel Labs“ verwenden, wenn der Name erstmals sichtbar wird oder die Marke nicht bereits aus dem Kontext hervorgeht. Das einzelne Signet passt zu Profilbildern, App-Symbolen und wiederkehrenden Bedienelementen. Eine inverse helle Variante ist für dunkle Flächen vorgesehen.

3. ABSTÄNDE UND KLEINE DARSTELLUNG

Als praktische Schutzraum-Regel rund um das Zeichen mindestens eine Strichbreite des G freilassen. Der Schutzraum gehört zusätzlich zum eigentlichen Zeichen. Logo und Wortmarke proportional skalieren; nicht unabhängig voneinander verzerren oder stauchen.

Bei Profilbildern den vorgesehenen Freiraum erhalten und den tatsächlichen runden Zuschnitt prüfen. Für sehr kleine Icons die gefüllte oder einfarbige Version in der Zielgröße ansehen, beispielsweise bei 16, 24 und 32 Pixeln. Öffnung, Querbalken und Flaschenhals müssen getrennt erkennbar bleiben. Eine allgemeingültige Mindestgröße wird nicht zugesichert; Rasterung, Display und Hintergrund beeinflussen das Ergebnis.

4. FARBEN UND THEMES

Die drei festen Markenfarben sind:

Ink       #111827 — dunkle Grundfarbe
Off-White #F7F8FA — helle Grundfarbe
Teal      #2DB8A8 — Markenakzent

Die UI-Themes ergänzen diese Basis um abgestufte Flächen, lesbare Textfarben, Rahmen, Fokuszustände und Funktionsfarben. Diese Abstufungen sind keine zusätzlichen gleichrangigen Logo-Farben. Teal bleibt der visuelle Schwerpunkt; Statusfarben markieren gezielt Erfolg, Warnung, Fehler oder Information.

In einer Oberfläche semantische Rollen verwenden, etwa für Hintergrund, Text oder Akzent, statt einzelne Hexwerte über viele Komponenten zu verteilen. Light und Dark verwenden passende eigene Zuordnungen. Ein Dark-Theme entsteht daher nicht durch pauschales Invertieren aller Farben. Die Dokumentation im Ordner theme beschreibt die konkrete CSS-Einbindung und die explizite Moduswahl.

theme/grethel-theme.css enthält die CSS-Variablen. Ohne explizite Auswahl folgt der Modus der Systemeinstellung; data-theme="light" oder data-theme="dark" wählt ihn ausdrücklich. Die aufgelösten Werte stehen in theme/grethel-theme.tokens.json. palette-light.png und palette-dark.png zeigen die wichtigsten Rollen als visuelle Übersicht. Helle Akzentbuttons verwenden funktionales Dunkel-Teal mit weißer Schrift; im dunklen Theme wird Marken-Teal mit Ink kombiniert.

Für Text auf hellem Marken-Teal dunkles Ink bevorzugen. Wo Teal selbst als kleiner Text oder wesentliche Kontur auf einer hellen Fläche erscheint, ist eine kontrastreichere funktionale Abstufung vorgesehen. Maßgeblich sind die geprüften Vordergrund-/Hintergrund-Paare im Kontrastbericht. Einzelne bestandene Paarprüfungen sind keine allgemeine Aussage über die Barrierefreiheit einer fertigen Anwendung. Status zusätzlich mit verständlichen Labels oder Formen vermitteln.

theme/contrast-report.json dokumentiert die geprüften Paare. Die Skalenarchitektur orientiert sich an Radix Colors und wurde um eigene Grethel-Abstufungen ergänzt. Quellen und Lizenzhinweise für übernommene Funktionsfarben stehen bei den Theme-Dateien.

5. HINTERGRÜNDE UND DETAILSTUFEN

Hintergrundmotive lassen freie Fläche für Inhalte. Text und Bedienelemente in den ruhigen Bereichen platzieren; das große Logo oder die Detailstruktur darf die Lesbarkeit nicht stören. Den Ausschnitt an das Zielformat anpassen und dabei wichtige Markenteile sowie den Schutzraum berücksichtigen. Bei Bannern den sichtbaren Ausschnitt der jeweiligen Plattform prüfen.

Die reduzierte Gestaltung ist für alltägliche Produkt- und Dokumentationsflächen vorgesehen. Die detailreichere Gestaltung kann Titelbilder oder große Präsentationsflächen unterstützen. Nicht mehrere Detailmotive, Outline-Zeichen und Vollfarben-Logos auf engem Raum übereinanderlegen.

6. DIAGRAMME UND UMSETZUNGSSTATUS

Die mitgelieferten Excalidraw-Beispiele und das Diagramm-Issue sind Designreferenzen. Die erweiterten Theme-Tokens definieren ein eigenes Grethel-Labs-Farbsystem und sind keine bereits implementierte excaliplant-Konfiguration. Eine Übernahme in die Software muss die dort vorhandenen Stilrollen und Exportpfade berücksichtigen.

Der Issue-Entwurf bleibt unveröffentlicht. Seine technischen Aussagen beziehen sich auf den darin dokumentierten Repository-Stand. Die separate Ergänzungsnotiz beschreibt die gewünschte Verbindung zwischen Markenassets, UI-Themes und Diagrammgestaltung, ohne neue öffentliche APIs vorauszusetzen.
