"""
Automated Data Cleaning Script
Demonstrates automation capabilities for data preprocessing
"""

import pandas as pd
import sqlite3
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))
import config


def clean_incident_data(df):
    """Clean and validate incident data"""
    print("Bereinige Vorfallsdaten...")
    
    # Remove duplicates
    initial_count = len(df)
    df = df.drop_duplicates(subset=['incident_id'])
    print(f"  Duplikate entfernt: {initial_count - len(df)}")
    
    # Validate geographic coordinates
    df = df[
        (df['latitude'].between(config.FRANKFURT_BOUNDS['lat_min'], config.FRANKFURT_BOUNDS['lat_max'])) &
        (df['longitude'].between(config.FRANKFURT_BOUNDS['lon_min'], config.FRANKFURT_BOUNDS['lon_max']))
    ]
    print(f"  Ungültige Koordinaten entfernt: {initial_count - len(df)}")
    
    # Fill missing damage estimates
    df['damage_estimate_eur'].fillna(0, inplace=True)
    
    # Standardize status values
    df['status'] = df['status'].str.strip()
    
    return df


def main():
    print("="*60)
    print("AUTOMATISIERTE DATENBEREINIGUNG")
    print("="*60)
    
    # Connect to database
    conn = sqlite3.connect(config.DATABASE_PATH)
    
    # Load incidents
    incidents = pd.read_sql_query("SELECT * FROM incidents", conn)
    print(f"\nGeladene Datensätze: {len(incidents)}")
    
    # Clean data
    incidents_clean = clean_incident_data(incidents)
    
    # Save cleaned data
    incidents_clean.to_sql('incidents_clean', conn, if_exists='replace', index=False)
    
    print(f"\n✓ Bereinigte Daten gespeichert: {len(incidents_clean)} Datensätze")
    print(f"✓ Neue Tabelle: incidents_clean")
    
    conn.close()


if __name__ == "__main__":
    main()