## copy_checker (Arbeitstitel)

Dieser Ordner enthält verschiedene Pythonskripte, welche die Metadaten der
Schülerzeugnisse ergänzen. Zudem können diese Metadaten noch in RDF-Format
geparst werden.

### Abhängigkeiten installieren

Installieren von Python 3  und pip3 mit
  ```bash
  sudo apt-get install python3
  curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
  python3 get-pip.py --user
  ```
Installieren der Module mit pip3
```bash
  pip3 install -r requirements.txt
 ```

 ### Ausführen

Mit folgenden Befehl kann die Anzahl der Dateien pro Matrikel ermittelt werden:

```bash
python3 -p "path/to/folder"
 ```
 Dies erstellt eine csv-Datei mit Matrikel und die Anzahl der Dateien pro Matrikel.

 Mit folgenden Befehl kann man die Metadatendatei der HMT mit neuen Metadatenkombinieren:

```bash
python3 --csv1 "path/to/HMT1-6200.csv" --csv2 "path/to/neuenMetadaten"
 ```
Die Metadaten werden dabei in RDF überführt. 
