"""
Validation script to check all imports and basic functionality
Run this before deployment: python validate.py
"""
import sys

def check_imports():
    """Check if all required packages can be imported"""
    print("🔍 Checking imports...")
    
    try:
        import streamlit
        print("✅ streamlit")
    except ImportError as e:
        print(f"❌ streamlit: {e}")
        return False
    
    try:
        import pandas
        print("✅ pandas")
    except ImportError as e:
        print(f"❌ pandas: {e}")
        return False
    
    try:
        import numpy
        print("✅ numpy")
    except ImportError as e:
        print(f"❌ numpy: {e}")
        return False
    
    try:
        import sklearn
        print("✅ scikit-learn")
    except ImportError as e:
        print(f"❌ scikit-learn: {e}")
        return False
    
    try:
        import qiskit
        print("✅ qiskit")
    except ImportError as e:
        print(f"❌ qiskit: {e}")
        return False
    
    try:
        import openpyxl
        print("✅ openpyxl")
    except ImportError as e:
        print(f"❌ openpyxl: {e}")
        return False
    
    return True

def check_modules():
    """Check if local modules can be imported"""
    print("\n🔍 Checking local modules...")
    
    try:
        from model.preprocessing import preprocess_data
        print("✅ model.preprocessing")
    except ImportError as e:
        print(f"❌ model.preprocessing: {e}")
        return False
    
    try:
        from model.quantum_encoding import angle_encoding
        print("✅ model.quantum_encoding")
    except ImportError as e:
        print(f"❌ model.quantum_encoding: {e}")
        return False
    
    try:
        from model.classifier import train_and_test_classifier
        print("✅ model.classifier")
    except ImportError as e:
        print(f"❌ model.classifier: {e}")
        return False
    
    return True

def check_files():
    """Check if required files exist"""
    print("\n🔍 Checking required files...")
    
    import os
    
    required_files = [
        'app.py',
        'requirements.txt',
        'model/__init__.py',
        'model/preprocessing.py',
        'model/quantum_encoding.py',
        'model/classifier.py',
        '.streamlit/config.toml'
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING")
            all_exist = False
    
    return all_exist

def main():
    """Run all validation checks"""
    print("=" * 50)
    print("QUANTUMIDS Deployment Validation")
    print("=" * 50)
    
    checks = [
        ("Imports", check_imports),
        ("Local Modules", check_modules),
        ("Required Files", check_files)
    ]
    
    results = []
    for name, check_func in checks:
        result = check_func()
        results.append((name, result))
    
    print("\n" + "=" * 50)
    print("Validation Results:")
    print("=" * 50)
    
    all_passed = True
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name}: {status}")
        if not result:
            all_passed = False
    
    print("=" * 50)
    if all_passed:
        print("🎉 All checks passed! Ready for deployment.")
        return 0
    else:
        print("⚠️  Some checks failed. Please fix errors before deploying.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

