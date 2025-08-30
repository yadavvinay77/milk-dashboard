Write-Host "Bootstrapping Radhey-Shyam Durgalay..." -ForegroundColor Cyan

# Ensure venv recommended (optional)
# python -m venv .venv; .\.venv\Scripts\Activate.ps1

pip install -r .\requirements.txt

$env:FLASK_APP = "manage.py"
$env:FLASK_ENV = "development"

# Fresh DB
if (Test-Path .\migrations) { Remove-Item -Recurse -Force .\migrations }
if (Test-Path .\instance\milk_dashboard.db) { Remove-Item -Force .\instance\milk_dashboard.db }

flask db init
flask db migrate -m "Initial schema"
flask db upgrade

Write-Host "Starting Flask..." -ForegroundColor Green
flask run