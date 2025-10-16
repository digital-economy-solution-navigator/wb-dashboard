"""
New Data Transformation Script for Western Balkans Dashboard
Based on the updated data structure with 17 indicators across 3 main categories:
1. Foundational Capabilities (14 indicators)
2. Digital Capabilities (3 indicators)
"""

import pandas as pd
import json
import os
from datetime import datetime

# Define the indicator mapping based on the new framework
INDICATOR_MAPPING = {
    # 🧩 1. Foundational Capabilities
    # A. Enabling Infrastructure - Energy
    "1": {
        "name": "Energy availability",
        "description": "Electricity consumption per capita",
        "category": "Foundational Capabilities",
        "subcategory": "Enabling Infrastructure - Energy",
        "unit": "kWh per capita"
    },
    "2": {
        "name": "Energy reliability", 
        "description": "Percentage of firms experiencing electrical outages",
        "category": "Foundational Capabilities",
        "subcategory": "Enabling Infrastructure - Energy",
        "unit": "%"
    },
    
    # A. Enabling Infrastructure - Digital
    "3": {
        "name": "Access to digital connectivity",
        "description": "Fixed broadband subscriptions per 100 people",
        "category": "Foundational Capabilities", 
        "subcategory": "Enabling Infrastructure - Digital",
        "unit": "per 100 people"
    },
    "4": {
        "name": "Quality of connectivity",
        "description": "Mean download speed (Mbps)",
        "category": "Foundational Capabilities",
        "subcategory": "Enabling Infrastructure - Digital", 
        "unit": "Mbps"
    },
    
    # B. Production Capabilities - Basic
    "5": {
        "name": "Productive investments",
        "description": "Gross Fixed Capital Formation (GFCF, % of GDP)",
        "category": "Foundational Capabilities",
        "subcategory": "Production Capabilities - Basic",
        "unit": "% of GDP"
    },
    "6": {
        "name": "Productive skills",
        "description": "Mean years of schooling",
        "category": "Foundational Capabilities",
        "subcategory": "Production Capabilities - Basic",
        "unit": "years"
    },
    
    # B. Production Capabilities - Intermediate
    "7": {
        "name": "Operational efficiency",
        "description": "ISO 9001 certificates",
        "category": "Foundational Capabilities",
        "subcategory": "Production Capabilities - Intermediate",
        "unit": "certificates"
    },
    "8": {
        "name": "Technology absorption",
        "description": "Intellectual Property Right payments (royalties, % of GDP)",
        "category": "Foundational Capabilities",
        "subcategory": "Production Capabilities - Intermediate",
        "unit": "% of GDP"
    },
    
    # C. Innovation Capabilities - Basic (Effort)
    "9": {
        "name": "Advanced skills",
        "description": "Gross enrolment ratio in tertiary education",
        "category": "Foundational Capabilities",
        "subcategory": "Innovation Capabilities - Basic (Effort)",
        "unit": "%"
    },
    "10": {
        "name": "Specialized skills",
        "description": "Percentage of graduates from STEM programmes in tertiary education",
        "category": "Foundational Capabilities",
        "subcategory": "Innovation Capabilities - Basic (Effort)",
        "unit": "%"
    },
    "11": {
        "name": "Research effort",
        "description": "Gross Expenditure in R&D (% of GDP)",
        "category": "Foundational Capabilities",
        "subcategory": "Innovation Capabilities - Basic (Effort)",
        "unit": "% of GDP"
    },
    
    # C. Innovation Capabilities - Intermediate (Output)
    "12": {
        "name": "Research output",
        "description": "Scientific and technical journal articles per million people",
        "category": "Foundational Capabilities",
        "subcategory": "Innovation Capabilities - Intermediate (Output)",
        "unit": "per million people"
    },
    "13": {
        "name": "Innovation output (patents)",
        "description": "Total patents in force per 100 billion USD GDP",
        "category": "Foundational Capabilities",
        "subcategory": "Innovation Capabilities - Intermediate (Output)",
        "unit": "per 100 billion USD GDP"
    },
    "14": {
        "name": "Innovation output (royalties)",
        "description": "Intellectual Property Right receipts (royalties, % of GDP)",
        "category": "Foundational Capabilities",
        "subcategory": "Innovation Capabilities - Intermediate (Output)",
        "unit": "% of GDP"
    },
    
    # 💻 2. Digital Capabilities
    # A. Absorption & Exposure
    "15": {
        "name": "Absorption and exposure to production technologies with digital potential",
        "description": "Imports of production technologies (% of GDP)",
        "category": "Digital Capabilities",
        "subcategory": "Absorption & Exposure",
        "unit": "% of GDP"
    },
    
    # B. Deployment & Adaptation
    "16": {
        "name": "Deployment and adaptation of digital production technologies",
        "description": "Imports of digital products (% of GDP)",
        "category": "Digital Capabilities",
        "subcategory": "Deployment & Adaptation",
        "unit": "% of GDP"
    },
    "17": {
        "name": "Industrial competitiveness in digital technologies",
        "description": "Exports of digital products (% of GDP)",
        "category": "Digital Capabilities",
        "subcategory": "Deployment & Adaptation",
        "unit": "% of GDP"
    }
}

def examine_excel_structure(file_path):
    """Examine the structure of the Excel file"""
    print("🔍 EXAMINING EXCEL FILE STRUCTURE")
    print("=" * 50)
    
    try:
        xl = pd.ExcelFile(file_path)
        print(f"📊 Found {len(xl.sheet_names)} sheets:")
        for i, sheet in enumerate(xl.sheet_names, 1):
            print(f"   {i}. {sheet}")
        
        print(f"\n📋 ANALYZING EACH SHEET:")
        print("=" * 50)
        
        sheet_info = {}
        
        for sheet_name in xl.sheet_names:
            print(f"\n📄 Sheet: {sheet_name}")
            print("-" * 30)
            
            try:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                print(f"   Shape: {df.shape[0]} rows × {df.shape[1]} columns")
                print(f"   Columns: {list(df.columns)}")
                
                # Show first few rows
                print(f"   Sample data:")
                print(df.head(3).to_string(index=False))
                
                sheet_info[sheet_name] = {
                    'shape': df.shape,
                    'columns': list(df.columns),
                    'sample_data': df.head(3).to_dict('records')
                }
                
            except Exception as e:
                print(f"   ❌ Error reading sheet: {e}")
                sheet_info[sheet_name] = {'error': str(e)}
        
        return sheet_info
        
    except Exception as e:
        print(f"❌ Error reading Excel file: {e}")
        return None

def transform_data(file_path, output_dir="transformed_data"):
    """Transform the Excel data into structured JSON format"""
    print("\n🔄 TRANSFORMING DATA")
    print("=" * 50)
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        xl = pd.ExcelFile(file_path)
        transformed_data = {}
        summary = {
            "transformation_date": datetime.now().isoformat(),
            "source_file": file_path,
            "total_sheets": len(xl.sheet_names),
            "indicators_processed": 0,
            "countries_identified": set(),
            "years_covered": set()
        }
        
        for sheet_name in xl.sheet_names:
            print(f"\n📊 Processing sheet: {sheet_name}")
            
            try:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                
                # Try to identify the structure
                if df.shape[0] > 0 and df.shape[1] > 0:
                    # Look for country and year columns
                    country_col = None
                    year_col = None
                    value_cols = []
                    
                    for col in df.columns:
                        col_lower = str(col).lower()
                        if 'country' in col_lower or 'nation' in col_lower:
                            country_col = col
                        elif 'year' in col_lower:
                            year_col = col
                        elif col_lower not in ['id', 'index', 'unnamed']:
                            value_cols.append(col)
                    
                    print(f"   Identified columns:")
                    print(f"     Country: {country_col}")
                    print(f"     Year: {year_col}")
                    print(f"     Value columns: {value_cols}")
                    
                    # Process the data
                    sheet_data = {
                        "sheet_name": sheet_name,
                        "structure": {
                            "country_column": country_col,
                            "year_column": year_col,
                            "value_columns": value_cols
                        },
                        "data": df.to_dict('records'),
                        "summary": {
                            "total_rows": len(df),
                            "countries": list(df[country_col].unique()) if country_col else [],
                            "years": list(df[year_col].unique()) if year_col else []
                        }
                    }
                    
                    # Update summary
                    if country_col:
                        summary["countries_identified"].update(df[country_col].unique())
                    if year_col:
                        summary["years_covered"].update(df[year_col].unique())
                    
                    transformed_data[sheet_name] = sheet_data
                    summary["indicators_processed"] += 1
                    
                    # Save individual sheet data
                    output_file = os.path.join(output_dir, f"{sheet_name.replace(' ', '_')}.json")
                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump(sheet_data, f, indent=2, ensure_ascii=False, default=str)
                    
                    print(f"   ✅ Saved to: {output_file}")
                
            except Exception as e:
                print(f"   ❌ Error processing sheet {sheet_name}: {e}")
                transformed_data[sheet_name] = {"error": str(e)}
        
        # Convert sets to lists for JSON serialization
        summary["countries_identified"] = list(summary["countries_identified"])
        summary["years_covered"] = list(summary["years_covered"])
        
        # Save consolidated data
        consolidated_file = os.path.join(output_dir, "consolidated_data.json")
        with open(consolidated_file, 'w', encoding='utf-8') as f:
            json.dump(transformed_data, f, indent=2, ensure_ascii=False, default=str)
        
        # Save summary
        summary_file = os.path.join(output_dir, "transformation_summary.json")
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False, default=str)
        
        # Save indicator mapping
        mapping_file = os.path.join(output_dir, "indicator_mapping.json")
        with open(mapping_file, 'w', encoding='utf-8') as f:
            json.dump(INDICATOR_MAPPING, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ TRANSFORMATION COMPLETE")
        print(f"   Consolidated data: {consolidated_file}")
        print(f"   Summary: {summary_file}")
        print(f"   Indicator mapping: {mapping_file}")
        print(f"   Total indicators processed: {summary['indicators_processed']}")
        print(f"   Countries identified: {len(summary['countries_identified'])}")
        print(f"   Years covered: {len(summary['years_covered'])}")
        
        return transformed_data, summary
        
    except Exception as e:
        print(f"❌ Error during transformation: {e}")
        return None, None

def main():
    """Main function to run the data transformation"""
    file_path = "data.xlsx"
    
    print("🚀 WESTERN BALKANS DASHBOARD - DATA TRANSFORMATION")
    print("=" * 60)
    print("Based on the new framework with 17 indicators:")
    print("🧩 Foundational Capabilities (14 indicators)")
    print("💻 Digital Capabilities (3 indicators)")
    print("=" * 60)
    
    # First, examine the structure
    structure_info = examine_excel_structure(file_path)
    
    if structure_info:
        # Then transform the data
        transformed_data, summary = transform_data(file_path)
        
        if transformed_data and summary:
            print(f"\n🎉 SUCCESS! Data transformation completed.")
            print(f"   Check the 'transformed_data' directory for results.")
        else:
            print(f"\n❌ Transformation failed.")
    else:
        print(f"\n❌ Could not examine Excel file structure.")

if __name__ == "__main__":
    main()

