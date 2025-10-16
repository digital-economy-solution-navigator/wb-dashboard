import pandas as pd
import json
import os

def analyze_excel_structure():
    """Analyze the structure of the updated data.xlsx file"""
    
    print("🔍 ANALYZING NEW DATA STRUCTURE")
    print("=" * 60)
    
    # Read the Excel file
    try:
        xl = pd.ExcelFile('data/data.xlsx')
        print(f"📊 Found {len(xl.sheet_names)} sheets:")
        for i, sheet in enumerate(xl.sheet_names, 1):
            print(f"   {i}. {sheet}")
        
        print("\n" + "=" * 60)
        print("📋 DETAILED SHEET ANALYSIS:")
        print("=" * 60)
        
        sheet_analysis = {}
        
        for sheet_name in xl.sheet_names:
            print(f"\n📄 SHEET: {sheet_name}")
            print("-" * 40)
            
            try:
                df = pd.read_excel('data/data.xlsx', sheet_name=sheet_name)
                
                # Basic info
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
                sheet_analysis[sheet_name] = {
                    'shape': df.shape,
                    'columns': list(df.columns),
                    'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()},
                    'sample_data': df.head(3).to_dict('records'),
                    'missing_values': missing[missing > 0].to_dict()
                }
                
            except Exception as e:
                print(f"   ❌ Error reading sheet: {e}")
                sheet_analysis[sheet_name] = {'error': str(e)}
        
        # Save analysis to JSON
        with open('data_structure_analysis.json', 'w') as f:
            json.dump(sheet_analysis, f, indent=2, default=str)
        
        print(f"\n💾 Analysis saved to: data_structure_analysis.json")
        
        # Try to identify the main data sheet
        print(f"\n🎯 IDENTIFYING MAIN DATA SHEET:")
        print("-" * 40)
        
        for sheet_name, analysis in sheet_analysis.items():
            if 'error' not in analysis:
                shape = analysis['shape']
                columns = analysis['columns']
                
                # Look for indicators of main data sheet
                indicators = []
                if shape[0] > 10:  # Has substantial data
                    indicators.append("substantial data")
                if any('country' in col.lower() for col in columns):
                    indicators.append("country column")
                if any('year' in col.lower() for col in columns):
                    indicators.append("year column")
                if any('value' in col.lower() or 'indicator' in col.lower() for col in columns):
                    indicators.append("value/indicator columns")
                
                if indicators:
                    print(f"   📊 {sheet_name}: {', '.join(indicators)}")
        
        return sheet_analysis
        
    except Exception as e:
        print(f"❌ Error reading Excel file: {e}")
        return None

if __name__ == "__main__":
    analysis = analyze_excel_structure()

