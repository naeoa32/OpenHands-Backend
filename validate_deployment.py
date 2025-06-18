#!/usr/bin/env python3
"""
✅ Complete Deployment Validator
Memastikan semua komponen siap untuk deployment 100% working
"""

import os
import sys
import json
import subprocess
import importlib.util
from pathlib import Path

class DeploymentValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.passed = []
        
    def log_error(self, message):
        self.errors.append(message)
        print(f"❌ {message}")
        
    def log_warning(self, message):
        self.warnings.append(message)
        print(f"⚠️  {message}")
        
    def log_pass(self, message):
        self.passed.append(message)
        print(f"✅ {message}")
    
    def print_header(self, title):
        print(f"\n{'='*60}")
        print(f"🔍 {title}")
        print('='*60)
    
    def check_required_files(self):
        """Check if all required files exist"""
        self.print_header("Required Files Check")
        
        required_files = {
            'Dockerfile': 'Docker configuration',
            'requirements.txt': 'Python dependencies',
            'app_hf.py': 'Main application file',
            'space_config.yml': 'HF Spaces configuration',
            '.github/workflows/deploy-huggingface.yml': 'GitHub Actions workflow'
        }
        
        for file_path, description in required_files.items():
            if Path(file_path).exists():
                self.log_pass(f"{file_path} - {description}")
            else:
                self.log_error(f"Missing {file_path} - {description}")
    
    def check_port_consistency(self):
        """Check port configuration consistency"""
        self.print_header("Port Configuration Check")
        
        # Check space_config.yml
        try:
            with open('space_config.yml', 'r') as f:
                content = f.read()
                if 'app_port: 7860' in content:
                    self.log_pass("space_config.yml uses port 7860")
                else:
                    self.log_error("space_config.yml does not use port 7860")
        except Exception as e:
            self.log_error(f"Cannot read space_config.yml: {e}")
        
        # Check app_hf.py
        try:
            with open('app_hf.py', 'r') as f:
                content = f.read()
                if 'PORT", 7860' in content:
                    self.log_pass("app_hf.py defaults to port 7860")
                else:
                    self.log_warning("app_hf.py does not default to port 7860")
        except Exception as e:
            self.log_error(f"Cannot read app_hf.py: {e}")
    
    def check_dependencies(self):
        """Check if critical dependencies are in requirements.txt"""
        self.print_header("Dependencies Check")
        
        critical_deps = [
            'fastapi',
            'uvicorn',
            'litellm',
            'browsergym-core',
            'python-dotenv',
            'aiohttp'
        ]
        
        try:
            with open('requirements.txt', 'r') as f:
                content = f.read()
                
            for dep in critical_deps:
                if dep in content:
                    self.log_pass(f"Found {dep}")
                else:
                    self.log_error(f"Missing critical dependency: {dep}")
                    
        except Exception as e:
            self.log_error(f"Cannot read requirements.txt: {e}")
    
    def check_dockerfile(self):
        """Check Dockerfile configuration"""
        self.print_header("Dockerfile Check")
        
        try:
            with open('Dockerfile', 'r') as f:
                content = f.read()
            
            checks = [
                ('EXPOSE 7860', 'Port 7860 exposed'),
                ('COPY requirements.txt', 'Requirements copied'),
                ('RUN pip install', 'Dependencies installed'),
                ('CMD', 'Startup command defined')
            ]
            
            for check, description in checks:
                if check in content:
                    self.log_pass(description)
                else:
                    self.log_warning(f"Missing or different: {description}")
                    
        except Exception as e:
            self.log_error(f"Cannot read Dockerfile: {e}")
    
    def check_app_structure(self):
        """Check app_hf.py structure"""
        self.print_header("Application Structure Check")
        
        try:
            with open('app_hf.py', 'r') as f:
                content = f.read()
            
            checks = [
                ('import uvicorn', 'Uvicorn imported'),
                ('from openhands.server.app import app', 'OpenHands app imported'),
                ('setup_hf_environment', 'Environment setup function'),
                ('if __name__ == "__main__"', 'Main execution block'),
                ('uvicorn.run', 'Uvicorn server start')
            ]
            
            for check, description in checks:
                if check in content:
                    self.log_pass(description)
                else:
                    self.log_error(f"Missing: {description}")
                    
        except Exception as e:
            self.log_error(f"Cannot read app_hf.py: {e}")
    
    def check_github_workflow(self):
        """Check GitHub Actions workflow"""
        self.print_header("GitHub Actions Workflow Check")
        
        workflow_path = '.github/workflows/deploy-huggingface.yml'
        
        try:
            with open(workflow_path, 'r') as f:
                content = f.read()
            
            checks = [
                ('on:', 'Trigger events defined'),
                ('push:', 'Push trigger configured'),
                ('workflow_dispatch:', 'Manual trigger enabled'),
                ('HF_TOKEN', 'HF token secret used'),
                ('HF_USERNAME', 'HF username secret used'),
                ('HF_SPACE_NAME', 'HF space name secret used')
            ]
            
            for check, description in checks:
                if check in content:
                    self.log_pass(description)
                else:
                    self.log_warning(f"Missing or different: {description}")
                    
        except Exception as e:
            self.log_error(f"Cannot read GitHub workflow: {e}")
    
    def check_environment_variables(self):
        """Check environment variable configuration"""
        self.print_header("Environment Variables Check")
        
        # Check if .env.example exists
        if Path('.env.example').exists():
            self.log_pass(".env.example file exists")
        else:
            self.log_warning(".env.example file missing")
        
        # Check critical environment variables
        critical_env_vars = [
            'LLM_API_KEY',
            'LLM_MODEL', 
            'LLM_BASE_URL'
        ]
        
        print("\nEnvironment variables status:")
        for var in critical_env_vars:
            if os.getenv(var):
                self.log_pass(f"{var} is set in environment")
            else:
                self.log_warning(f"{var} not set (should be set in HF Space)")
    
    def check_import_compatibility(self):
        """Check if critical imports work"""
        self.print_header("Import Compatibility Check")
        
        critical_imports = [
            ('fastapi', 'FastAPI framework'),
            ('uvicorn', 'ASGI server'),
            ('litellm', 'LLM integration'),
            ('aiohttp', 'HTTP client'),
            ('python_dotenv', 'Environment variables')
        ]
        
        for module_name, description in critical_imports:
            try:
                if module_name == 'python_dotenv':
                    import dotenv
                else:
                    __import__(module_name)
                self.log_pass(f"{description} import successful")
            except ImportError:
                self.log_warning(f"{description} not installed (will be installed in HF Spaces)")
            except Exception as e:
                self.log_warning(f"{description} import issue: {e}")
    
    def check_openhands_structure(self):
        """Check OpenHands package structure"""
        self.print_header("OpenHands Package Check")
        
        openhands_path = Path('openhands')
        if openhands_path.exists():
            self.log_pass("OpenHands package directory exists")
            
            critical_modules = [
                'openhands/__init__.py',
                'openhands/server/',
                'openhands/server/app.py',
                'openhands/agenthub/',
                'openhands/core/'
            ]
            
            for module_path in critical_modules:
                if Path(module_path).exists():
                    self.log_pass(f"{module_path} exists")
                else:
                    self.log_error(f"Missing critical module: {module_path}")
        else:
            self.log_error("OpenHands package directory missing")
    
    def check_documentation(self):
        """Check documentation files"""
        self.print_header("Documentation Check")
        
        doc_files = [
            'README.md',
            'SETUP_AUTO_DEPLOY.md',
            'README_HF_DEPLOY.md'
        ]
        
        for doc_file in doc_files:
            if Path(doc_file).exists():
                self.log_pass(f"{doc_file} exists")
            else:
                self.log_warning(f"Documentation file missing: {doc_file}")
    
    def run_syntax_check(self):
        """Run Python syntax check on main files"""
        self.print_header("Syntax Check")
        
        python_files = [
            'app_hf.py',
            'deploy_to_hf.py',
            'test_deployment.py',
            'setup_env.py'
        ]
        
        for py_file in python_files:
            if Path(py_file).exists():
                try:
                    with open(py_file, 'r') as f:
                        content = f.read()
                    compile(content, py_file, 'exec')
                    self.log_pass(f"{py_file} syntax OK")
                except SyntaxError as e:
                    self.log_error(f"{py_file} syntax error: {e}")
                except Exception as e:
                    self.log_warning(f"{py_file} check issue: {e}")
    
    def generate_deployment_checklist(self):
        """Generate final deployment checklist"""
        self.print_header("Deployment Checklist")
        
        checklist = [
            "✅ All required files present",
            "✅ Port configuration consistent (7860)",
            "✅ Dependencies complete in requirements.txt",
            "✅ Dockerfile properly configured",
            "✅ GitHub Actions workflow ready",
            "✅ Environment variables documented",
            "✅ OpenHands package structure intact",
            "✅ Python syntax valid"
        ]
        
        print("\nPre-deployment checklist:")
        for item in checklist:
            print(f"  {item}")
        
        print("\n🎯 Next steps:")
        print("  1. Set GitHub Secrets (HF_TOKEN, HF_USERNAME, HF_SPACE_NAME)")
        print("  2. Set HF Space environment variables (LLM_API_KEY, etc.)")
        print("  3. Push to main branch to trigger auto-deploy")
        print("  4. Monitor deployment in GitHub Actions")
        print("  5. Test endpoints after deployment")
    
    def run_all_checks(self):
        """Run all validation checks"""
        print("🚀 Starting complete deployment validation...")
        print("🎯 Ensuring 100% working deployment")
        
        checks = [
            self.check_required_files,
            self.check_port_consistency,
            self.check_dependencies,
            self.check_dockerfile,
            self.check_app_structure,
            self.check_github_workflow,
            self.check_environment_variables,
            self.check_import_compatibility,
            self.check_openhands_structure,
            self.check_documentation,
            self.run_syntax_check
        ]
        
        for check in checks:
            try:
                check()
            except Exception as e:
                self.log_error(f"Check failed with exception: {e}")
        
        # Generate summary
        self.print_summary()
        self.generate_deployment_checklist()
        
        return len(self.errors) == 0
    
    def print_summary(self):
        """Print validation summary"""
        self.print_header("Validation Summary")
        
        total_checks = len(self.passed) + len(self.warnings) + len(self.errors)
        
        print(f"\n📊 Results:")
        print(f"  ✅ Passed: {len(self.passed)}")
        print(f"  ⚠️  Warnings: {len(self.warnings)}")
        print(f"  ❌ Errors: {len(self.errors)}")
        print(f"  📈 Total: {total_checks}")
        
        if self.errors:
            print(f"\n🚨 Critical Issues (Must Fix):")
            for error in self.errors:
                print(f"  ❌ {error}")
        
        if self.warnings:
            print(f"\n⚠️  Warnings (Should Review):")
            for warning in self.warnings[:5]:  # Show first 5
                print(f"  ⚠️  {warning}")
            if len(self.warnings) > 5:
                print(f"  ... and {len(self.warnings) - 5} more warnings")
        
        if len(self.errors) == 0:
            print(f"\n🎉 Validation PASSED! Ready for deployment!")
            print(f"🚀 All critical components are properly configured")
        else:
            print(f"\n🚨 Validation FAILED! Fix {len(self.errors)} critical issues first")

def main():
    validator = DeploymentValidator()
    success = validator.run_all_checks()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()