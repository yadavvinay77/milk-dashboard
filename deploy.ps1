# Deployment script for Milk Dashboard
param(
    [string]$Version,
    [string]$Environment = "production"
)

Write-Host " Deploying Milk Dashboard v$Version to $Environment" -ForegroundColor Cyan

# Update version file
Set-Content -Path "VERSION" -Value $Version

# Install dependencies
Write-Host " Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Run database migrations
Write-Host " Running database migrations..." -ForegroundColor Yellow
$env:FLASK_APP = "manage.py"
flask db upgrade

Write-Host " Deployment completed successfully!" -ForegroundColor Green
Write-Host "Version: $Version" -ForegroundColor Cyan
Write-Host "Environment: $Environment" -ForegroundColor Cyan
