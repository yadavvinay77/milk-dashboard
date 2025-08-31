# Rollback script
param(
    [string]$Version
)

Write-Host " Rolling back to version $Version" -ForegroundColor Yellow

# Checkout the specific version
git checkout tags/v$Version

# Reinstall dependencies
pip install -r requirements.txt

# Run database migrations
$env:FLASK_APP = "manage.py"
flask db upgrade

Write-Host " Rollback to version $Version completed successfully!" -ForegroundColor Green
