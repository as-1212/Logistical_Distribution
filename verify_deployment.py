#!/usr/bin/env python3
"""
Quick deployment validation script
Verifies all components are properly configured
"""

import os
import sys
import json

def check_file_exists(path, description):
    exists = os.path.exists(path)
    status = "✅" if exists else "❌"
    print(f"  {status} {description}")
    return exists

def check_env_file(path, description):
    exists = os.path.exists(path)
    status = "✅" if exists else "⚠️"
    print(f"  {status} {description}")
    return exists

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def main():
    print("\n🚀 Smart Logistics - Deployment Readiness Check")
    print("="*60)
    
    all_good = True
    
    # Check root files
    print_section("📁 Root Configuration Files")
    all_good &= check_file_exists("Procfile", "Procfile (Render process config)")
    all_good &= check_file_exists("render.yaml", "render.yaml (Render blueprint)")
    all_good &= check_file_exists(".env.example", ".env.example (Root environment template)")
    all_good &= check_file_exists("build.sh", "build.sh (Build script)")
    all_good &= check_file_exists("dev.sh", "dev.sh (Development startup)")
    all_good &= check_file_exists("start.sh", "start.sh (Production startup)")
    
    # Check backend
    print_section("🔧 Backend Configuration")
    all_good &= check_file_exists("smart-logistics-backend/server.js", "server.js (Express server)")
    all_good &= check_file_exists("smart-logistics-backend/package.json", "package.json (Dependencies)")
    all_good &= check_file_exists("smart-logistics-backend/.env.example", ".env.example (Backend env template)")
    
    # Check frontend
    print_section("📊 Frontend Configuration")
    all_good &= check_file_exists("smart-logistics-frontend/app.py", "app.py (Streamlit app)")
    all_good &= check_file_exists("smart-logistics-frontend/dashboard.py", "dashboard.py (Dashboard components)")
    all_good &= check_file_exists("smart-logistics-frontend/map_utils.py", "map_utils.py (Map visualization)")
    all_good &= check_file_exists("smart-logistics-frontend/requirements.txt", "requirements.txt (Python dependencies)")
    all_good &= check_file_exists("smart-logistics-frontend/.env.example", ".env.example (Frontend env template)")
    
    # Check ML engine
    print_section("🧠 ML Engine Configuration")
    all_good &= check_file_exists("smart-logistics-ml/ml_engine.py", "ml_engine.py (ML processing)")
    all_good &= check_file_exists("smart-logistics-ml/requirements.txt", "requirements.txt (ML dependencies)")
    
    # Check documentation
    print_section("📖 Documentation")
    all_good &= check_file_exists("SETUP_GUIDE.md", "SETUP_GUIDE.md (Complete setup guide)")
    all_good &= check_file_exists("RENDER_DEPLOYMENT.md", "RENDER_DEPLOYMENT.md (Deployment guide)")
    all_good &= check_file_exists("DEPLOYMENT_CHECKLIST.md", "DEPLOYMENT_CHECKLIST.md (Verification)")
    all_good &= check_file_exists("DEPLOYMENT_SUMMARY.md", "DEPLOYMENT_SUMMARY.md (Executive summary)")
    all_good &= check_file_exists("QUICK_REFERENCE.md", "QUICK_REFERENCE.md (Quick reference)")
    all_good &= check_file_exists("test_integration.py", "test_integration.py (Integration tests)")
    
    # Check environment files
    print_section("🔐 Environment Files Status")
    env_exists = os.path.exists(".env")
    if env_exists:
        print("  ⚠️  .env exists (remove before deployment)")
    else:
        print("  ✅ .env not present (good for git)")
    
    backend_env = os.path.exists("smart-logistics-backend/.env")
    if backend_env:
        print("  ⚠️  Backend .env exists (remove before deployment)")
    else:
        print("  ✅ Backend .env not present (good for git)")
    
    frontend_env = os.path.exists("smart-logistics-frontend/.env")
    if frontend_env:
        print("  ⚠️  Frontend .env exists (remove before deployment)")
    else:
        print("  ✅ Frontend .env not present (good for git)")
    
    # Check Node dependencies
    print_section("📦 Dependencies Status")
    backend_nm = os.path.exists("smart-logistics-backend/node_modules")
    status = "✅ Installed" if backend_nm else "⚠️  Not installed (run ./build.sh)"
    print(f"  {status} Backend node_modules")
    
    # Summary
    print_section("✨ Deployment Readiness Summary")
    
    if all_good:
        print("\n  ✅ ALL CHECKS PASSED!")
        print("\n  Your project is ready to deploy to Render!")
        print("\n  Next steps:")
        print("  1. ./build.sh          - Install all dependencies")
        print("  2. ./dev.sh            - Test locally")
        print("  3. git push origin main - Push to GitHub")
        print("  4. Go to render.com    - Deploy!")
        return 0
    else:
        print("\n  ⚠️  Some checks failed. Please verify all files are present.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
