"""
Western Balkans Dashboard - Data Transformation Script v2
Based on the new 17-indicator framework with comprehensive categorization

This script transforms the updated data.xlsx into a structured format
compatible with the dashboard's filtering and visualization system.
"""

import pandas as pd
import json
import os
from datetime import datetime
import numpy as np

# Comprehensive indicator mapping based on the new framework
INDICATOR_FRAMEWORK = {
    # 🧩 1. Foundational Capabilities
    "foundational_capabilities": {
        "enabling_infrastructure": {
            "energy": {
                "1": {
                    "id": "energy_availability",
                    "name": "Energy availability",
                    "description": "Electricity consumption per capita",
                    "unit": "kWh per capita",
                    "category": "Foundational Capabilities",
                    "subcategory": "Enabling Infrastructure - Energy",
                    "layer": "Basic"
                },
                "2": {
                    "id": "energy_reliability",
                    "name": "Energy reliability",
                    "description": "Percentage of firms experiencing electrical outages",
                    "unit": "%",
                    "category": "Foundational Capabilities",
                    "subcategory": "Enabling Infrastructure - Energy",
                    "layer": "Basic"
                }
            },
            "digital": {
                "3": {
                    "id": "digital_connectivity",
                    "name": "Access to digital connectivity",
                    "description": "Fixed broadband subscriptions per 100 people",
                    "unit": "per 100 people",
                    "category": "Foundational Capabilities",
                    "subcategory": "Enabling Infrastructure - Digital",
                    "layer": "Basic"
                },
                "4": {
                    "id": "connectivity_quality",
                    "name": "Quality of connectivity",
                    "description": "Mean download speed (Mbps)",
                    "unit": "Mbps",
                    "category": "Foundational Capabilities",
                    "subcategory": "Enabling Infrastructure - Digital",
                    "layer": "Basic"
                }
            }
        },
        "production_capabilities": {
            "basic": {
                "5": {
                    "id": "productive_investments",
                    "name": "Productive investments",
                    "description": "Gross Fixed Capital Formation (GFCF, % of GDP)",
                    "unit": "% of GDP",
                    "category": "Foundational Capabilities",
                    "subcategory": "Production Capabilities - Basic",
                    "layer": "Basic"
                },
                "6": {
                    "id": "productive_skills",
                    "name": "Productive skills",
                    "description": "Mean years of schooling",
                    "unit": "years",
                    "category": "Foundational Capabilities",
                    "subcategory": "Production Capabilities - Basic",
                    "layer": "Basic"
                }
            },
            "intermediate": {
                "7": {
                    "id": "operational_efficiency",
                    "name": "Operational efficiency",
                    "description": "ISO 9001 certificates",
                    "unit": "certificates",
                    "category": "Foundational Capabilities",
                    "subcategory": "Production Capabilities - Intermediate",
                    "layer": "Intermediate"
                },
                "8": {
                    "id": "technology_absorption",
                    "name": "Technology absorption",
                    "description": "Intellectual Property Right payments (royalties, % of GDP)",
                    "unit": "% of GDP",
                    "category": "Foundational Capabilities",
                    "subcategory": "Production Capabilities - Intermediate",
                    "layer": "Intermediate"
                }
            }
        },
        "innovation_capabilities": {
            "basic_effort": {
                "9": {
                    "id": "advanced_skills",
                    "name": "Advanced skills",
                    "description": "Gross enrolment ratio in tertiary education",
                    "unit": "%",
                    "category": "Foundational Capabilities",
                    "subcategory": "Innovation Capabilities - Basic (Effort)",
                    "layer": "Basic"
                },
                "10": {
                    "id": "specialized_skills",
                    "name": "Specialized skills",
                    "description": "Percentage of graduates from STEM programmes in tertiary education",
                    "unit": "%",
                    "category": "Foundational Capabilities",
                    "subcategory": "Innovation Capabilities - Basic (Effort)",
                    "layer": "Basic"
                },
                "11": {
                    "id": "research_effort",
                    "name": "Research effort",
                    "description": "Gross Expenditure in R&D (% of GDP)",
                    "unit": "% of GDP",
                    "category": "Foundational Capabilities",
                    "subcategory": "Innovation Capabilities - Basic (Effort)",
                    "layer": "Basic"
                }
            },
            "intermediate_output": {
                "12": {
                    "id": "research_output",
                    "name": "Research output",
                    "description": "Scientific and technical journal articles per million people",
                    "unit": "per million people",
                    "category": "Foundational Capabilities",
                    "subcategory": "Innovation Capabilities - Intermediate (Output)",
                    "layer": "Intermediate"
                },
                "13": {
                    "id": "innovation_patents",
                    "name": "Innovation output (patents)",
                    "description": "Total patents in force per 100 billion USD GDP",
                    "unit": "per 100 billion USD GDP",
                    "category": "Foundational Capabilities",
                    "subcategory": "Innovation Capabilities - Intermediate (Output)",
                    "layer": "Intermediate"
                },
                "14": {
                    "id": "innovation_royalties",
                    "name": "Innovation output (royalties)",
                    "description": "Intellectual Property Right receipts (royalties, % of GDP)",
                    "unit": "% of GDP",
                    "category": "Foundational Capabilities",
                    "subcategory": "Innovation Capabilities - Intermediate (Output)",
                    "layer": "Intermediate"
                }
            }
        }
    },
    # 💻 2. Digital Capabilities
    "digital_capabilities": {
        "absorption_exposure": {
            "15": {
                "id": "digital_absorption",
                "name": "Absorption and exposure to production technologies with digital potential",
                "description": "Imports of production technologies (% of GDP)",
                "unit": "% of GDP",
                "category": "Digital Capabilities",
                "subcategory": "Absorption & Exposure",
                "layer": "Advanced"
            }
        },
        "deployment_adaptation": {
            "16": {
                "id": "digital_deployment",
                "name": "Deployment and adaptation of digital production technologies",
                "description": "Imports of digital products (% of GDP)",
                "unit": "% of GDP",
                "category": "Digital Capabilities",
                "subcategory": "Deployment & Adaptation",
                "layer": "Advanced"
            },
            "17": {
                "id": "digital_competitiveness",
                "name": "Industrial competitiveness in digital technologies",
                "description": "Exports of digital products (% of GDP)",
                "unit": "% of GDP",
                "category": "Digital Capabilities",
                "subcategory": "Deployment & Adaptation",
                "layer": "Advanced"
            }
        }
    }
}

def flatten_indicator_mapping():
    """Flatten the nested indicator mapping into a simple dictionary"""
    flattened = {}
    
    def extract_indicators(data, prefix=""):
        for key, value in data.items():
            if isinstance(value, dict):
                if "id" in value:  # This is an indicator
                    flattened[value["id"]] = value
                else:  # This is a category, recurse
                    extract_indicators(value, f"{prefix}{key}_")
    
    extract_indicators(INDICATOR_FRAMEWORK)
    return flattened

def examine_excel_structure(file_path):
    """Examine the structure of the Excel file and return detailed information"""
    print("🔍 EXAMINING EXCEL FILE STRUCTURE")
    print("=" * 60)
    
    try:
        xl = pd.ExcelFile(file_path)
        print(f"📊 Found {len(xl.sheet_names)} sheets:")
        for i, sheet in enumerate(xl.sheet_names, 1):
            print(f"   {i}. {sheet}")
        
        print(f"\n📋 DETAILED SHEET ANALYSIS:")
        print("=" * 60)
        
        sheet_info = {}
        
        for sheet_name in xl.sheet_names:
            print(f"\n📄 Sheet: {sheet_name}")
            print("-" * 40)
            
            try:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                print(f"   Shape: {df.shape[0]} rows × {df.shape[1]} columns")
                print(f"   Columns: {list(df.columns)}")
                
                # Data types
                print(f"   Data types:")
                for col, dtype in df.dtypes.items():
                    print(f"     - {col}: {dtype}")
                
                # Sample data
                print(f"   Sample data (first 3 rows):")
                print(df.head(3).to_string(index=False))
                
                # Check for missing values
                missing = df.isnull().sum()
                if missing.sum() > 0:
                    print(f"   Missing values:")
                    for col, count in missing[missing > 0].items():
                        print(f"     - {col}: {count} missing")
                else:
                    print("   ✅ No missing values")
                
                # Store analysis
                sheet_info[sheet_name] = {
                    'shape': df.shape,
                    'columns': list(df.columns),
                    'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()},
                    'sample_data': df.head(3).to_dict('records'),
                    'missing_values': missing[missing > 0].to_dict()
                }
                
            except Exception as e:
                print(f"   ❌ Error reading sheet: {e}")
                sheet_info[sheet_name] = {'error': str(e)}
        
        return sheet_info
        
    except Exception as e:
        print(f"❌ Error reading Excel file: {e}")
        return None

def identify_data_structure(df):
    """Identify the structure of a dataframe and return column mappings"""
    structure = {
        'country_col': None,
        'year_col': None,
        'indicator_col': None,
        'value_cols': [],
        'metadata_cols': []
    }
    
    for col in df.columns:
        col_lower = str(col).lower()
        
        # Identify country column
        if any(keyword in col_lower for keyword in ['country', 'nation', 'territory', 'economy']):
            structure['country_col'] = col
        
        # Identify year column
        elif any(keyword in col_lower for keyword in ['year', 'time', 'period']):
            structure['year_col'] = col
        
        # Identify indicator column
        elif any(keyword in col_lower for keyword in ['indicator', 'variable', 'measure', 'metric']):
            structure['indicator_col'] = col
        
        # Identify value columns (numeric columns that aren't year)
        elif pd.api.types.is_numeric_dtype(df[col]) and col != structure['year_col']:
            structure['value_cols'].append(col)
        
        # Everything else is metadata
        else:
            structure['metadata_cols'].append(col)
    
    return structure

def transform_sheet_to_standard_format(df, sheet_name, structure):
    """Transform a sheet to the standard dashboard format"""
    data_points = []
    
    # If we have indicator column, treat each row as a data point
    if structure['indicator_col']:
        for _, row in df.iterrows():
            country = row[structure['country_col']] if structure['country_col'] else 'Unknown'
            year = row[structure['year_col']] if structure['year_col'] else None
            indicator = row[structure['indicator_col']] if structure['indicator_col'] else sheet_name
            
            # Get the value (use first value column if multiple)
            value = None
            if structure['value_cols']:
                value = row[structure['value_cols'][0]]
            
            # Skip rows with missing essential data
            if pd.isna(country) or pd.isna(year) or pd.isna(value):
                continue
            
            data_point = {
                'indicator': str(indicator),
                'country': str(country),
                'year': int(year) if not pd.isna(year) else None,
                'value': float(value) if not pd.isna(value) else None,
                'category': 'Unknown',
                'subcategory': 'Unknown',
                'layer': 'Unknown',
                'unit': 'Unknown',
                'sheet_source': sheet_name
            }
            
            # Try to match with our indicator framework
            flattened_mapping = flatten_indicator_mapping()
            for indicator_id, indicator_info in flattened_mapping.items():
                if (indicator_id.lower() in str(indicator).lower() or 
                    indicator_info['name'].lower() in str(indicator).lower() or
                    indicator_info['description'].lower() in str(indicator).lower()):
                    data_point.update({
                        'category': indicator_info['category'],
                        'subcategory': indicator_info['subcategory'],
                        'layer': indicator_info['layer'],
                        'unit': indicator_info['unit']
                    })
                    break
            
            data_points.append(data_point)
    
    # If no indicator column, treat each value column as a separate indicator
    elif structure['value_cols']:
        for _, row in df.iterrows():
            country = row[structure['country_col']] if structure['country_col'] else 'Unknown'
            year = row[structure['year_col']] if structure['year_col'] else None
            
            for value_col in structure['value_cols']:
                value = row[value_col]
                
                # Skip rows with missing essential data
                if pd.isna(country) or pd.isna(year) or pd.isna(value):
                    continue
                
                data_point = {
                    'indicator': str(value_col),
                    'country': str(country),
                    'year': int(year) if not pd.isna(year) else None,
                    'value': float(value) if not pd.isna(value) else None,
                    'category': 'Unknown',
                    'subcategory': 'Unknown',
                    'layer': 'Unknown',
                    'unit': 'Unknown',
                    'sheet_source': sheet_name
                }
                
                # Try to match with our indicator framework
                flattened_mapping = flatten_indicator_mapping()
                for indicator_id, indicator_info in flattened_mapping.items():
                    if (indicator_id.lower() in str(value_col).lower() or 
                        indicator_info['name'].lower() in str(value_col).lower() or
                        indicator_info['description'].lower() in str(value_col).lower()):
                        data_point.update({
                            'category': indicator_info['category'],
                            'subcategory': indicator_info['subcategory'],
                            'layer': indicator_info['layer'],
                            'unit': indicator_info['unit']
                        })
                        break
                
                data_points.append(data_point)
    
    return data_points

def transform_data(file_path, output_dir="transformed_data_v2"):
    """Main transformation function"""
    print("\n🔄 TRANSFORMING DATA TO DASHBOARD FORMAT")
    print("=" * 60)
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        xl = pd.ExcelFile(file_path)
        all_data_points = []
        transformation_summary = {
            "transformation_date": datetime.now().isoformat(),
            "source_file": file_path,
            "total_sheets": len(xl.sheet_names),
            "sheets_processed": 0,
            "total_data_points": 0,
            "countries_identified": set(),
            "years_covered": set(),
            "indicators_identified": set(),
            "categories_identified": set()
        }
        
        for sheet_name in xl.sheet_names:
            print(f"\n📊 Processing sheet: {sheet_name}")
            
            try:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                
                if df.shape[0] == 0:
                    print(f"   ⚠️  Sheet is empty, skipping")
                    continue
                
                # Identify structure
                structure = identify_data_structure(df)
                print(f"   Structure identified:")
                print(f"     Country: {structure['country_col']}")
                print(f"     Year: {structure['year_col']}")
                print(f"     Indicator: {structure['indicator_col']}")
                print(f"     Value columns: {structure['value_cols']}")
                
                # Transform to standard format
                sheet_data_points = transform_sheet_to_standard_format(df, sheet_name, structure)
                print(f"   Generated {len(sheet_data_points)} data points")
                
                if sheet_data_points:
                    all_data_points.extend(sheet_data_points)
                    transformation_summary["sheets_processed"] += 1
                    
                    # Update summary statistics
                    for dp in sheet_data_points:
                        transformation_summary["countries_identified"].add(dp['country'])
                        transformation_summary["years_covered"].add(dp['year'])
                        transformation_summary["indicators_identified"].add(dp['indicator'])
                        transformation_summary["categories_identified"].add(dp['category'])
                
            except Exception as e:
                print(f"   ❌ Error processing sheet {sheet_name}: {e}")
        
        # Convert sets to lists for JSON serialization
        transformation_summary["countries_identified"] = sorted(list(transformation_summary["countries_identified"]))
        transformation_summary["years_covered"] = sorted(list(transformation_summary["years_covered"]))
        transformation_summary["indicators_identified"] = sorted(list(transformation_summary["indicators_identified"]))
        transformation_summary["categories_identified"] = sorted(list(transformation_summary["categories_identified"]))
        transformation_summary["total_data_points"] = len(all_data_points)
        
        # Create the consolidated dataset in dashboard format
        consolidated_data = {
            "metadata": {
                "title": "Western Balkans Dashboard Data",
                "description": "Comprehensive dataset covering 17 indicators across Foundational and Digital Capabilities",
                "transformation_date": transformation_summary["transformation_date"],
                "source_file": transformation_summary["source_file"],
                "total_data_points": transformation_summary["total_data_points"],
                "countries": transformation_summary["countries_identified"],
                "years": transformation_summary["years_covered"],
                "indicators": transformation_summary["indicators_identified"],
                "categories": transformation_summary["categories_identified"]
            },
            "data_points": all_data_points
        }
        
        # Save files
        consolidated_file = os.path.join(output_dir, "consolidated_dataset.json")
        with open(consolidated_file, 'w', encoding='utf-8') as f:
            json.dump(consolidated_data, f, indent=2, ensure_ascii=False, default=str)
        
        summary_file = os.path.join(output_dir, "transformation_summary.json")
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(transformation_summary, f, indent=2, ensure_ascii=False, default=str)
        
        # Save indicator framework
        framework_file = os.path.join(output_dir, "indicator_framework.json")
        with open(framework_file, 'w', encoding='utf-8') as f:
            json.dump(INDICATOR_FRAMEWORK, f, indent=2, ensure_ascii=False)
        
        # Save flattened mapping for easy lookup
        flattened_mapping = flatten_indicator_mapping()
        mapping_file = os.path.join(output_dir, "indicator_mapping.json")
        with open(mapping_file, 'w', encoding='utf-8') as f:
            json.dump(flattened_mapping, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ TRANSFORMATION COMPLETE")
        print(f"   📁 Output directory: {output_dir}")
        print(f"   📊 Consolidated data: {consolidated_file}")
        print(f"   📋 Summary: {summary_file}")
        print(f"   🗺️  Framework: {framework_file}")
        print(f"   🔍 Mapping: {mapping_file}")
        print(f"   📈 Total data points: {transformation_summary['total_data_points']}")
        print(f"   🌍 Countries: {len(transformation_summary['countries_identified'])}")
        print(f"   📅 Years: {len(transformation_summary['years_covered'])}")
        print(f"   📊 Indicators: {len(transformation_summary['indicators_identified'])}")
        print(f"   🏷️  Categories: {len(transformation_summary['categories_identified'])}")
        
        return consolidated_data, transformation_summary
        
    except Exception as e:
        print(f"❌ Error during transformation: {e}")
        return None, None

def main():
    """Main function to run the data transformation"""
    file_path = "data.xlsx"
    
    print("🚀 WESTERN BALKANS DASHBOARD - DATA TRANSFORMATION v2")
    print("=" * 70)
    print("Based on the comprehensive 17-indicator framework:")
    print("🧩 Foundational Capabilities (14 indicators)")
    print("   - Enabling Infrastructure (Energy & Digital)")
    print("   - Production Capabilities (Basic & Intermediate)")
    print("   - Innovation Capabilities (Basic & Intermediate)")
    print("💻 Digital Capabilities (3 indicators)")
    print("   - Absorption & Exposure")
    print("   - Deployment & Adaptation")
    print("=" * 70)
    
    # First, examine the structure
    structure_info = examine_excel_structure(file_path)
    
    if structure_info:
        # Then transform the data
        consolidated_data, summary = transform_data(file_path)
        
        if consolidated_data and summary:
            print(f"\n🎉 SUCCESS! Data transformation completed.")
            print(f"   The dashboard can now load data from: transformed_data_v2/consolidated_dataset.json")
            print(f"   Update the script.js file to point to the new data location.")
        else:
            print(f"\n❌ Transformation failed.")
    else:
        print(f"\n❌ Could not examine Excel file structure.")

if __name__ == "__main__":
    main()
