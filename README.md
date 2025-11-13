# Polizei Frankfurt – Datenanalyse-Projekt

Dieses Projekt demonstriert eine vollständige Datenanalyse-Pipeline für polizeiliche Ermittlungsdaten, wie sie beim **Polizeipräsidium Frankfurt am Main, K36 – Auswertung und Analyse** eingesetzt werden könnten.

## Projektübersicht

Das Projekt simuliert realistische Ermittlungsdaten inklusive:

- Vorfallsdaten mit geografischen Koordinaten  
- Verdächtigendatenbank  
- Kommunikationsnetzwerk-Daten  
- Standort-Hotspot-Analysen  

Es demonstriert die Kernkompetenzen für die Position:

- Massendatenauswertung und -analyse  
- Geografische Visualisierung (Crime Heatmaps)  
- Dashboard-Erstellung mit Python  
- SQL-Datenbankmanagement und Abfrageoptimierung  
- Automatisierungsskripte für wiederkehrende Aufgaben  
- Statistische Analysen und Mustererkennung  

## Technologien

- Python 3.8+  
- Pandas (Datenmanipulation und -analyse)  
- SQLite (relationale Datenbank)  
- Matplotlib / Seaborn (Visualisierungen und Dashboards)  
- NumPy (numerische Berechnungen)  
- Faker (synthetische Datengenerierung)  

## Projektstruktur

polizeipräsidium/
├── config.py # Zentrale Konfiguration
├── db_create.py # ETL-Pipeline
├── analyse.py # Statistische Analysen & Dashboard
├── geo_analysis.py # Geografische Analysen & Heatmaps
├── automation_scripts/
│ ├── data_cleaner.py # Datenbereinigung
│ ├── report_generator.py # Berichtserstellung
│ └── batch_processor.py # Batch-Verarbeitung
├── data/
│ ├── raw/ # Rohdaten (CSV, JSON)
│ └── processed/ # SQLite-Datenbank
├── output/ # Analyseergebnisse & Visualisierungen
└── README.md


## Installation und Ausführung

### Voraussetzungen

- Python 3.8 oder höher  
- pip  

### Installation

```bash
# Repository klonen
git clone https://github.com/mignocharly/polizeipräsidium.git
cd polizeipräsidium

# Virtuelle Umgebung erstellen
python -m venv venv
venv\Scripts\activate  # Windows
# oder
source venv/bin/activate  # Linux/Mac

# Abhängigkeiten installieren
pip install -r requirements.txt

Ausführung
# Schritt 1: Daten generieren und ETL durchführen
python db_create.py

# Schritt 2: Statistische Analysen und Dashboard erstellen
python analyse.py

# Schritt 3: Geografische Analysen (Crime Heatmaps)
python geo_analysis.py

# Optional: Automatisierungsskripte
python automation_scripts/data_cleaner.py

Generierte Datensätze
1. Vorfallsdaten (incidents)

Aktenzeichen, Deliktskategorie, Datum, Uhrzeit

Koordinaten (Latitude, Longitude)

Stadtteile (Frankfurt-Distrikte)

Status, Priorität, Schadenshöhe, Zeugenzahl

2. Verdächtige (suspects)

Verdächtigen-ID, Alter, Geschlecht, Nationalität

Vorstrafen, Haftstatus, Risikobewertung, Wohnbezirk

3. Standorte (locations)

Hotspot-Koordinaten, Stadtteil, Vorfallshäufigkeit

Durchschnittliche Reaktionszeit

4. Kommunikationsdaten (communications)

Kommunikationstyp (Telefon, SMS, WhatsApp, etc.)

Sender/Empfänger-Netzwerk

Verschlüsselungsstatus, Relevanzbewertung

Analyseergebnisse
dashboard_overview.png

Top-Deliktskategorien

Fallstatus-Verteilung

Prioritätsanalyse

Zeitliche Trends

Stadtteil-Ranking

crime_heatmap.png

Geografische Verteilung nach Deliktart

Stadtteil-Ranking

Hotspot-Identifikation

temporal_patterns.png

Wochentag- und Zeitmuster

Deliktkategorien-Trends

Prioritätsverteilung über Zeit

network_analysis.png

Kommunikationsnetzwerk

Verschlüsselungs- und Relevanzanalyse

statistical_report.csv

Statistische Kennzahlen und Korrelationen

Besondere Features
SQL-Datenbank mit Optimierungen

Indexierte Tabellen

SQL Views für wiederkehrende Analysen

Foreign Key Relationships

Automatisierungsskripte

data_cleaner.py: automatische Datenvalidierung

report_generator.py: automatisierte Berichtserstellung

batch_processor.py: Stapelverarbeitung

Dashboard-Visualisierungen

Mehr als 12 Analysegrafiken

Hochauflösender PNG-Export (300 DPI)

Geovisualisierung

Crime Heatmaps mit echten Frankfurt-Koordinaten

Stadtteilbasierte Clusteranalysen

Bezug zur Stellenausschreibung

Dieses Projekt demonstriert alle geforderten Kompetenzen für die Stelle:

Massendatenauswertung: über 2.500 Vorfälle und 5.000 Kommunikationsdaten

Python-Programmierung (OOP, Skriptstrukturierung)

SQL-Datenbankmodellierung und Optimierung

Datenvisualisierung und Dashboard-Erstellung

Geo-Analysen und Heatmaps

Automatisierung von Analyseprozessen

Statistische und explorative Analysen

Ausführliche Code-Dokumentation

Nutzung in der Bewerbung

Im Anschreiben kann erwähnt werden:

Zur Vorbereitung auf diese Position habe ich ein praxisnahes Datenanalyse-Projekt entwickelt, das die Kernaufgaben der Stelle widerspiegelt.

Das Projekt umfasst:

ETL-Pipelines für polizeiliche Massendaten

SQL-Datenbankarchitektur mit Indexierung

Dashboard-Visualisierungen und Crime Heatmaps

Automatisierungsskripte für wiederkehrende Analysen


Kontakt

Entwickelt als Portfolio-Projekt für die Bewerbung beim
Polizeipräsidium Frankfurt am Main – K36 Auswertung und Analyse

Autor: Charles Nguenkam
E-Mail: charles.nguenkam@gmail.com

GitHub: https://github.com/mignoncharly