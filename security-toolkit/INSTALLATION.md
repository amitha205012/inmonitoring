# Installation & Setup Guide

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

## Step-by-Step Installation

### 1. Clone Repository
```bash
git clone https://github.com/amitha205012/inmonitoring.git
cd inmonitoring/security-toolkit
```

### 2. Create Virtual Environment
```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Upgrade pip
```bash
pip install --upgrade pip
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Create Environment File
```bash
cp .env.example .env
# Edit .env with your settings
```

### 6. Run Individual Modules

#### Password Analyzer
```bash
cd 1_password_strength_analyzer
python password_analyzer.py
```

#### Vulnerability Scanner
```bash
cd 2_vulnerability_scanner
python scanner.py
```

#### Phishing Detection
```bash
cd 3_phishing_detection
python phishing_model.py
```

#### Secure Login System
```bash
cd 4_secure_login_system
python app.py
# Visit http://localhost:5000
```

## Troubleshooting

### ModuleNotFoundError
```bash
# Make sure virtual environment is activated
# and dependencies are installed
pip install -r requirements.txt
```

### Port Already in Use
```bash
# Change port in app.py
app.run(port=5001)
```

### Database Issues
```bash
# Remove old database
rm 4_secure_login_system/secure_auth.db

# Recreate on next run
python app.py
```

### SSL/TLS Issues
```bash
# Update certificates
pip install --upgrade certifi
```

## Verification

To verify installation:
```bash
# Check Python version
python --version

# Check installed packages
pip list | grep -E "Flask|scikit|bcrypt"

# Test imports
python -c "import flask, sklearn, bcrypt; print('All imports successful!')"
```

## Next Steps
- Read QUICK_START.md for 5-minute tutorial
- Review README_COMPLETE.md for detailed documentation
- Check SETUP_GUIDE.md for advanced configuration
