# Version management script
param(
    [string]$BumpType = "patch"  # patch, minor, major
)

# Read current version
$currentVersion = Get-Content -Path "VERSION" -Raw
$versionParts = $currentVersion.Trim().Split('.')

$major = [int]$versionParts[0]
$minor = [int]$versionParts[1]
$patch = [int]$versionParts[2]

# Bump version
switch ($BumpType.ToLower()) {
    "major" {
        $major++
        $minor = 0
        $patch = 0
    }
    "minor" {
        $minor++
        $patch = 0
    }
    "patch" {
        $patch++
    }
    default {
        Write-Error "Invalid bump type. Use 'major', 'minor', or 'patch'"
        exit 1
    }
}

$newVersion = "$major.$minor.$patch"

# Update version file
Set-Content -Path "VERSION" -Value $newVersion

# Update changelog (you'll need to add this manually)
Write-Host " Please update CHANGELOG.md with changes for version $newVersion" -ForegroundColor Yellow

# Create git tag
git add VERSION
git commit -m "Bump version to $newVersion"
git tag -a "v$newVersion" -m "Release version $newVersion"

Write-Host " Version bumped to $newVersion" -ForegroundColor Green
Write-Host " Next steps:" -ForegroundColor Cyan
Write-Host "1. Update CHANGELOG.md with your changes" -ForegroundColor Cyan
Write-Host "2. Run: git push origin main --tags" -ForegroundColor Cyan
