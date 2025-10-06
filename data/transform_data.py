#!/usr/bin/env python3
"""
Data Transformation Script
Transforms raw JSON data from Excel sheets into a consistent, standardized format
for easy visualization and filtering.
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Any, Optional

class DataTransformer:
    def __init__(self, input_dir: str = "json_output", output_dir: str = "standardized_data"):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.indicators = {}
        self.countries = set()
        self.years = set()
        
    def clean_string(self, text: Any) -> str:
        """Clean and normalize string values."""
        if text is None or text == "":
            return ""
        return str(text).strip()
    
    def extract_year_from_column(self, column_name: str) -> Optional[int]:
        """Extract year from column names like '20152022', '20102014', etc."""
        # Look for 4-digit year patterns
        year_match = re.search(r'(\d{4})', str(column_name))
        if year_match:
            return int(year_match.group(1))
        return None
    
    def is_data_column(self, column_name: str) -> bool:
        """Determine if a column contains actual data values."""
        if not column_name or column_name.startswith('Unnamed_') or column_name == 'NaN':
            return False
        
        # Skip metadata columns
        metadata_columns = {
            'economy', 'code', 'region', 'income_group', 'last_available_year',
            'column1', 'column2', 'column110', 'column18', 'column19', 'column20',
            'column21', 'column22'
        }
        
        if column_name.lower() in metadata_columns:
            return False
            
        # Check if it looks like a year range (e.g., 20152022)
        if re.match(r'^\d{4}\d{4}$', str(column_name)):
            return True
            
        # Check if it's a single year
        if re.match(r'^\d{4}$', str(column_name)):
            return True
            
        return False
    
    def extract_indicator_name(self, filename: str) -> str:
        """Extract clean indicator name from filename."""
        # Remove file extension and clean up
        name = filename.replace('.json', '')
        
        # Remove leading numbers and underscores
        name = re.sub(r'^\d+_', '', name)
        
        # Replace underscores with spaces and title case
        name = name.replace('_', ' ').title()
        
        # Clean up specific cases
        name = name.replace('Gdp', 'GDP')
        name = name.replace('Ipr', 'IPR')
        name = name.replace('Gfcf', 'GFCF')
        name = name.replace('Stem', 'STEM')
        name = name.replace('Gerd', 'GERD')
        name = name.replace('Ptdp', 'PTDP')
        name = name.replace('Adtp', 'ADTP')
        
        return name
    
    def categorize_indicator(self, indicator_name: str) -> str:
        """Categorize indicators into logical groups."""
        name_lower = indicator_name.lower()
        
        if any(word in name_lower for word in ['electricity', 'broadband', 'download', 'speed', 'outages']):
            return 'Infrastructure'
        elif any(word in name_lower for word in ['schooling', 'enrolment', 'stem', 'graduates']):
            return 'Education'
        elif any(word in name_lower for word in ['research', 'gerd', 'articles', 'patents', 'royalties']):
            return 'Innovation & Research'
        elif any(word in name_lower for word in ['gfcf', 'gdp', 'ipr']):
            return 'Economic'
        elif any(word in name_lower for word in ['iso', 'imports', 'exports']):
            return 'Trade & Standards'
        else:
            return 'Other'
    
    def transform_sheet_data(self, filename: str, data: List[Dict]) -> Dict[str, Any]:
        """Transform a single sheet's data into standardized format."""
        indicator_name = self.extract_indicator_name(filename)
        category = self.categorize_indicator(indicator_name)
        
        transformed_data = {
            'indicator': indicator_name,
            'category': category,
            'filename': filename,
            'data_points': [],
            'metadata': {
                'total_records': len(data),
                'countries': set(),
                'years': set(),
                'has_country_data': False
            }
        }
        
        for record in data:
            # Skip empty or invalid records
            if not record or all(v is None or v == "" for v in record.values()):
                continue
            
            # Extract country information
            country = None
            country_code = None
            region = None
            income_group = None
            
            for key, value in record.items():
                if key.lower() == 'economy' and value:
                    country = self.clean_string(value)
                elif key.lower() == 'code' and value:
                    country_code = self.clean_string(value)
                elif key.lower() == 'region' and value:
                    region = self.clean_string(value)
                elif key.lower() == 'income_group' and value:
                    income_group = self.clean_string(value)
            
            # Extract data values
            for column, value in record.items():
                if not self.is_data_column(column) or value is None:
                    continue
                
                # Try to convert to number
                try:
                    numeric_value = float(value) if value != "" else None
                except (ValueError, TypeError):
                    continue
                
                if numeric_value is None:
                    continue
                
                # Extract year from column name
                year = self.extract_year_from_column(column)
                if year is None:
                    continue
                
                # Create standardized data point
                data_point = {
                    'country': country or 'Unknown',
                    'country_code': country_code or '',
                    'region': region or 'Unknown',
                    'income_group': income_group or 'Unknown',
                    'year': year,
                    'value': numeric_value,
                    'indicator': indicator_name,
                    'category': category
                }
                
                transformed_data['data_points'].append(data_point)
                
                # Update metadata
                if country:
                    transformed_data['metadata']['countries'].add(country)
                    transformed_data['metadata']['has_country_data'] = True
                transformed_data['metadata']['years'].add(year)
                self.countries.add(country or 'Unknown')
                self.years.add(year)
        
        # Convert sets to lists for JSON serialization
        transformed_data['metadata']['countries'] = list(transformed_data['metadata']['countries'])
        transformed_data['metadata']['years'] = sorted(list(transformed_data['metadata']['years']))
        
        return transformed_data
    
    def create_consolidated_dataset(self, all_indicators: Dict[str, Any]) -> Dict[str, Any]:
        """Create a consolidated dataset with all indicators."""
        consolidated = {
            'metadata': {
                'total_indicators': len(all_indicators),
                'total_countries': len(self.countries),
                'year_range': {
                    'min': min(self.years) if self.years else None,
                    'max': max(self.years) if self.years else None
                },
                'countries': sorted(list(self.countries)),
                'categories': {}
            },
            'indicators': all_indicators,
            'data_points': []
        }
        
        # Group by category
        for indicator_data in all_indicators.values():
            category = indicator_data['category']
            if category not in consolidated['metadata']['categories']:
                consolidated['metadata']['categories'][category] = []
            consolidated['metadata']['categories'][category].append(indicator_data['indicator'])
            
            # Add all data points to consolidated list
            consolidated['data_points'].extend(indicator_data['data_points'])
        
        return consolidated
    
    def transform_all_data(self) -> Dict[str, Any]:
        """Transform all JSON files in the input directory."""
        # Create output directory
        Path(self.output_dir).mkdir(exist_ok=True)
        
        all_indicators = {}
        
        # Process each JSON file
        for filename in os.listdir(self.input_dir):
            if not filename.endswith('.json') or filename == 'conversion_summary.json':
                continue
            
            filepath = os.path.join(self.input_dir, filename)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                print(f"Processing {filename}...")
                transformed = self.transform_sheet_data(filename, data)
                
                if transformed['data_points']:  # Only save if we have actual data
                    all_indicators[transformed['indicator']] = transformed
                    
                    # Save individual indicator file
                    output_file = os.path.join(self.output_dir, f"{transformed['indicator'].replace(' ', '_')}.json")
                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump(transformed, f, indent=2, ensure_ascii=False)
                    
                    print(f"  ✓ Saved {len(transformed['data_points'])} data points")
                else:
                    print(f"  ⚠ No valid data points found")
                    
            except Exception as e:
                print(f"  ✗ Error processing {filename}: {str(e)}")
        
        # Create consolidated dataset
        print("\nCreating consolidated dataset...")
        consolidated = self.create_consolidated_dataset(all_indicators)
        
        # Save consolidated dataset
        consolidated_file = os.path.join(self.output_dir, 'consolidated_dataset.json')
        with open(consolidated_file, 'w', encoding='utf-8') as f:
            json.dump(consolidated, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Consolidated dataset saved with {len(consolidated['data_points'])} total data points")
        
        # Create summary
        summary = {
            'transformation_date': str(Path().cwd()),
            'input_directory': self.input_dir,
            'output_directory': self.output_dir,
            'indicators_processed': len(all_indicators),
            'total_data_points': len(consolidated['data_points']),
            'countries': sorted(list(self.countries)),
            'year_range': {
                'min': min(self.years) if self.years else None,
                'max': max(self.years) if self.years else None
            },
            'categories': consolidated['metadata']['categories']
        }
        
        summary_file = os.path.join(self.output_dir, 'transformation_summary.json')
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Transformation summary saved")
        
        return consolidated

def main():
    """Main function to run the transformation."""
    transformer = DataTransformer()
    result = transformer.transform_all_data()
    
    print(f"\n🎉 Transformation complete!")
    print(f"📊 Processed {len(result['indicators'])} indicators")
    print(f"🌍 Data for {len(result['metadata']['countries'])} countries")
    print(f"📅 Year range: {result['metadata']['year_range']['min']}-{result['metadata']['year_range']['max']}")
    print(f"📁 Output saved to: {transformer.output_dir}/")

if __name__ == "__main__":
    main()
