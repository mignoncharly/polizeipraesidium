"""
Configuration file for police data analytics project
"""
import os
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / 'data'
RAW_DATA_DIR = DATA_DIR / 'raw'
PROCESSED_DATA_DIR = DATA_DIR / 'processed'
OUTPUT_DIR = BASE_DIR / 'output'
AUTOMATION_DIR = BASE_DIR / 'automation_scripts'

# Create directories
for directory in [RAW_DATA_DIR, PROCESSED_DATA_DIR, OUTPUT_DIR, AUTOMATION_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Database configuration
DATABASE_PATH = PROCESSED_DATA_DIR / 'police_analytics.db'

# Data generation parameters
NUM_INCIDENTS = 5000
NUM_SUSPECTS = 1000
NUM_LOCATIONS = 300
NUM_COMMUNICATIONS = 10000

# Frankfurt districts (Stadtteile)
FRANKFURT_DISTRICTS = [
    'Altstadt', 'Innenstadt', 'Bahnhofsviertel', 'Westend-Süd', 'Westend-Nord',
    'Nordend-West', 'Nordend-Ost', 'Ostend', 'Bornheim', 'Sachsenhausen-Nord',
    'Sachsenhausen-Süd', 'Bockenheim', 'Gallus', 'Griesheim', 'Rödelheim',
    'Hausen', 'Praunheim', 'Niederursel', 'Ginnheim', 'Dornbusch',
    'Eschersheim', 'Eckenheim', 'Preungesheim', 'Bonames', 'Berkersheim',
    'Fechenheim', 'Höchst', 'Unterliederbach', 'Zeilsheim', 'Sindlingen',
    'Nied', 'Schwanheim', 'Sossenheim', 'Nieder-Erlenbach', 'Kalbach-Riedberg',
    'Harheim', 'Nieder-Eschbach', 'Bergen-Enkheim', 'Seckbach', 'Riederwald',
    'Frankfurter Berg'
]

# Crime categories
CRIME_CATEGORIES = [
    'Diebstahl', 'Körperverletzung', 'Betrug', 'Sachbeschädigung',
    'Einbruchdiebstahl', 'Raub', 'Drogendelikt', 'Verkehrsdelikt',
    'Unterschlagung', 'Erpressung', 'Beleidigung', 'Bedrohung',
    'Urkundenfälschung', 'Computerbetrug', 'Hausfriedensbruch'
]

# Incident status
INCIDENT_STATUS = ['Ermittlung läuft', 'Abgeschlossen', 'Eingestellt', 'Gerichtlich']

# Priority levels
PRIORITY_LEVELS = ['Niedrig', 'Mittel', 'Hoch', 'Dringend']

# Geographic bounds for Frankfurt am Main
FRANKFURT_BOUNDS = {
    'lat_min': 50.015,
    'lat_max': 50.195,
    'lon_min': 8.472,
    'lon_max': 8.800
}

# Communication types
COMM_TYPES = [
    'Telefonat', 'SMS', 'E-Mail', 'WhatsApp', 'Telegram',
    'Signal', 'Persönlicher Kontakt', 'Brief', 'Social Media'
]