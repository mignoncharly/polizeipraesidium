"""
Comprehensive Data Analysis for Police Investigation Data
Statistical analysis and advanced visualizations
"""

import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
import config

warnings.filterwarnings('ignore')

# Configure matplotlib for German text
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False
sns.set_style("whitegrid")
sns.set_palette("Set2")


class PoliceDataAnalyzer:
    """Comprehensive analysis of police investigation data"""
    
    def __init__(self, db_path=config.DATABASE_PATH):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.load_data()
    
    def load_data(self):
        """Load all tables from database"""
        print("Lade Daten aus Datenbank...")
        
        self.incidents = pd.read_sql_query("SELECT * FROM incidents", self.conn)
        self.suspects = pd.read_sql_query("SELECT * FROM suspects", self.conn)
        self.locations = pd.read_sql_query("SELECT * FROM locations", self.conn)
        self.communications = pd.read_sql_query("SELECT * FROM communications", self.conn)
        
        # Convert date columns
        self.incidents['incident_date'] = pd.to_datetime(self.incidents['incident_date'])
        self.incidents['resolved_date'] = pd.to_datetime(self.incidents['resolved_date'])
        self.communications['comm_date'] = pd.to_datetime(self.communications['comm_date'])
        
        print(f"✓ {len(self.incidents)} Vorfälle, {len(self.suspects)} Verdächtige, "
              f"{len(self.locations)} Standorte, {len(self.communications)} Kommunikationsdaten geladen")
        
        # Debug: Print column names to identify the issue
        print(f"\nSpalten in suspects Tabelle: {list(self.suspects.columns)}")
    
    def statistical_overview(self):
        """Generate comprehensive statistical overview"""
        print("\n" + "="*70)
        print("STATISTISCHE ÜBERSICHT")
        print("="*70)
        
        # Incident statistics
        print("\n VORFALLSTATISTIK:")
        print(f"  Gesamtvorfälle: {len(self.incidents):,}")
        print(f"  Laufende Ermittlungen: {len(self.incidents[self.incidents['status'] == 'Ermittlung läuft']):,}")
        print(f"  Abgeschlossene Fälle: {len(self.incidents[self.incidents['status'] == 'Abgeschlossen']):,}")
        
        solved_rate = (len(self.incidents[self.incidents['status'] == 'Abgeschlossen']) / len(self.incidents)) * 100
        print(f"  Aufklärungsquote: {solved_rate:.1f}%")
        
        # Crime categories
        print("\n TOP 5 DELIKTSKATEGORIEN:")
        for category, count in self.incidents['crime_category'].value_counts().head(5).items():
            pct = (count / len(self.incidents)) * 100
            print(f"  {category}: {count:,} ({pct:.1f}%)")
        
        # District analysis
        print("\n TOP 5 STADTTEILE (nach Vorfallzahl):")
        for district, count in self.incidents['district'].value_counts().head(5).items():
            print(f"  {district}: {count:,}")
        
        # Temporal patterns
        print("\n ZEITLICHE MUSTER:")
        print(f"  Häufigster Wochentag: {self.incidents['weekday'].mode()[0]}")
        print(f"  Häufigste Stunde: {self.incidents['hour'].mode()[0]:02d}:00 Uhr")
        
        # Resolution time
        resolved = self.incidents[self.incidents['status'] == 'Abgeschlossen']
        if len(resolved) > 0:
            print(f"\n⏱ BEARBEITUNGSZEIT (abgeschlossene Fälle):")
            print(f"  Durchschnitt: {resolved['resolution_days'].mean():.0f} Tage")
            print(f"  Median: {resolved['resolution_days'].median():.0f} Tage")
        
        # Suspect statistics - FIXED: Check column names and use correct boolean filtering
        print(f"\n VERDÄCHTIGE:")
        print(f"  Gesamtzahl: {len(self.suspects):,}")
        
        # Check if column exists and use correct filtering
        if 'known_to_police' in self.suspects.columns:
            known_to_police_count = len(self.suspects[self.suspects['known_to_police'] == True])
            print(f"  Polizeibekannt: {known_to_police_count:,}")
        else:
            print("  Polizeibekannt: Spalte nicht gefunden")
        
        if 'arrest_status' in self.suspects.columns:
            u_haft_count = len(self.suspects[self.suspects['arrest_status'] == 'U-Haft'])
            print(f"  In U-Haft: {u_haft_count:,}")
        else:
            print("  In U-Haft: Spalte nicht gefunden")
        
        # Damage estimate
        total_damage = self.incidents['damage_estimate_eur'].sum()
        print(f"\n SCHADENSHÖHE:")
        print(f"  Gesamtschaden: {total_damage:,.2f} EUR")
        print(f"  Durchschnitt pro Vorfall: {self.incidents['damage_estimate_eur'].mean():,.2f} EUR")
    
    def create_dashboard_visualization(self):
        """Create comprehensive dashboard overview"""
        print("\n=== ERSTELLE DASHBOARD-VISUALISIERUNG ===")
        
        fig = plt.figure(figsize=(24, 14))
        fig.suptitle('Polizei Frankfurt – Ermittlungsdaten Dashboard', 
                     fontsize=22, fontweight='bold', y=0.995)
        
        # 1. Crime Categories
        ax1 = plt.subplot(3, 4, 1)
        crime_counts = self.incidents['crime_category'].value_counts().head(8)
        ax1.barh(range(len(crime_counts)), crime_counts.values, color=sns.color_palette("rocket", len(crime_counts)))
        ax1.set_yticks(range(len(crime_counts)))
        ax1.set_yticklabels(crime_counts.index, fontsize=9)
        ax1.set_xlabel('Anzahl', fontsize=10)
        ax1.set_title('Top 8 Deliktskategorien', fontsize=12, fontweight='bold')
        ax1.grid(axis='x', alpha=0.3)
        
        # 2. Status Distribution
        ax2 = plt.subplot(3, 4, 2)
        status_counts = self.incidents['status'].value_counts()
        colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4']
        wedges, texts, autotexts = ax2.pie(status_counts.values, labels=status_counts.index, 
                                            autopct='%1.1f%%', colors=colors, startangle=90)
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        ax2.set_title('Fallstatus-Verteilung', fontsize=12, fontweight='bold')
        
        # 3. Priority Distribution
        ax3 = plt.subplot(3, 4, 3)
        priority_counts = self.incidents['priority'].value_counts()
        priority_order = ['Dringend', 'Hoch', 'Mittel', 'Niedrig']
        priority_counts = priority_counts.reindex(priority_order, fill_value=0)
        colors_priority = ['#d32f2f', '#ff9800', '#ffc107', '#4caf50']
        ax3.bar(range(len(priority_counts)), priority_counts.values, color=colors_priority)
        ax3.set_xticks(range(len(priority_counts)))
        ax3.set_xticklabels(priority_counts.index, fontsize=9)
        ax3.set_ylabel('Anzahl', fontsize=10)
        ax3.set_title('Prioritätsverteilung', fontsize=12, fontweight='bold')
        ax3.grid(axis='y', alpha=0.3)
        
        # 4. Incidents over time
        ax4 = plt.subplot(3, 4, 4)
        incidents_monthly = self.incidents.set_index('incident_date').resample('M').size()
        ax4.plot(incidents_monthly.index, incidents_monthly.values, marker='o', linewidth=2, color='steelblue')
        ax4.fill_between(incidents_monthly.index, incidents_monthly.values, alpha=0.3)
        ax4.set_xlabel('Monat', fontsize=10)
        ax4.set_ylabel('Anzahl Vorfälle', fontsize=10)
        ax4.set_title('Vorfälle pro Monat', fontsize=12, fontweight='bold')
        ax4.grid(alpha=0.3)
        ax4.tick_params(axis='x', rotation=45, labelsize=8)
        
        # 5. Top Districts
        ax5 = plt.subplot(3, 4, 5)
        district_counts = self.incidents['district'].value_counts().head(10)
        ax5.barh(range(len(district_counts)), district_counts.values, color=sns.color_palette("viridis", len(district_counts)))
        ax5.set_yticks(range(len(district_counts)))
        ax5.set_yticklabels(district_counts.index, fontsize=8)
        ax5.set_xlabel('Vorfälle', fontsize=10)
        ax5.set_title('Top 10 Stadtteile', fontsize=12, fontweight='bold')
        ax5.grid(axis='x', alpha=0.3)
        
        # 6. Weekday Pattern
        ax6 = plt.subplot(3, 4, 6)
        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekday_german = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
        weekday_counts = self.incidents['weekday'].value_counts().reindex(weekday_order)
        ax6.bar(weekday_german, weekday_counts.values, color=sns.color_palette("mako", 7))
        ax6.set_ylabel('Anzahl', fontsize=10)
        ax6.set_title('Vorfälle nach Wochentag', fontsize=12, fontweight='bold')
        ax6.grid(axis='y', alpha=0.3)
        
        # 7. Hourly Pattern
        ax7 = plt.subplot(3, 4, 7)
        hourly_counts = self.incidents['hour'].value_counts().sort_index()
        ax7.plot(hourly_counts.index, hourly_counts.values, marker='o', linewidth=2, color='darkred')
        ax7.fill_between(hourly_counts.index, hourly_counts.values, alpha=0.3, color='darkred')
        ax7.set_xlabel('Uhrzeit', fontsize=10)
        ax7.set_ylabel('Anzahl', fontsize=10)
        ax7.set_title('Vorfälle nach Tageszeit', fontsize=12, fontweight='bold')
        ax7.set_xticks(range(0, 24, 3))
        ax7.grid(alpha=0.3)
        
        # 8. Resolution Time Distribution
        ax8 = plt.subplot(3, 4, 8)
        resolved = self.incidents[self.incidents['status'] == 'Abgeschlossen'].copy()
        if len(resolved) > 0:
            ax8.hist(resolved['resolution_days'], bins=30, color='teal', edgecolor='black', alpha=0.7)
            ax8.axvline(resolved['resolution_days'].median(), color='red', 
                       linestyle='--', linewidth=2, label=f'Median: {resolved["resolution_days"].median():.0f}d')
            ax8.set_xlabel('Tage', fontsize=10)
            ax8.set_ylabel('Häufigkeit', fontsize=10)
            ax8.set_title('Bearbeitungsdauer', fontsize=12, fontweight='bold')
            ax8.legend(fontsize=9)
            ax8.grid(alpha=0.3)
        
        # 9. Suspect Age Distribution
        ax9 = plt.subplot(3, 4, 9)
        ax9.hist(self.suspects['age'], bins=20, color='coral', edgecolor='black', alpha=0.7)
        ax9.axvline(self.suspects['age'].median(), color='blue', 
                   linestyle='--', linewidth=2, label=f'Median: {self.suspects["age"].median():.0f}')
        ax9.set_xlabel('Alter', fontsize=10)
        ax9.set_ylabel('Häufigkeit', fontsize=10)
        ax9.set_title('Altersverteilung Verdächtige', fontsize=12, fontweight='bold')
        ax9.legend(fontsize=9)
        ax9.grid(alpha=0.3)
        
        # 10. Arrest Status
        ax10 = plt.subplot(3, 4, 10)
        if 'arrest_status' in self.suspects.columns:
            arrest_counts = self.suspects['arrest_status'].value_counts()
            ax10.bar(range(len(arrest_counts)), arrest_counts.values, color=sns.color_palette("Set3", len(arrest_counts)))
            ax10.set_xticks(range(len(arrest_counts)))
            ax10.set_xticklabels(arrest_counts.index, rotation=45, ha='right', fontsize=8)
            ax10.set_ylabel('Anzahl', fontsize=10)
            ax10.set_title('Haftstatus Verdächtige', fontsize=12, fontweight='bold')
            ax10.grid(axis='y', alpha=0.3)
        else:
            ax10.text(0.5, 0.5, 'Daten nicht verfügbar', ha='center', va='center', transform=ax10.transAxes)
            ax10.set_title('Haftstatus Verdächtige', fontsize=12, fontweight='bold')
        
        # 11. Communication Types
        ax11 = plt.subplot(3, 4, 11)
        comm_counts = self.communications['comm_type'].value_counts().head(7)
        ax11.barh(range(len(comm_counts)), comm_counts.values, color=sns.color_palette("crest", len(comm_counts)))
        ax11.set_yticks(range(len(comm_counts)))
        ax11.set_yticklabels(comm_counts.index, fontsize=8)
        ax11.set_xlabel('Anzahl', fontsize=10)
        ax11.set_title('Kommunikationstypen', fontsize=12, fontweight='bold')
        ax11.grid(axis='x', alpha=0.3)
        
        # 12. Key Metrics Summary
        ax12 = plt.subplot(3, 4, 12)
        ax12.axis('off')
        
        # Calculate metrics safely
        total_incidents = len(self.incidents)
        active_investigations = len(self.incidents[self.incidents['status'] == 'Ermittlung läuft'])
        solved_rate = (len(self.incidents[self.incidents['status'] == 'Abgeschlossen']) / total_incidents * 100) if total_incidents > 0 else 0
        
        total_suspects = len(self.suspects)
        if 'known_to_police' in self.suspects.columns:
            known_to_police = len(self.suspects[self.suspects['known_to_police'] == True])
        else:
            known_to_police = 0
        
        total_damage = self.incidents['damage_estimate_eur'].sum()
        total_communications = len(self.communications)
        encrypted_pct = (self.communications['is_encrypted'].sum() / total_communications * 100) if total_communications > 0 else 0
        
        metrics_text = f"""
        SCHLÜSSELKENNZAHLEN
        
        Gesamtvorfälle: {total_incidents:,}
        Laufende Ermittlungen: {active_investigations:,}
        Aufklärungsquote: {solved_rate:.1f}%
        
        Verdächtige: {total_suspects:,}
        Polizeibekannt: {known_to_police:,}
        
        Gesamtschaden: {total_damage/1000000:.1f} Mio. EUR
        
        Kommunikationsdaten: {total_communications:,}
        Verschlüsselt: {encrypted_pct:.1f}%
        """
        
        ax12.text(0.1, 0.5, metrics_text, fontsize=11, verticalalignment='center',
                 bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        output_path = config.OUTPUT_DIR / 'dashboard_overview.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✓ Dashboard gespeichert: {output_path}")
        plt.close()
    
    def create_temporal_analysis(self):
        """Create detailed temporal pattern analysis"""
        print("\n=== ERSTELLE ZEITLICHE MUSTERERKENNUNG ===")
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 10))
        fig.suptitle('Zeitliche Muster und Trends', fontsize=18, fontweight='bold')
        
        # 1. Monthly trend by category
        ax1 = axes[0, 0]
        top_categories = self.incidents['crime_category'].value_counts().head(5).index
        for category in top_categories:
            category_data = self.incidents[self.incidents['crime_category'] == category]
            monthly = category_data.set_index('incident_date').resample('M').size()
            ax1.plot(monthly.index, monthly.values, marker='o', label=category, linewidth=2)
        ax1.set_xlabel('Monat', fontsize=11)
        ax1.set_ylabel('Anzahl Vorfälle', fontsize=11)
        ax1.set_title('Top 5 Deliktsarten über Zeit', fontsize=13, fontweight='bold')
        ax1.legend(fontsize=9, loc='best')
        ax1.grid(alpha=0.3)
        ax1.tick_params(axis='x', rotation=45)
        
        # 2. Heatmap: Weekday vs Hour
        ax2 = axes[0, 1]
        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekday_german = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
        
        heatmap_data = pd.crosstab(
            pd.Categorical(self.incidents['weekday'], categories=weekday_order, ordered=True),
            self.incidents['hour']
        )
        heatmap_data.index = weekday_german
        
        sns.heatmap(heatmap_data, cmap='YlOrRd', annot=False, fmt='d', ax=ax2, cbar_kws={'label': 'Anzahl'})
        ax2.set_xlabel('Stunde', fontsize=11)
        ax2.set_ylabel('Wochentag', fontsize=11)
        ax2.set_title('Vorfallshäufigkeit: Wochentag × Uhrzeit', fontsize=13, fontweight='bold')
        
        # 3. Priority over time
        ax3 = axes[1, 0]
        priority_time = self.incidents.groupby([
            pd.Grouper(key='incident_date', freq='M'),
            'priority'
        ]).size().unstack(fill_value=0)
        
        priority_time.plot(kind='area', stacked=True, ax=ax3, alpha=0.7,
                          color=['#d32f2f', '#ff9800', '#ffc107', '#4caf50'])
        ax3.set_xlabel('Monat', fontsize=11)
        ax3.set_ylabel('Anzahl Vorfälle', fontsize=11)
        ax3.set_title('Prioritätsverteilung über Zeit', fontsize=13, fontweight='bold')
        ax3.legend(title='Priorität', loc='upper left', fontsize=9)
        ax3.grid(alpha=0.3)
        ax3.tick_params(axis='x', rotation=45)
        
        # 4. District trends
        ax4 = axes[1, 1]
        top_districts = self.incidents['district'].value_counts().head(5).index
        for district in top_districts:
            district_data = self.incidents[self.incidents['district'] == district]
            monthly = district_data.set_index('incident_date').resample('M').size()
            ax4.plot(monthly.index, monthly.values, marker='s', label=district, linewidth=2)
        ax4.set_xlabel('Monat', fontsize=11)
        ax4.set_ylabel('Anzahl Vorfälle', fontsize=11)
        ax4.set_title('Top 5 Stadtteile über Zeit', fontsize=13, fontweight='bold')
        ax4.legend(fontsize=9, loc='best')
        ax4.grid(alpha=0.3)
        ax4.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        output_path = config.OUTPUT_DIR / 'temporal_patterns.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✓ Zeitliche Analyse gespeichert: {output_path}")
        plt.close()
    
    def create_network_analysis(self):
        """Create communication network analysis"""
        print("\n=== ERSTELLE NETZWERKANALYSE ===")
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 10))
        fig.suptitle('Kommunikationsnetzwerk-Analyse', fontsize=18, fontweight='bold')
        
        # 1. Communication frequency by type
        ax1 = axes[0, 0]
        comm_type_counts = self.communications['comm_type'].value_counts()
        ax1.bar(range(len(comm_type_counts)), comm_type_counts.values, 
               color=sns.color_palette("twilight", len(comm_type_counts)))
        ax1.set_xticks(range(len(comm_type_counts)))
        ax1.set_xticklabels(comm_type_counts.index, rotation=45, ha='right', fontsize=9)
        ax1.set_ylabel('Anzahl Kommunikationen', fontsize=11)
        ax1.set_title('Häufigkeit nach Kommunikationstyp', fontsize=13, fontweight='bold')
        ax1.grid(axis='y', alpha=0.3)
        
        # 2. Encryption status
        ax2 = axes[0, 1]
        encrypted_pct = (self.communications['is_encrypted'].sum() / len(self.communications)) * 100
        sizes = [encrypted_pct, 100 - encrypted_pct]
        colors = ['#e74c3c', '#2ecc71']
        labels = [f'Verschlüsselt\n({encrypted_pct:.1f}%)', f'Unverschlüsselt\n({100-encrypted_pct:.1f}%)']
        ax2.pie(sizes, labels=labels, colors=colors, autopct='', startangle=90, textprops={'fontsize': 11})
        ax2.set_title('Verschlüsselungsstatus', fontsize=13, fontweight='bold')
        
        # 3. Communication volume over time
        ax3 = axes[1, 0]
        comm_monthly = self.communications.set_index('comm_date').resample('M').size()
        ax3.plot(comm_monthly.index, comm_monthly.values, marker='o', linewidth=2, color='purple')
        ax3.fill_between(comm_monthly.index, comm_monthly.values, alpha=0.3, color='purple')
        ax3.set_xlabel('Monat', fontsize=11)
        ax3.set_ylabel('Anzahl Kommunikationen', fontsize=11)
        ax3.set_title('Kommunikationsvolumen über Zeit', fontsize=13, fontweight='bold')
        ax3.grid(alpha=0.3)
        ax3.tick_params(axis='x', rotation=45)
        
        # 4. Relevance score distribution
        ax4 = axes[1, 1]
        relevance_counts = self.communications['relevance_score'].value_counts().sort_index()
        ax4.bar(relevance_counts.index, relevance_counts.values, color='teal', alpha=0.7, edgecolor='black')
        ax4.set_xlabel('Relevanzbewertung (1-10)', fontsize=11)
        ax4.set_ylabel('Anzahl', fontsize=11)
        ax4.set_title('Verteilung der Kommunikationsrelevanz', fontsize=13, fontweight='bold')
        ax4.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        output_path = config.OUTPUT_DIR / 'network_analysis.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✓ Netzwerkanalyse gespeichert: {output_path}")
        plt.close()
    
    def generate_statistical_report(self):
        """Generate comprehensive statistical report CSV"""
        print("\n=== ERSTELLE STATISTIKBERICHT ===")
        
        report_data = []
        
        # Overall metrics
        report_data.append({
            'Kategorie': 'Übersicht',
            'Metrik': 'Gesamtvorfälle',
            'Wert': len(self.incidents),
            'Einheit': 'Anzahl'
        })
        
        report_data.append({
            'Kategorie': 'Übersicht',
            'Metrik': 'Aufklärungsquote',
            'Wert': round((len(self.incidents[self.incidents['status'] == 'Abgeschlossen']) / len(self.incidents)) * 100, 2),
            'Einheit': '%'
        })
        
        report_data.append({
            'Kategorie': 'Übersicht',
            'Metrik': 'Durchschnittliche Bearbeitungszeit',
            'Wert': round(self.incidents[self.incidents['status'] == 'Abgeschlossen']['resolution_days'].mean(), 1),
            'Einheit': 'Tage'
        })
        
        report_data.append({
            'Kategorie': 'Übersicht',
            'Metrik': 'Gesamtschaden',
            'Wert': round(self.incidents['damage_estimate_eur'].sum(), 2),
            'Einheit': 'EUR'
        })
        
        # Top crime categories
        for i, (category, count) in enumerate(self.incidents['crime_category'].value_counts().head(5).items(), 1):
            report_data.append({
                'Kategorie': 'Top Delikte',
                'Metrik': f'{i}. {category}',
                'Wert': count,
                'Einheit': 'Vorfälle'
            })
        
        # Top districts
        for i, (district, count) in enumerate(self.incidents['district'].value_counts().head(5).items(), 1):
            report_data.append({
                'Kategorie': 'Top Stadtteile',
                'Metrik': f'{i}. {district}',
                'Wert': count,
                'Einheit': 'Vorfälle'
            })
        
        # Suspect metrics
        report_data.append({
            'Kategorie': 'Verdächtige',
            'Metrik': 'Gesamtzahl',
            'Wert': len(self.suspects),
            'Einheit': 'Personen'
        })
        
        report_data.append({
            'Kategorie': 'Verdächtige',
            'Metrik': 'Durchschnittsalter',
            'Wert': round(self.suspects['age'].mean(), 1),
            'Einheit': 'Jahre'
        })
        
        # Check if column exists
        if 'known_to_police' in self.suspects.columns:
            report_data.append({
                'Kategorie': 'Verdächtige',
                'Metrik': 'Polizeibekannt',
                'Wert': len(self.suspects[self.suspects['known_to_police'] == True]),
                'Einheit': 'Personen'
            })
        
        # Communication metrics
        report_data.append({
            'Kategorie': 'Kommunikation',
            'Metrik': 'Gesamtdatensätze',
            'Wert': len(self.communications),
            'Einheit': 'Einträge'
        })
        
        report_data.append({
            'Kategorie': 'Kommunikation',
            'Metrik': 'Verschlüsselungsrate',
            'Wert': round((self.communications['is_encrypted'].sum() / len(self.communications)) * 100, 1),
            'Einheit': '%'
        })
        
        report_df = pd.DataFrame(report_data)
        output_path = config.OUTPUT_DIR / 'statistical_report.csv'
        report_df.to_csv(output_path, index=False, encoding='utf-8-sig')
        
        print(f"✓ Statistikbericht gespeichert: {output_path}")
        print("\n" + report_df.to_string(index=False))
        
        return report_df
    
    def run_complete_analysis(self):
        """Execute complete analysis pipeline"""
        print("\n" + "="*70)
        print("POLIZEI-DATENANALYSE PIPELINE")
        print("="*70)
        
        start_time = datetime.now()
        
        # Run analyses
        self.statistical_overview()
        self.create_dashboard_visualization()
        self.create_temporal_analysis()
        self.create_network_analysis()
        self.generate_statistical_report()
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print("\n" + "="*70)
        print(f"ANALYSE ABGESCHLOSSEN in {duration:.2f} Sekunden")
        print(f"Alle Ergebnisse in: {config.OUTPUT_DIR}")
        print("="*70)
    
    def __del__(self):
        """Close database connection"""
        if hasattr(self, 'conn'):
            self.conn.close()


def main():
    """Main execution function"""
    analyzer = PoliceDataAnalyzer()
    analyzer.run_complete_analysis()


if __name__ == "__main__":
    main()