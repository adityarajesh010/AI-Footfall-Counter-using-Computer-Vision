# Quick Start Guide

## Prerequisites
- Python 3.10 or higher
- Internet connection (for downloading YOLOv8 model on first run)

## Installation Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

Or install from backend folder:
```bash
cd backend
pip install -r requirements.txt
```

### 2. Start the Application
```bash
cd backend
python -m uvicorn main:app --reload
```

### 3. Access the Application
Open your browser and go to:
```
http://localhost:8000/static/index.html
```

## Download Test Videos
- Market Square: https://drive.google.com/file/d/1J1aH3KdruJFXLiiRGg2HwR925Adqhv3z/view?usp=drive_link
- Grocery Store: https://drive.google.com/file/d/1bbnGeOpsKlXq--6WW5uJqwCfuH-QFUAe/view?usp=drive_link
- Subway: https://drive.google.com/file/d/1HzbU-OumykCLCCC_n8Nw6V6_ZfAzCOA7/view?usp=drive_link

## Troubleshooting
- If port 8000 is in use: `python -m uvicorn main:app --reload --port 8001`
- YOLOv8 model will be auto-downloaded on first run (~20MB)
- Make sure you're in the `backend` directory when running the server
