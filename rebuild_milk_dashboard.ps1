# Milk Dashboard Project Setup Script
# This script will clean up and create the basic structure

$projectDir = "C:\Users\yadav\Documents\Projects\milk_dashboard"

Write-Host "🚀 Starting Milk Dashboard Project Setup..." -ForegroundColor Cyan

# Remove existing project files
Write-Host "🧹 Cleaning up existing project..." -ForegroundColor Yellow
if (Test-Path $projectDir) {
    Remove-Item -Recurse -Force $projectDir -ErrorAction SilentlyContinue
}
Start-Sleep -Seconds 2

# Create directory structure
Write-Host "📁 Creating directory structure..." -ForegroundColor Green
$directories = @(
    $projectDir,
    "$projectDir\app",
    "$projectDir\app\routes",
    "$projectDir\app\utils",
    "$projectDir\app\models",
    "$projectDir\blueprints",
    "$projectDir\blueprints\sweet_export",
    "$projectDir\static",
    "$projectDir\static\css",
    "$projectDir\static\js",
    "$projectDir\templates",
    "$projectDir\templates\customers",
    "$projectDir\templates\partials",
    "$projectDir\templates\logs",
    "$projectDir\templates\sweet_export",
    "$projectDir\instance"
)

foreach ($dir in $directories) {
    New-Item -ItemType Directory -Path $dir -Force | Out-Null
}

# Create basic files
Write-Host "📝 Creating basic configuration files..." -ForegroundColor Yellow

# Create requirements.txt
@"
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-Migrate==4.0.5
pandas==2.0.3
XlsxWriter==3.1.2
"@ | Set-Content "$projectDir\requirements.txt"

# Create config.py
@"
import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "instance", "milk_dashboard.db")
os.makedirs(os.path.join(BASE_DIR, "instance"), exist_ok=True)

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    DEFAULT_MILK_RATE = 190.0
    DEFAULT_KHOYA_RATE = 310.0
"@ | Set-Content "$projectDir\config.py"

# Create basic __init__.py files
"# This file makes directories Python packages" | Set-Content "$projectDir\app\__init__.py"
"# Blueprint initialization" | Set-Content "$projectDir\blueprints\sweet_export\__init__.py"

Write-Host "✅ Basic project structure created!" -ForegroundColor Green
Write-Host "📋 Next steps:" -ForegroundColor Cyan
Write-Host "1. Run: pip install -r requirements.txt" -ForegroundColor Yellow
Write-Host "2. I'll provide the remaining files separately" -ForegroundColor Yellow