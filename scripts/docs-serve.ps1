$ErrorActionPreference = "Stop"

$venvActivate = Join-Path -Path ".venv" -ChildPath "Scripts/Activate.ps1"
if (Test-Path $venvActivate) {
    Write-Host "Activating virtual environment" -ForegroundColor Cyan
    & $venvActivate
} else {
    Write-Host "No virtualenv detected; proceeding with system Python PATH" -ForegroundColor Yellow
}
python -m pip install -r docs/requirements.txt
python -m sphinx_autobuild docs docs/_build/html
