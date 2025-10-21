"""
Proper Data Transformation Script for Western Balkans Dashboard
This script handles the actual Excel file structure with 17 sheets
"""

import pandas as pd
import json
import os
from datetime import datetime
import numpy as np

# Define the indicator names for each sheet
INDICATOR_NAMES = {
    1: "Energy availability",
    2: "Energy reliability", 
    3: "Access to digital connectivity",
    4: "Quality of connectivity",
    5: "Productive investments",
    6: "Productive skills",
    7: "Operational efficiency",
    8: "Technology absorption",
    9: "Advanced skills",
    10: "Specialized skills",
    11: "Research effort",
    12: "Research output",
    13: "Innovation output (patents)",
    14: "Innovation output (royalties)",
    15: "Absorption and exposure to production technologies",
    16: "Deployment and adaptation of digital production technologies",
    17: "Industrial competitiveness in digital technologies"
}

# Define categories for each indicator
INDICATOR_CATEGORIES = {
    1: "Foundational Capabilities",
    2: "Foundational Capabilities",
    3: "Digital Capabilities", 
    4: "Digital Capabilities",
    5: "Foundational Capabilities",
    6: "Foundational Capabilities",
    7: "Foundational Capabilities",
    8: "Digital Capabilities",
    9: "Digital Capabilities",
    10: "Digital Capabilities",
    11: "Digital Capabilities",
    12: "Digital Capabilities",
    13: "Digital Capabilities",
    14: "Digital Capabilities",
    15: "Digital Capabilities",
    16: "Digital Capabilities",
    17: "Digital Capabilities"
}

def transform_excel_data(file_path):
    """Transform the Excel file into the dashboard format"""
    print("🔄 TRANSFORMING EXCEL DATA")
    print("=" * 60)
    
    try:
        xl = pd.ExcelFile(file_path)
        print(f"📊 Found {len(xl.sheet_names)} sheets: {xl.sheet_names}")
        
        all_data_points = []
        processed_sheets = 0
        
        for sheet_name in xl.sheet_names:
            sheet_num = int(sheet_name)
            indicator_name = INDICATOR_NAMES.get(sheet_num, f"Indicator {sheet_num}")
            category = INDICATOR_CATEGORIES.get(sheet_num, "Unknown")
            
            print(f"\n📄 Processing sheet {sheet_num}: {indicator_name}")
            print("-" * 50)
            
            try:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                print(f"   Shape: {df.shape[0]} rows × {df.shape[1]} columns")
                
                # Find the country column
                country_col = None
                for col in ['Country', 'Country Code']:
                    if col in df.columns:
                        country_col = col
                        break
                
                if country_col is None:
                    print(f"   ❌ No country column found in sheet {sheet_num}")
                    continue
                
                # Find year columns (numeric columns that are years)
                year_cols = []
                for col in df.columns:
                    if col not in [country_col, 'Code', 'Region', 'Income group', 'PartnerISO3', 'TradeFlowName']:
                        try:
                            year_val = int(col)
                            if 2000 <= year_val <= 2030:  # Reasonable year range
                                year_cols.append(col)
                        except:
                            pass
                
                print(f"   📅 Found year columns: {year_cols}")
                
                # Extract data points
                sheet_data_points = 0
                for _, row in df.iterrows():
                    country = row[country_col]
                    if pd.isna(country) or country == '..':
                        continue
                    
                    for year_col in year_cols:
                        value = row[year_col]
                        if pd.isna(value) or value == '..':
                            continue
                        
                        try:
                            numeric_value = float(value)
                            data_point = {
                                "indicator": indicator_name,
                                "country": country,
                                "year": int(year_col),
                                "value": numeric_value,
                                "category": category,
                                "layer": "Basic" if category == "Foundational Capabilities" else "Advanced",
                                "unit": "Various"  # We'll need to determine units per indicator
                            }
                            all_data_points.append(data_point)
                            sheet_data_points += 1
                        except:
                            continue
                
                print(f"   ✅ Extracted {sheet_data_points} data points")
                processed_sheets += 1
                
            except Exception as e:
                print(f"   ❌ Error processing sheet {sheet_num}: {str(e)}")
                continue
        
        print(f"\n📊 TRANSFORMATION SUMMARY")
        print("=" * 60)
        print(f"✅ Successfully processed {processed_sheets} sheets")
        print(f"📈 Total data points: {len(all_data_points)}")
        
        # Create metadata
        countries = sorted(list(set([dp['country'] for dp in all_data_points])))
        years = sorted(list(set([dp['year'] for dp in all_data_points])))
        indicators = sorted(list(set([dp['indicator'] for dp in all_data_points])))
        categories = sorted(list(set([dp['category'] for dp in all_data_points])))
        
        metadata = {
            "title": "Western Balkans Dashboard Data",
            "description": "Comprehensive dataset covering indicators across Foundational and Digital Capabilities",
            "transformation_date": datetime.now().isoformat(),
            "source_file": "data.xlsx",
            "total_data_points": len(all_data_points),
            "countries": countries,
            "years": years,
            "indicators": indicators,
            "categories": categories
        }
        
        # Create the consolidated dataset
        consolidated_data = {
            "metadata": metadata,
            "data_points": all_data_points
        }
        
        # Save to file
        output_file = "transformed_data_v2/consolidated_dataset.json"
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(consolidated_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved to: {output_file}")
        print(f"📊 Countries: {len(countries)} ({', '.join(countries)})")
        print(f"📅 Years: {len(years)} ({min(years)}-{max(years)})")
        print(f"📈 Indicators: {len(indicators)}")
        print(f"🏷️ Categories: {', '.join(categories)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error transforming data: {str(e)}")
        return False

if __name__ == "__main__":
    file_path = "data.xlsx"
    
    if not os.path.exists(file_path):
        print(f"❌ Excel file not found: {file_path}")
        exit(1)
    
    success = transform_excel_data(file_path)
    
    if success:
        print("\n🎉 Transformation completed successfully!")
        print("You can now refresh your dashboard to see all indicators.")
    else:
        print("\n❌ Transformation failed. Check the errors above.")
