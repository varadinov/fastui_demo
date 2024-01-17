# Requirements
Python 3.11.X is required
```bash
python --version
```
Python 3.11.1

# Python virtual environment
* Create venv
```bash
python -m venv venv
```
* Activate venv
```bash
source ./venv/bin/activate
```

# Install dependencies
```bash
pip install -r requirements.txt
```
* FastAPI
* FastUI
* Uvicorn
* PyJWT
* python-multiform

# Rum demo
```bash
cd demoX_xxxxx
uvicorn main:app
```