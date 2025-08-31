# Milk Dashboard 

A comprehensive milk management system for Radhey-Shyam Durgalay.

## Features

-  Dashboard with business metrics and trends
-  Daily log for milk sales and money transactions
-  Customer management system
-  Sweet export module for khoya sales
-  Export functionality (CSV/Excel)
-  Invoice generation
-  Mobile-responsive design

## Version Control

This project uses semantic versioning (MAJOR.MINOR.PATCH).

### Version Management

`ash
# Bump patch version (bug fixes)
.\version.ps1 patch

# Bump minor version (new features)
.\version.ps1 minor

# Bump major version (breaking changes)
.\version.ps1 major

## Deployment
```bash
# Deploy specific version
.\deploy.ps1 -Version "1.0.0" -Environment "production"

# Rollback to previous version
.\rollback.ps1 -Version "1.0.0"
```

## CI/CD Pipeline
This project uses GitHub Actions for continuous integration and deployment.

### Getting Started

1. Clone the repository:

```bash
git clone https://github.com/yadavvinay77/milk-dashboard.git
cd milk-dashboard
```
2. Install dependencies:

```bash
pip install -r requirements.txt
```
3. Initialize database:

```bash
flask db upgrade
```

4. Run the application:

```bash
flask run
```