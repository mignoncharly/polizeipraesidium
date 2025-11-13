"""
Geographic Analysis and Crime Heatmap Generation
Specialized script for geospatial analysis of crime data
"""

import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import config

plt.rcParams['font.family'] = 'DejaVu Sans'
sns.set_style("white")


class GeoAnalyzer:
    """Geographic analysis of crime data"""
    
    def __init__(self, db_path=config.DATABASE_PATH):
        self.conn = sqlite3.connect(db_path)
        self.load_data()
    
    def load_data(self):
        """Load data from database"""
        print("Lade geografische Daten...")
        self.incidents = pd.read_sql_query("SELECT * FROM incidents", self.conn)
        self.locations = pd.read_sql_query("SELECT * FROM locations", self.conn)
        print(f"✓ {len(self.incidents)} Vorfälle mit Geokoordinaten geladen")
        
        # Debug: Print column names to identify the issue
        print(f"Spalten in locations Tabelle: {list(self.locations.columns)}")
    
    def create_crime_heatmap(self):
        """Create comprehensive crime heatmap"""
        print("\n=== ERSTELLE CRIME HEATMAP ===")
        
        fig = plt.figure(figsize=(20, 12))
        fig.suptitle('Geografische Kriminalitätsanalyse – Frankfurt am Main', 
                     fontsize=20, fontweight='bold')
        
        # 1. Overall heatmap
        ax1 = plt.subplot(2, 2, 1)
        
        # Create 2D histogram for heatmap
        heatmap, xedges, yedges = np.histogram2d(
            self.incidents['longitude'],
            self.incidents['latitude'],
            bins=50
        )
        
        extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
        
        im = ax1.imshow(heatmap.T, extent=extent, origin='lower', cmap='hot', aspect='auto', interpolation='gaussian')
        ax1.scatter(self.incidents['longitude'], self.incidents['latitude'], 
                   alpha=0.1, s=5, c='blue', edgecolors='none')
        
        plt.colorbar(im, ax=ax1, label='Vorfallsdichte')
        ax1.set_xlabel('Längengrad', fontsize=11)
        ax1.set_ylabel('Breitengrad', fontsize=11)
        ax1.set_title('Kriminalitäts-Heatmap (Gesamtübersicht)', fontsize=13, fontweight='bold')
        ax1.grid(alpha=0.3)
        
        # 2. Hotspots by crime category
        ax2 = plt.subplot(2, 2, 2)
        
        top_categories = self.incidents['crime_category'].value_counts().head(3).index
        colors = ['red', 'blue', 'green']
        
        for category, color in zip(top_categories, colors):
            category_data = self.incidents[self.incidents['crime_category'] == category]
            ax2.scatter(category_data['longitude'], category_data['latitude'],
                       alpha=0.4, s=30, c=color, label=category, edgecolors='black', linewidth=0.5)
        
        ax2.set_xlabel('Längengrad', fontsize=11)
        ax2.set_ylabel('Breitengrad', fontsize=11)
        ax2.set_title('Räumliche Verteilung: Top 3 Deliktsarten', fontsize=13, fontweight='bold')
        ax2.legend(loc='best', fontsize=9)
        ax2.grid(alpha=0.3)
        
        # 3. District-level aggregation
        ax3 = plt.subplot(2, 2, 3)
        
        district_counts = self.incidents['district'].value_counts().head(15)
        colors = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, len(district_counts)))
        
        ax3.barh(range(len(district_counts)), district_counts.values, color=colors)
        ax3.set_yticks(range(len(district_counts)))
        ax3.set_yticklabels(district_counts.index, fontsize=9)
        ax3.set_xlabel('Anzahl Vorfälle', fontsize=11)
        ax3.set_title('Vorfallshäufigkeit nach Stadtteil (Top 15)', fontsize=13, fontweight='bold')
        ax3.grid(axis='x', alpha=0.3)
        
        # 4. High-priority incidents map
        ax4 = plt.subplot(2, 2, 4)
        
        high_priority = self.incidents[self.incidents['priority'].isin(['Hoch', 'Dringend'])]
        
        scatter = ax4.scatter(high_priority['longitude'], high_priority['latitude'],
                             c=high_priority['priority'].map({'Hoch': 1, 'Dringend': 2}),
                             cmap='YlOrRd', s=50, alpha=0.6, edgecolors='black', linewidth=0.5)
        
        ax4.set_xlabel('Längengrad', fontsize=11)
        ax4.set_ylabel('Breitengrad', fontsize=11)
        ax4.set_title('Hochpriorisierte Vorfälle (Hoch/Dringend)', fontsize=13, fontweight='bold')
        cbar = plt.colorbar(scatter, ax=ax4, ticks=[1, 2])
        cbar.ax.set_yticklabels(['Hoch', 'Dringend'])
        ax4.grid(alpha=0.3)
        
        plt.tight_layout()
        output_path = config.OUTPUT_DIR / 'crime_heatmap.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✓ Crime Heatmap gespeichert: {output_path}")
        plt.close()
    
    def analyze_hotspots(self):
        """Analyze and visualize crime hotspots"""
        print("\n=== HOTSPOT-ANALYSE ===")
        
        # Check if column exists and use correct boolean filtering
        if 'is_hotspot' in self.locations.columns:
            hotspots = self.locations[self.locations['is_hotspot'] == True]
        else:
            print("⚠ 'is_hotspot' Spalte nicht gefunden. Verwende alternative Methode...")
            # Alternative: Create hotspots based on incident count
            hotspot_threshold = self.locations['incident_count'].quantile(0.75)
            hotspots = self.locations[self.locations['incident_count'] >= hotspot_threshold]
            print(f"  Hotspot-Schwelle: {hotspot_threshold} Vorfälle")
        
        print(f"Identifizierte Hotspots: {len(hotspots)}")
        
        if len(hotspots) > 0:
            print("\nTop 10 Hotspots nach Vorfallzahl:")
            top_hotspots = hotspots.nlargest(10, 'incident_count')
            
            for idx, row in top_hotspots.iterrows():
                print(f"  {row['location_name']} ({row['district']}): {row['incident_count']} Vorfälle")
        else:
            print("⚠ Keine Hotspots gefunden")
    
    def create_hotspot_map(self):
        """Create a dedicated hotspot visualization"""
        print("\n=== ERSTELLE HOTSPOT-KARTE ===")
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
        fig.suptitle('Kriminalitäts-Hotspots Frankfurt am Main', fontsize=16, fontweight='bold')
        
        # 1. All locations with incident count
        scatter1 = ax1.scatter(self.locations['longitude'], self.locations['latitude'],
                              c=self.locations['incident_count'], cmap='Reds', 
                              s=50, alpha=0.7, edgecolors='black', linewidth=0.5)
        ax1.set_xlabel('Längengrad', fontsize=11)
        ax1.set_ylabel('Breitengrad', fontsize=11)
        ax1.set_title('Vorfallszahl pro Standort', fontsize=13, fontweight='bold')
        plt.colorbar(scatter1, ax=ax1, label='Anzahl Vorfälle')
        ax1.grid(alpha=0.3)
        
        # 2. Hotspots only
        if 'is_hotspot' in self.locations.columns:
            hotspots = self.locations[self.locations['is_hotspot'] == True]
            title_suffix = "(is_hotspot = True)"
        else:
            # Use top 20% locations by incident count as hotspots
            hotspot_threshold = self.locations['incident_count'].quantile(0.8)
            hotspots = self.locations[self.locations['incident_count'] >= hotspot_threshold]
            title_suffix = f"(Top 20%: ≥{hotspot_threshold} Vorfälle)"
        
        if len(hotspots) > 0:
            scatter2 = ax2.scatter(hotspots['longitude'], hotspots['latitude'],
                                  c=hotspots['incident_count'], cmap='OrRd', 
                                  s=80, alpha=0.8, edgecolors='red', linewidth=1)
            ax2.set_xlabel('Längengrad', fontsize=11)
            ax2.set_ylabel('Breitengrad', fontsize=11)
            ax2.set_title(f'Identifizierte Hotspots {title_suffix}', fontsize=13, fontweight='bold')
            plt.colorbar(scatter2, ax=ax2, label='Anzahl Vorfälle')
        else:
            ax2.text(0.5, 0.5, 'Keine Hotspots gefunden', 
                    ha='center', va='center', transform=ax2.transAxes, fontsize=12)
            ax2.set_title('Identifizierte Hotspots', fontsize=13, fontweight='bold')
        
        ax2.grid(alpha=0.3)
        
        plt.tight_layout()
        output_path = config.OUTPUT_DIR / 'hotspot_analysis.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✓ Hotspot-Karte gespeichert: {output_path}")
        plt.close()
    
    def create_district_analysis(self):
        """Create detailed district-level analysis"""
        print("\n=== ERSTELLE STADTTEIL-ANALYSE ===")
        
        # Calculate district statistics
        district_stats = self.incidents.groupby('district').agg({
            'incident_id': 'count',
            'damage_estimate_eur': 'sum',
            'resolution_days': 'mean',
            'evidence_items': 'mean'
        }).round(2).reset_index()
        
        district_stats = district_stats.rename(columns={
            'incident_id': 'vorfaelle',
            'damage_estimate_eur': 'gesamtschaden',
            'resolution_days': 'durchschnittliche_bearbeitungszeit',
            'evidence_items': 'durchschnittliche_beweismittel'
        })
        
        # Sort by incident count
        district_stats = district_stats.sort_values('vorfaelle', ascending=False)
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 12))
        fig.suptitle('Stadtteilanalyse - Kriminalitätsstatistiken', fontsize=16, fontweight='bold')
        
        # 1. Incidents by district
        top_districts = district_stats.head(15)
        colors1 = plt.cm.viridis(np.linspace(0.2, 0.8, len(top_districts)))
        ax1.barh(range(len(top_districts)), top_districts['vorfaelle'], color=colors1)
        ax1.set_yticks(range(len(top_districts)))
        ax1.set_yticklabels(top_districts['district'], fontsize=9)
        ax1.set_xlabel('Anzahl Vorfälle', fontsize=11)
        ax1.set_title('Top 15 Stadtteile nach Vorfallzahl', fontsize=13, fontweight='bold')
        ax1.grid(axis='x', alpha=0.3)
        
        # 2. Damage by district
        top_damage = district_stats.nlargest(10, 'gesamtschaden')
        colors2 = plt.cm.Reds(np.linspace(0.3, 0.8, len(top_damage)))
        ax2.barh(range(len(top_damage)), top_damage['gesamtschaden'], color=colors2)
        ax2.set_yticks(range(len(top_damage)))
        ax2.set_yticklabels(top_damage['district'], fontsize=9)
        ax2.set_xlabel('Schadenssumme (EUR)', fontsize=11)
        ax2.set_title('Top 10 Stadtteile nach Schadenshöhe', fontsize=13, fontweight='bold')
        ax2.grid(axis='x', alpha=0.3)
        
        # 3. Resolution time by district
        resolution_stats = district_stats[district_stats['durchschnittliche_bearbeitungszeit'] > 0].nlargest(10, 'durchschnittliche_bearbeitungszeit')
        if len(resolution_stats) > 0:
            colors3 = plt.cm.Blues(np.linspace(0.3, 0.8, len(resolution_stats)))
            ax3.barh(range(len(resolution_stats)), resolution_stats['durchschnittliche_bearbeitungszeit'], color=colors3)
            ax3.set_yticks(range(len(resolution_stats)))
            ax3.set_yticklabels(resolution_stats['district'], fontsize=9)
            ax3.set_xlabel('Durchschnittliche Bearbeitungszeit (Tage)', fontsize=11)
            ax3.set_title('Längste Bearbeitungszeiten nach Stadtteil', fontsize=13, fontweight='bold')
            ax3.grid(axis='x', alpha=0.3)
        else:
            ax3.text(0.5, 0.5, 'Keine Daten verfügbar', ha='center', va='center', transform=ax3.transAxes)
            ax3.set_title('Längste Bearbeitungszeiten nach Stadtteil', fontsize=13, fontweight='bold')
        
        # 4. Evidence items by district
        evidence_stats = district_stats.nlargest(10, 'durchschnittliche_beweismittel')
        colors4 = plt.cm.Greens(np.linspace(0.3, 0.8, len(evidence_stats)))
        ax4.barh(range(len(evidence_stats)), evidence_stats['durchschnittliche_beweismittel'], color=colors4)
        ax4.set_yticks(range(len(evidence_stats)))
        ax4.set_yticklabels(evidence_stats['district'], fontsize=9)
        ax4.set_xlabel('Durchschnittliche Beweismittel', fontsize=11)
        ax4.set_title('Meiste Beweismittel pro Vorfall', fontsize=13, fontweight='bold')
        ax4.grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        output_path = config.OUTPUT_DIR / 'district_analysis.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✓ Stadtteil-Analyse gespeichert: {output_path}")
        
        # Save district statistics to CSV
        csv_path = config.OUTPUT_DIR / 'district_statistics.csv'
        district_stats.to_csv(csv_path, index=False, encoding='utf-8-sig')
        print(f"✓ Stadtteil-Statistiken gespeichert: {csv_path}")
        
        plt.close()
    
    def run_analysis(self):
        """Execute geographic analysis"""
        print("\n" + "="*70)
        print("GEOGRAFISCHE ANALYSE")
        print("="*70)
        
        self.create_crime_heatmap()
        self.analyze_hotspots()
        self.create_hotspot_map()
        self.create_district_analysis()
        
        print("\n✓ Geografische Analyse abgeschlossen")
    
    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()


def main():
    analyzer = GeoAnalyzer()
    analyzer.run_analysis()


if __name__ == "__main__":
    main()