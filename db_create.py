"""
ETL Pipeline for Police Investigation Data Analytics
Generates synthetic police data and creates normalized database
"""

import pandas as pd
import numpy as np
import sqlite3
import json
from datetime import datetime, timedelta
from faker import Faker
import random
import hashlib
import config

# Initialize Faker with German locale
fake = Faker('de_DE')
Faker.seed(42)
random.seed(42)
np.random.seed(42)


class PoliceDataGenerator:
    """Generate realistic synthetic police investigation data"""
    
    def __init__(self):
        self.fake = fake
        self.start_date = datetime(2023, 1, 1)
        self.end_date = datetime(2025, 11, 13)
    
    def generate_incident_id(self, index):
        """Generate unique incident identifier"""
        year = random.randint(2023, 2025)
        return f"AZ-{year}-{index:06d}"
    
    def random_date(self):
        """Generate random date within range"""
        delta = self.end_date - self.start_date
        random_days = random.randint(0, delta.days)
        return self.start_date + timedelta(days=random_days)
    
    def random_time(self):
        """Generate random time of day"""
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        return f"{hour:02d}:{minute:02d}"
    
    def generate_coordinates(self):
        """Generate random coordinates within Frankfurt bounds"""
        lat = random.uniform(
            config.FRANKFURT_BOUNDS['lat_min'],
            config.FRANKFURT_BOUNDS['lat_max']
        )
        lon = random.uniform(
            config.FRANKFURT_BOUNDS['lon_min'],
            config.FRANKFURT_BOUNDS['lon_max']
        )
        return round(lat, 6), round(lon, 6)
    
    def generate_incidents(self, n=config.NUM_INCIDENTS):
        """Generate incident data with geographic information"""
        print(f"Generating {n} incident records...")
        
        incidents = []
        for i in range(n):
            incident_date = self.random_date()
            incident_time = self.random_time()
            
            # Determine status and resolution date
            status = random.choices(
                config.INCIDENT_STATUS,
                weights=[0.40, 0.35, 0.15, 0.10],
                k=1
            )[0]  # Extract string from list
            
            if status in ['Abgeschlossen', 'Eingestellt', 'Gerichtlich']:
                days_to_resolve = random.randint(7, 365)
                resolved_date = incident_date + timedelta(days=days_to_resolve)
            else:
                resolved_date = None
            
            lat, lon = self.generate_coordinates()
            district = random.choice(config.FRANKFURT_DISTRICTS)
            
            incident = {
                'incident_id': self.generate_incident_id(i + 1),
                'crime_category': random.choice(config.CRIME_CATEGORIES),
                'incident_date': incident_date,
                'incident_time': incident_time,
                'district': district,
                'latitude': lat,
                'longitude': lon,
                'street_name': fake.street_name(),
                'priority': random.choice(config.PRIORITY_LEVELS),
                'status': status,
                'reported_by': random.choice(['Zeuge', 'Opfer', 'Patrouille', 'Notruf', 'Anonym']),
                'resolved_date': resolved_date,
                'officers_assigned': random.randint(1, 4),
                'damage_estimate_eur': round(random.uniform(0, 50000), 2) if random.random() > 0.3 else 0,
                'witnesses_count': random.randint(0, 5),
                'evidence_items': random.randint(0, 15)
            }
            incidents.append(incident)
        
        return pd.DataFrame(incidents)
    
    def generate_suspects(self, incidents_df, n=config.NUM_SUSPECTS):
        """Generate suspect data"""
        print(f"Generating {n} suspect records...")
        
        suspects = []
        incident_ids = incidents_df['incident_id'].tolist()
        
        for i in range(n):
            birth_year = random.randint(1960, 2007)
            
            suspect = {
                'suspect_id': f"VD-{i+1:06d}",
                'incident_id': random.choice(incident_ids),
                'name': fake.name(),
                'birth_year': birth_year,
                'age': 2025 - birth_year,
                'gender': random.choice(['Männlich', 'Weiblich', 'Divers']),
                'nationality': random.choice([
                    'Deutsch', 'Türkisch', 'Polnisch', 'Italienisch', 
                    'Rumänisch', 'Kroatisch', 'Syrisch', 'Afghanisch', 'Unbekannt'
                ]),
                'previous_offenses': random.randint(0, 15),
                'address_district': random.choice(config.FRANKFURT_DISTRICTS),
                'known_to_police': random.choice([True, False]),
                'arrest_status': random.choices(
                    ['Auf freiem Fuß', 'Festgenommen', 'U-Haft', 'Verurteilt', 'Flüchtig'],
                    weights=[0.50, 0.20, 0.10, 0.15, 0.05],
                    k=1
                )[0],  # Extract string from list
                'risk_level': random.choice(['Niedrig', 'Mittel', 'Hoch'])
            }
            suspects.append(suspect)
        
        return suspects
    
    def generate_locations(self, incidents_df, n=config.NUM_LOCATIONS):
        """Generate location hotspot data"""
        print(f"Generating {n} location records...")
        
        locations = []
        
        for i in range(n):
            lat, lon = self.generate_coordinates()
            
            location = {
                'location_id': f"LOC-{i+1:05d}",
                'location_name': random.choice([
                    fake.street_name(),
                    f"{fake.street_name()} / {fake.street_name()}",
                    fake.company() + ' Parkplatz',
                    f"U-Bahn {fake.word().capitalize()}",
                    'Hauptbahnhof',
                    'Römer',
                    'Zeil',
                    fake.city()
                ]),
                'district': random.choice(config.FRANKFURT_DISTRICTS),
                'latitude': lat,
                'longitude': lon,
                'location_type': random.choice([
                    'Straße', 'Kreuzung', 'Parkplatz', 'Öffentlicher Platz',
                    'Bahnhof', 'U-Bahn Station', 'Einkaufszentrum',
                    'Park', 'Wohngebiet', 'Gewerbegebiet'
                ]),
                'incident_count': random.randint(1, 50),
                'avg_response_time_min': random.randint(5, 45),
                'is_hotspot': random.choice([True, False])
            }
            locations.append(location)
        
        return pd.DataFrame(locations)
    
    def generate_communications(self, suspects_df, n=config.NUM_COMMUNICATIONS):
        """Generate communication records for network analysis"""
        print(f"Generating {n} communication records...")
        
        communications = []
        suspect_ids = suspects_df['suspect_id'].tolist()
        
        for i in range(n):
            comm_date = self.random_date()
            
            communication = {
                'comm_id': f"COMM-{i+1:07d}",
                'from_suspect_id': random.choice(suspect_ids),
                'to_suspect_id': random.choice(suspect_ids),
                'comm_type': random.choice(config.COMM_TYPES),
                'comm_date': comm_date,
                'comm_time': self.random_time(),
                'duration_seconds': random.randint(10, 3600) if random.random() > 0.3 else None,
                'is_encrypted': random.choice([True, False]),
                'relevance_score': random.randint(1, 10),
                'analyzed': random.choice([True, False])
            }
            communications.append(communication)
        
        return pd.DataFrame(communications)


class PoliceETL:
    """ETL Pipeline for police analytics data"""
    
    def __init__(self):
        self.generator = PoliceDataGenerator()
        self.db_path = config.DATABASE_PATH
    
    def extract(self):
        """Extract: Generate synthetic data"""
        print("\n=== DATENEXTRAKTION ===")
        
        # Generate datasets
        incidents_df = self.generator.generate_incidents()
        suspects_list = self.generator.generate_suspects(incidents_df)
        locations_df = self.generator.generate_locations(incidents_df)
        communications_df = self.generator.generate_communications(pd.DataFrame(suspects_list))
        
        # Save raw data
        print("\nSpeichere Rohdaten...")
        incidents_df.to_csv(config.RAW_DATA_DIR / 'incidents.csv', index=False, encoding='utf-8-sig')
        
        with open(config.RAW_DATA_DIR / 'suspects.json', 'w', encoding='utf-8') as f:
            json.dump(suspects_list, f, ensure_ascii=False, indent=2, default=str)
        
        locations_df.to_csv(config.RAW_DATA_DIR / 'locations.csv', index=False, encoding='utf-8-sig')
        communications_df.to_csv(config.RAW_DATA_DIR / 'communications.csv', index=False, encoding='utf-8-sig')
        
        print(f"✓ Rohdaten gespeichert in {config.RAW_DATA_DIR}")
        
        return incidents_df, suspects_list, locations_df, communications_df
    
    def transform(self, incidents_df, suspects_list, locations_df, communications_df):
        """Transform: Clean and validate data"""
        print("\n=== DATENTRANSFORMATION ===")
        
        # Convert suspects from JSON to DataFrame
        suspects_df = pd.DataFrame(suspects_list)
        
        # Data cleaning - Incidents
        print("Bereinige Vorfallsdaten...")
        incidents_df['incident_date'] = pd.to_datetime(incidents_df['incident_date'])
        incidents_df['resolved_date'] = pd.to_datetime(incidents_df['resolved_date'], errors='coerce')
        
        # Calculate resolution days only for resolved incidents
        mask = incidents_df['resolved_date'].notna()
        incidents_df.loc[mask, 'resolution_days'] = (
            incidents_df.loc[mask, 'resolved_date'] - incidents_df.loc[mask, 'incident_date']
        ).dt.days
        incidents_df['resolution_days'] = incidents_df['resolution_days'].fillna(0).astype(int)
        
        # Add temporal features
        incidents_df['month'] = incidents_df['incident_date'].dt.month
        incidents_df['weekday'] = incidents_df['incident_date'].dt.day_name()
        
        # Handle time conversion safely
        def safe_time_convert(time_str):
            try:
                return pd.to_datetime(time_str, format='%H:%M').hour
            except:
                return random.randint(0, 23)
        
        incidents_df['hour'] = incidents_df['incident_time'].apply(safe_time_convert)
        incidents_df['year'] = incidents_df['incident_date'].dt.year
        
        # Data cleaning - Communications
        print("Bereinige Kommunikationsdaten...")
        communications_df['comm_date'] = pd.to_datetime(communications_df['comm_date'])
        communications_df['is_encrypted'] = communications_df['is_encrypted'].astype(bool)
        communications_df['analyzed'] = communications_df['analyzed'].astype(bool)
        
        # Data cleaning - Locations
        print("Bereinige Standortdaten...")
        locations_df['is_hotspot'] = locations_df['is_hotspot'].astype(bool)
        
        # Data validation
        print("\nValidiere Datenintegrität...")
        assert incidents_df['incident_id'].is_unique, "Incident IDs müssen eindeutig sein"
        assert suspects_df['suspect_id'].is_unique, "Suspect IDs müssen eindeutig sein"
        assert locations_df['location_id'].is_unique, "Location IDs müssen eindeutig sein"
        
        # Check geographic bounds
        assert incidents_df['latitude'].between(
            config.FRANKFURT_BOUNDS['lat_min'], 
            config.FRANKFURT_BOUNDS['lat_max']
        ).all(), "Latitude außerhalb Frankfurt-Grenzen"
        
        print("✓ Datentransformation erfolgreich abgeschlossen")
        
        return incidents_df, suspects_df, locations_df, communications_df
    
    def load(self, incidents_df, suspects_df, locations_df, communications_df):
        """Load: Create SQLite database with indexes"""
        print("\n=== DATENBANK-LADEN ===")
        
        # Remove existing database
        if self.db_path.exists():
            self.db_path.unlink()
        
        # Create connection
        conn = sqlite3.connect(self.db_path)
        
        print(f"Erstelle Datenbank: {self.db_path}")
        
        # Load dataframes to SQLite
        incidents_df.to_sql('incidents', conn, if_exists='replace', index=False)
        suspects_df.to_sql('suspects', conn, if_exists='replace', index=False)
        locations_df.to_sql('locations', conn, if_exists='replace', index=False)
        communications_df.to_sql('communications', conn, if_exists='replace', index=False)
        
        # Create indexes for query performance
        print("Erstelle Indizes...")
        cursor = conn.cursor()
        
        cursor.execute("CREATE INDEX idx_incidents_date ON incidents(incident_date)")
        cursor.execute("CREATE INDEX idx_incidents_district ON incidents(district)")
        cursor.execute("CREATE INDEX idx_incidents_category ON incidents(crime_category)")
        cursor.execute("CREATE INDEX idx_incidents_status ON incidents(status)")
        cursor.execute("CREATE INDEX idx_suspects_incident ON suspects(incident_id)")
        cursor.execute("CREATE INDEX idx_locations_district ON locations(district)")
        cursor.execute("CREATE INDEX idx_locations_hotspot ON locations(is_hotspot)")
        cursor.execute("CREATE INDEX idx_comm_from ON communications(from_suspect_id)")
        cursor.execute("CREATE INDEX idx_comm_to ON communications(to_suspect_id)")
        cursor.execute("CREATE INDEX idx_comm_date ON communications(comm_date)")
        
        # Create views for common queries
        print("Erstelle SQL Views...")
        
        cursor.execute("""
            CREATE VIEW vw_active_investigations AS
            SELECT 
                i.incident_id,
                i.crime_category,
                i.incident_date,
                i.district,
                i.priority,
                COUNT(DISTINCT s.suspect_id) as suspect_count,
                i.evidence_items
            FROM incidents i
            LEFT JOIN suspects s ON i.incident_id = s.incident_id
            WHERE i.status = 'Ermittlung läuft'
            GROUP BY i.incident_id
        """)
        
        cursor.execute("""
            CREATE VIEW vw_district_statistics AS
            SELECT 
                district,
                COUNT(*) as total_incidents,
                SUM(CASE WHEN status = 'Abgeschlossen' THEN 1 ELSE 0 END) as solved_incidents,
                AVG(resolution_days) as avg_resolution_days,
                SUM(damage_estimate_eur) as total_damage
            FROM incidents
            GROUP BY district
            ORDER BY total_incidents DESC
        """)
        
        conn.commit()
        
        # Print database statistics
        print("\n=== DATENBANKSTATISTIK ===")
        for table in ['incidents', 'suspects', 'locations', 'communications']:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"  {table}: {count:,} Datensätze")
        
        conn.close()
        print(f"\n✓ Datenbank erfolgreich erstellt: {self.db_path}")
    
    def run_pipeline(self):
        """Execute complete ETL pipeline"""
        print("="*70)
        print("POLIZEI-DATENANALYSE ETL PIPELINE")
        print("="*70)
        
        start_time = datetime.now()
        
        # ETL Process
        incidents_df, suspects_list, locations_df, communications_df = self.extract()
        incidents_df, suspects_df, locations_df, communications_df = self.transform(
            incidents_df, suspects_list, locations_df, communications_df
        )
        self.load(incidents_df, suspects_df, locations_df, communications_df)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print("\n" + "="*70)
        print(f"ETL PIPELINE ABGESCHLOSSEN in {duration:.2f} Sekunden")
        print("="*70)


def main():
    """Main execution function"""
    etl = PoliceETL()
    etl.run_pipeline()


if __name__ == "__main__":
    main()