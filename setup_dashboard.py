"""
Dashboard Setup Script
This script helps set up the Western Balkans Dashboard
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"   Error output: {e.stderr}")
        return False

def check_python_packages():
    """Check if required Python packages are installed"""
    print("🔍 Checking Python packages...")
    
    required_packages = ['pandas', 'openpyxl']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} (missing)")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
        install_command = f"pip install {' '.join(missing_packages)}"
        return run_command(install_command, "Package installation")
    
    return True

def setup_dashboard():
    """Main setup function"""
    print("🚀 WESTERN BALKANS DASHBOARD SETUP")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("index.html"):
        print("❌ index.html not found. Please run this script from the dashboard root directory.")
        return False
    
    print("✅ Dashboard files found")
    
    # Check Python packages
    if not check_python_packages():
        print("❌ Failed to install required packages")
        return False
    
    # Check for data.xlsx
    if not os.path.exists("data/data.xlsx"):
        print("❌ data/data.xlsx not found")
        print("   Please place your Excel data file as data/data.xlsx")
        return False
    
    print("✅ data.xlsx found")
    
    # Run data transformation
    print("\n🔄 Running data transformation...")
    
    # Try comprehensive transformation first
    if run_command("cd data && python transform_data_v2.py", "Comprehensive data transformation"):
        print("✅ Comprehensive transformation completed")
        print("   Dashboard should now work with full features")
        return True
    
    # Fall back to simple transformation
    print("⚠️  Comprehensive transformation failed, trying simple version...")
    if run_command("cd data && python simple_transform.py", "Simple data transformation"):
        print("✅ Simple transformation completed")
        print("   Dashboard will work with basic features")
        print("   Note: Update script.js line 8 to use 'data/transformed_data/consolidated_dataset.json'")
        return True
    
    print("❌ Both transformation methods failed")
    print("   Please check the error messages above and ensure:")
    print("   1. data.xlsx is in the correct format")
    print("   2. Python packages are properly installed")
    print("   3. You have write permissions in the data directory")
    
    return False

def main():
    """Main function"""
    success = setup_dashboard()
    
    if success:
        print("\n🎉 SETUP COMPLETE!")
        print("   You can now open index.html in your web browser")
        print("   The dashboard should load your data successfully")
    else:
        print("\n❌ SETUP FAILED")
        print("   Please check the error messages above and try again")
        print("   You can also run the transformation manually:")
        print("   cd data")
        print("   python transform_data_v2.py")
        print("   OR")
        print("   python simple_transform.py")

if __name__ == "__main__":
    main()
