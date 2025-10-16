"""
Dashboard Status Checker
This script checks if the dashboard data files exist and provides guidance
"""

import os
import json

def check_dashboard_status():
    print("🔍 CHECKING DASHBOARD STATUS")
    print("=" * 50)
    
    # Check if data directory exists
    data_dir = "data"
    if not os.path.exists(data_dir):
        print("❌ Data directory not found")
        return False
    
    print(f"✅ Data directory exists: {data_dir}")
    
    # Check for Excel file
    excel_file = os.path.join(data_dir, "data.xlsx")
    if os.path.exists(excel_file):
        print(f"✅ Excel file found: {excel_file}")
    else:
        print(f"❌ Excel file not found: {excel_file}")
        print("   Please place your data.xlsx file in the data/ directory")
        return False
    
    # Check for transformation outputs
    transformed_v2_dir = os.path.join(data_dir, "transformed_data_v2")
    transformed_simple_dir = os.path.join(data_dir, "transformed_data")
    
    v2_exists = os.path.exists(transformed_v2_dir)
    simple_exists = os.path.exists(transformed_simple_dir)
    
    print(f"\n📊 TRANSFORMATION STATUS:")
    print(f"   Comprehensive transformation: {'✅' if v2_exists else '❌'}")
    print(f"   Simple transformation: {'✅' if simple_exists else '❌'}")
    
    if v2_exists:
        consolidated_file = os.path.join(transformed_v2_dir, "consolidated_dataset.json")
        if os.path.exists(consolidated_file):
            print(f"   ✅ Consolidated dataset: {consolidated_file}")
            try:
                with open(consolidated_file, 'r') as f:
                    data = json.load(f)
                    print(f"   📈 Data points: {len(data.get('data_points', []))}")
                    print(f"   🌍 Countries: {len(data.get('metadata', {}).get('countries', []))}")
                    print(f"   📅 Years: {len(data.get('metadata', {}).get('years', []))}")
            except Exception as e:
                print(f"   ❌ Error reading consolidated dataset: {e}")
        else:
            print(f"   ❌ Consolidated dataset not found: {consolidated_file}")
    
    if simple_exists:
        consolidated_file = os.path.join(transformed_simple_dir, "consolidated_dataset.json")
        if os.path.exists(consolidated_file):
            print(f"   ✅ Simple consolidated dataset: {consolidated_file}")
        else:
            print(f"   ❌ Simple consolidated dataset not found: {consolidated_file}")
    
    # Check dashboard files
    print(f"\n🖥️  DASHBOARD FILES:")
    dashboard_files = ["index.html", "script.js", "styles.css"]
    for file in dashboard_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file}")
    
    # Provide recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    
    if not v2_exists and not simple_exists:
        print("   1. Run the data transformation script:")
        print("      cd data")
        print("      python transform_data_v2.py")
        print("      OR")
        print("      python simple_transform.py")
    elif v2_exists:
        print("   ✅ Data transformation complete - dashboard should work!")
    elif simple_exists:
        print("   ⚠️  Simple transformation found - update script.js to use:")
        print("      'data/transformed_data/consolidated_dataset.json'")
    
    return True

if __name__ == "__main__":
    check_dashboard_status()
