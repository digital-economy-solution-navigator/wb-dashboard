import pandas as pd
import sys

try:
    # Read Excel file
    xl = pd.ExcelFile('data/data.xlsx')
    print(f"Excel file has {len(xl.sheet_names)} sheets:")
    for i, sheet in enumerate(xl.sheet_names, 1):
        print(f"  {i}. {sheet}")
    
    # Check first sheet
    if xl.sheet_names:
        first_sheet = xl.sheet_names[0]
        df = pd.read_excel('data/data.xlsx', sheet_name=first_sheet)
        print(f"\nFirst sheet '{first_sheet}' has {df.shape[0]} rows and {df.shape[1]} columns")
        print(f"Columns: {list(df.columns)}")
        print(f"\nFirst 3 rows:")
        print(df.head(3).to_string())
        
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

