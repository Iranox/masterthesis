<?php

require_once("header.php");
require_once("footer.php");

$content='
<h2 align="center"> Lehrer-Schüler-Verbindungen</h2>
<h3> Hintergrund </h3>
<p>
Die Frage von Lehrer-Schüler-Verbindungen ist für die musikhistorische
Forschung von hoher Bedeutung. Zwar geben die Zeugnisse Aufschluss über die
Frage, welche/r Schülerin/Schüler von welchem Lehrer unterrichtet
wurde. </p> <p>Allerdings wurden diese bislang nie systematisch und umfassend,
höchstens im Einzelfall ausgewertet. Unbeantwortet bleibt im Umkehrschluss
bislang die Frage, welche Schüler*innen insgesamt von einem einzelnen Lehrer
unterrichtet wurden.</p><p>
Von einer Texterkennung und Auslese der Unterschriften auf den Zeugnissen
erhoffen wir uns hinsichtlich dieser Forschungsfrage Unterstützung. Durch
Clustern von ähnlichen Unterschriften und eine intellektuelle Zuordnung zu
Lehrernamen lassen sich bedeutende Informationen auslesen. Dabei stellt die
mögliche Anreicherung der Lehrernamen mit GND/VIAF-IDs einen zusätzlichen
Mehrwert dar.</font></p>';

echo myHeader().($content).myFooter();
