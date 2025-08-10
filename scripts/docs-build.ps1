$ErrorActionPreference = "Stop"

$venvActivate = Join-Path -Path ".venv" -ChildPath "Scripts/Activate.ps1"
if (Test-Path $venvActivate) {
    Write-Host "Activating virtual environment" -ForegroundColor Cyan
    & $venvActivate
} else {
    Write-Host "No virtualenv detected; proceeding with system Python PATH" -ForegroundColor Yellow
}
python -m pip install -r docs/requirements.txt
python -m sphinx -b html docs docs/_build/html
Write-Host "Docs built at docs/_build/html" -ForegroundColor Green
