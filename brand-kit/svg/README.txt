GRETHEL LABS — SVG-MASTER UND VARIANTEN

16 eigenständige SVGs. Alle Logo- und Schriftformen bestehen aus nativen
Vektorpfaden. Keine eingebetteten Pixelbilder, externen Schriftdateien,
Skripte oder externen Ressourcen.

Farben
Ink       #111827
Off-white #F7F8FA
Teal      #2DB8A8

Varianten und natürliche Maße
master-mark.svg               600 × 600, farbiges Master-Signet
signet-color.svg              600 × 600, farbig
signet-mono.svg               600 × 600, einfarbig Ink
signet-inverse.svg            600 × 600, Off-white mit Teal
signet-outline.svg            600 × 600, Konturvariante
wordmark-ink.svg              951 × 119, Wortmarke Ink
wordmark-inverse.svg          951 × 119, Wortmarke Off-white
logo-horizontal-light.svg    1600 × 480
logo-horizontal-dark.svg     1600 × 480
logo-stacked-light.svg       1254 × 1254
logo-stacked-dark.svg        1254 × 1254
avatar-light.svg             1000 × 1000
avatar-dark.svg              1000 × 1000
banner-light.svg             2400 × 800, Verhältnis 3:1
banner-dark.svg              2400 × 800, Verhältnis 3:1
logo-construction.svg        1254 × 1254, dekorative Konstruktionsansicht

Light/dark bezeichnet die vorgesehene Hintergrundfläche. Die Standardlogos
sind transparent. Avatare, Banner und Konstruktionsansicht haben einen
expliziten Hintergrund. Outline und Konstruktion eignen sich für größere
Darstellungen; für kleine Icons das gefüllte Signet verwenden.

Wiederverwendung
master-paths.json enthält:
  colors.ink / colors.off_white / colors.teal
  mark.viewBox / mark.base_path / mark.accent_path / mark.fill_rule
  wordmark.viewBox / wordmark.path / wordmark.fill_rule

build_variants.py erzeugt alle SVGs aus diesen Pfaden neu und benötigt nur
die Python-Standardbibliothek. Die Wortmarke ist in Pfade umgewandelt;
sie benötigt keine Schriftdatei und ist kein direkt bearbeitbarer Text.

Referenz und Normalisierung
Die freigegebene Bildreferenz wurde in echte Vektoren rekonstruiert.
Gerade Signetkanten wurden ausgerichtet und Rundungen geglättet.
Die Wortmarke erhält die Schriftformen der Referenz als geglättete Konturen.
Flache Markenfarben ersetzen Rastertextur und Schattierung. Daher handelt
es sich nicht um eine pixelgenaue Kopie des generierten Ausgangsbilds.

Prüfung
validation.json dokumentiert XML-, Ressourcen- und Maßprüfung.
previews/ enthält für jedes SVG ein separates PNG mit doppelter Auflösung.
Diese Vorschauen haben für die Ansicht einen hellen oder dunklen
Hintergrund; die Transparenz der zugrunde liegenden SVGs bleibt erhalten.

PNG-Export mit Inkscape, beispielsweise:
inkscape master-mark.svg --export-type=png --export-filename=mark.png --export-width=1200
