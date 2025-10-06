#!/usr/bin/env python3
"""
Excel to JSON Converter
Reads an Excel file and converts all sheets to JSON format for dashboard use.
"""

import pandas as pd
import json
import os
from pathlib import Path

def excel_to_json(excel_file_path, output_dir="json_output"):
    """
    Convert Excel file sheets to JSON format.
    
    Args:
        excel_file_path (str): Path to the Excel file
        output_dir (str): Directory to save JSON files
    """
    try:
        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(exist_ok=True)
        
        # Read all sheets from Excel file
        excel_file = pd.ExcelFile(excel_file_path)
        sheet_names = excel_file.sheet_names
        
        print(f"Found {len(sheet_names)} sheets: {sheet_names}")
        
        # Convert each sheet to JSON
        for sheet_name in sheet_names:
            print(f"Processing sheet: {sheet_name}")
            
            # Read the sheet
            df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
            
            # Clean column names (remove spaces, special characters)
            df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace('[^a-zA-Z0-9_]', '', regex=True)
            
            # Handle NaN values - convert to None for JSON serialization
            df = df.where(pd.notnull(df), None)
            
            # Replace any remaining NaN values with None
            df = df.replace({pd.NA: None})
            
            # Convert to JSON-serializable format
            json_data = df.to_dict('records')
            
            # Clean up any remaining NaN values in the data
            def clean_nan(obj):
                if isinstance(obj, dict):
                    return {k: clean_nan(v) for k, v in obj.items()}
                elif isinstance(obj, list):
                    return [clean_nan(item) for item in obj]
                elif pd.isna(obj) or str(obj) == 'nan' or str(obj) == 'NaN':
                    return None
                else:
                    return obj
            
            json_data = clean_nan(json_data)
            
            # Create output filename
            safe_sheet_name = "".join(c for c in sheet_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_sheet_name = safe_sheet_name.replace(' ', '_')
            output_file = os.path.join(output_dir, f"{safe_sheet_name}.json")
            
            # Write JSON file
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False, default=str)
            
            print(f"  ✓ Saved {len(json_data)} records to {output_file}")
        
        # Create a summary file with metadata
        summary = {
            "source_file": excel_file_path,
            "sheets_processed": len(sheet_names),
            "sheet_names": sheet_names,
            "output_directory": output_dir,
            "files_created": [f"{name.replace(' ', '_')}.json" for name in sheet_names]
        }
        
        summary_file = os.path.join(output_dir, "conversion_summary.json")
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Conversion complete!")
        print(f"✓ Summary saved to: {summary_file}")
        print(f"✓ All JSON files saved to: {output_dir}/")
        
        return summary
        
    except Exception as e:
        print(f"Error processing Excel file: {str(e)}")
        return None

def main():
    """Main function to run the conversion."""
    excel_file = "data.xlsx"
    
    if not os.path.exists(excel_file):
        print(f"Error: {excel_file} not found in current directory")
        return
    
    print(f"Converting {excel_file} to JSON...")
    result = excel_to_json(excel_file)
    
    if result:
        print("\nConversion successful!")
    else:
        print("\nConversion failed!")

if __name__ == "__main__":
    main()
