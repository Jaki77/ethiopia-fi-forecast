"""
Data processing utilities for Ethiopia Financial Inclusion Forecasting
Task 1: Data Exploration and Enrichment
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json
from pathlib import Path

class DataProcessor:
    """Process and enrich financial inclusion data."""
    
    def __init__(self, data_dir='../data'):
        self.data_dir = Path(data_dir)
        self.raw_dir = self.data_dir / 'raw'
        self.processed_dir = self.data_dir / 'processed'
        
        # Create directories if they don't exist
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        
    def load_data(self):
        """Load all raw datasets."""
        print("Loading datasets...")
        
        try:
            self.df = pd.read_csv(self.raw_dir / 'ethiopia_fi_unified_data.csv')
            self.ref_codes = pd.read_csv(self.raw_dir / 'reference_codes.csv')
            
            print(f"Main dataset: {self.df.shape}")
            print(f"Reference codes: {self.ref_codes.shape}")
            
            return True
        except FileNotFoundError as e:
            print(f"Error loading data: {e}")
            return False
    
    def analyze_dataset(self):
        """Perform initial analysis of the dataset."""
        analysis = {}
        
        # Record type distribution
        analysis['record_counts'] = self.df['record_type'].value_counts().to_dict()
        
        # Date ranges
        obs = self.df[self.df['record_type'] == 'observation'].copy()
        if 'observation_date' in obs.columns:
            obs['observation_date'] = pd.to_datetime(obs['observation_date'], errors='coerce')
            analysis['obs_date_range'] = {
                'min': obs['observation_date'].min().strftime('%Y-%m-%d') if not obs['observation_date'].isna().all() else None,
                'max': obs['observation_date'].max().strftime('%Y-%m-%d') if not obs['observation_date'].isna().all() else None
            }
        
        # Unique indicators
        unique_indicators = obs['indicator_code'].dropna().unique()
        analysis['unique_indicators_count'] = len(unique_indicators)
        analysis['sample_indicators'] = unique_indicators[:5].tolist()
        
        # Missing values
        missing = self.df.isnull().sum()
        analysis['missing_values'] = missing[missing > 0].to_dict()
        
        return analysis
    
    def create_enrichment_template(self):
        """Create a template for new data entries."""
        template = {
            'observation': {
                'required': ['pillar', 'indicator', 'indicator_code', 'value_numeric', 
                            'observation_date', 'source_name', 'source_url'],
                'optional': ['source_type', 'confidence', 'notes', 'collected_by', 'collection_date']
            },
            'event': {
                'required': ['event_name', 'event_category', 'event_date', 'description'],
                'optional': ['source_name', 'source_url', 'confidence', 'notes']
            },
            'impact_link': {
                'required': ['parent_id', 'pillar', 'related_indicator', 'impact_direction'],
                'optional': ['impact_magnitude', 'lag_months', 'evidence_basis', 'notes']
            }
        }
        
        return template
    
    def save_enriched_data(self, enriched_df, filename='ethiopia_fi_enriched.csv'):
        """Save enriched dataset."""
        save_path = self.processed_dir / filename
        enriched_df.to_csv(save_path, index=False)
        print(f"Enriched data saved to: {save_path}")
        return save_path
    
    def generate_report(self, analysis, new_records):
        """Generate a summary report."""
        report = {
            'generated_date': datetime.now().isoformat(),
            'dataset_analysis': analysis,
            'enrichment_summary': {
                'new_observations': len(new_records.get('observations', [])),
                'new_events': len(new_records.get('events', [])),
                'new_impact_links': len(new_records.get('impact_links', []))
            },
            'data_quality_issues': [],
            'recommendations': []
        }
        
        # Save report
        report_path = self.processed_dir / 'task1_report.json'
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report_path


def main():
    """Main execution function."""
    print("="*60)
    print("TASK 1: DATA EXPLORATION AND ENRICHMENT")
    print("="*60)
    
    # Initialize processor
    processor = DataProcessor()
    
    # Load data
    if not processor.load_data():
        return
    
    # Analyze dataset
    print("\nAnalyzing dataset...")
    analysis = processor.analyze_dataset()
    
    print(f"\nDataset Summary:")
    print(f"- Total records: {len(processor.df)}")
    print(f"- Record types: {analysis['record_counts']}")
    print(f"- Unique indicators: {analysis['unique_indicators_count']}")
    print(f"- Observation date range: {analysis['obs_date_range']}")
    
    # Create enrichment template
    template = processor.create_enrichment_template()
    print(f"\nEnrichment template created.")
    
    # Note: In practice, you would add new records here
    # For now, we'll just save the original data as enriched
    processor.save_enriched_data(processor.df)
    
    # Generate report
    report_path = processor.generate_report(analysis, {})
    print(f"\nReport generated: {report_path}")
    
    print("\n✅ Task 1 processing completed!")


if __name__ == "__main__":
    main()