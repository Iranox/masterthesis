<?php

require_once("header.php");
require_once("footer.php");

$content='<h2 align="center">Daten <h2/>

<h3>Zeugnisse</h3>
<p>
In Rahmen eines Digitalisierungsprozess wurden verschiedene Zeugnisse aus dem Archiv
eingescannt. Dabei wurden schwarz-weiß Bilder erstellt. Bei einigen Schülern sind
mehrere Zeugnisse vorhanden, welche ebenfalls eingescannt wurden. Die Dateien wurden
jeweils mit der Matrikelnummer des Schülers benannt, damit diese eindeutig zuordnen kann.
Falls es mehrere Zeugnisse für einen Schüler gibt, ist die Version im Dateinamen vermerkt. </p>
<br /> <p>
Auf den Zeugnissen sind jeweils die Fächer vermerkt, in welchen die Studenten
geprüft wurden. Dabei wurde eine verbale Einschätzung von den jeweiligen Dozenten
vermerkt. Anschließend ist die Unterschrift des jeweiligen Dozenten vermerkt.</p>

<h2>Metadaten</h2>
<p>
Während des Digitalisierungsprozess wurden für jedes Zeugnis ein Eintrag in eine
csv-Datei festgehalten. Dabei wurden die Schülernamen, Herkunft, Matrikelnummer
und ähnliches festgehalten. Die jeweiligen Lehrer wurden allerdings nicht festgehalten.
Die Lücke soll durch das Projekt geschlossen werden.</p>';

echo myHeader().($content).myFooter();
