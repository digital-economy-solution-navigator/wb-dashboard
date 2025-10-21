"""
Examine Excel file structure to understand the data format
"""

import pandas as pd
import os

def examine_excel_file():
    """Examine the Excel file in detail"""
    file_path = "data.xlsx"
    
    if not os.path.exists(file_path):
        print(f"❌ Excel file not found: {file_path}")
        return
    
    print("🔍 EXAMINING EXCEL FILE STRUCTURE")
    print("=" * 60)
    
    try:
        xl = pd.ExcelFile(file_path)
        print(f"📊 Found {len(xl.sheet_names)} sheets:")
        for i, sheet in enumerate(xl.sheet_names, 1):
            print(f"   {i}. {sheet}")
        
        print(f"\n📋 DETAILED ANALYSIS:")
        print("=" * 60)
        
        for sheet_name in xl.sheet_names:
            print(f"\n📄 Sheet: '{sheet_name}'")
            print("-" * 50)
            
            try:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                print(f"   Shape: {df.shape[0]} rows × {df.shape[1]} columns")
                print(f"   Columns: {list(df.columns)}")
                
                # Show data types
                print(f"   Data types:")
                for col, dtype in df.dtypes.items():
                    print(f"     - {col}: {dtype}")
                
                # Show first few rows
                print(f"   First 5 rows:")
                print(df.head(5).to_string(index=False))
                
                # Check for missing values
                missing = df.isnull().sum()
                if missing.sum() > 0:
                    print(f"   Missing values:")
                    for col, count in missing[missing > 0].items():
                        print(f"     - {col}: {count} missing")
                else:
                    print(f"   ✅ No missing values")
                
                # Look for potential indicators
                print(f"   Potential indicators (numeric columns):")
                numeric_cols = [col for col in df.columns if df[col].dtype in ['int64', 'float64']]
                for col in numeric_cols:
                    non_null_count = df[col].count()
                    print(f"     - {col}: {non_null_count} non-null values")
                
                # Look for country-like columns
                print(f"   Potential country columns:")
                for col in df.columns:
                    if df[col].dtype == 'object':
                        unique_vals = df[col].dropna().unique()
                        if len(unique_vals) <= 20:  # Reasonable number of countries
                            print(f"     - {col}: {len(unique_vals)} unique values: {list(unique_vals)[:5]}")
                
                # Look for year-like columns
                print(f"   Potential year columns:")
                for col in df.columns:
                    if df[col].dtype in ['int64', 'float64']:
                        unique_vals = df[col].dropna().unique()
                        if len(unique_vals) > 1 and all(1900 <= v <= 2030 for v in unique_vals if pd.notna(v)):
                            print(f"     - {col}: {len(unique_vals)} unique values: {sorted(unique_vals)[:5]}")
                
            except Exception as e:
                print(f"   ❌ Error reading sheet: {e}")
        
        print(f"\n✅ Analysis complete!")
        
    except Exception as e:
        print(f"❌ Error reading Excel file: {e}")

if __name__ == "__main__":
    examine_excel_file()
