"""
Simple Data Transformation Script for Western Balkans Dashboard
A streamlined version that focuses on core functionality
"""

import pandas as pd
import json
import os
from datetime import datetime

# Simplified indicator mapping
INDICATORS = {
    "1": {"name": "Energy availability", "category": "Foundational", "subcategory": "Energy"},
    "2": {"name": "Energy reliability", "category": "Foundational", "subcategory": "Energy"},
    "3": {"name": "Digital connectivity", "category": "Foundational", "subcategory": "Digital"},
    "4": {"name": "Connectivity quality", "category": "Foundational", "subcategory": "Digital"},
    "5": {"name": "Productive investments", "category": "Foundational", "subcategory": "Production"},
    "6": {"name": "Productive skills", "category": "Foundational", "subcategory": "Production"},
    "7": {"name": "Operational efficiency", "category": "Foundational", "subcategory": "Production"},
    "8": {"name": "Technology absorption", "category": "Foundational", "subcategory": "Production"},
    "9": {"name": "Advanced skills", "category": "Foundational", "subcategory": "Innovation"},
    "10": {"name": "Specialized skills", "category": "Foundational", "subcategory": "Innovation"},
    "11": {"name": "Research effort", "category": "Foundational", "subcategory": "Innovation"},
    "12": {"name": "Research output", "category": "Foundational", "subcategory": "Innovation"},
    "13": {"name": "Innovation patents", "category": "Foundational", "subcategory": "Innovation"},
    "14": {"name": "Innovation royalties", "category": "Foundational", "subcategory": "Innovation"},
    "15": {"name": "Digital absorption", "category": "Digital", "subcategory": "Absorption"},
    "16": {"name": "Digital deployment", "category": "Digital", "subcategory": "Deployment"},
    "17": {"name": "Digital competitiveness", "category": "Digital", "subcategory": "Deployment"}
}

def transform_excel_to_dashboard_format():
    """Transform Excel data to dashboard format"""
    print("🔄 Transforming data...")
    
    try:
        # Read Excel file
        xl = pd.ExcelFile('data.xlsx')
        print(f"Found {len(xl.sheet_names)} sheets: {xl.sheet_names}")
        
        all_data = []
        
        for sheet_name in xl.sheet_names:
            print(f"Processing sheet: {sheet_name}")
            df = pd.read_excel('data.xlsx', sheet_name=sheet_name)
            
            # Try to identify columns
            country_col = None
            year_col = None
            value_cols = []
            
            for col in df.columns:
                col_lower = str(col).lower()
                if 'country' in col_lower:
                    country_col = col
                elif 'year' in col_lower:
                    year_col = col
                elif df[col].dtype in ['int64', 'float64']:
                    value_cols.append(col)
            
            print(f"  Country: {country_col}, Year: {year_col}, Values: {value_cols}")
            
            # Process data
            if country_col and year_col:
                for _, row in df.iterrows():
                    country = row[country_col]
                    year = row[year_col]
                    
                    for value_col in value_cols:
                        value = row[value_col]
                        if pd.notna(country) and pd.notna(year) and pd.notna(value):
                            all_data.append({
                                'indicator': value_col,
                                'country': str(country),
                                'year': int(year),
                                'value': float(value),
                                'category': 'Unknown',
                                'subcategory': 'Unknown'
                            })
        
        # Create output
        output = {
            'metadata': {
                'title': 'Western Balkans Dashboard Data',
                'transformation_date': datetime.now().isoformat(),
                'total_points': len(all_data)
            },
            'data_points': all_data
        }
        
        # Save to file
        os.makedirs('transformed_data', exist_ok=True)
        with open('transformed_data/consolidated_dataset.json', 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"✅ Transformation complete! Generated {len(all_data)} data points")
        print("📁 Output saved to: transformed_data/consolidated_dataset.json")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    transform_excel_to_dashboard_format()
