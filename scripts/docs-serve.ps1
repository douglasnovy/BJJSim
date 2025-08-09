$ErrorActionPreference = "Stop"

if (-not (Test-Path .venv)) {
    Write-Host "Virtual env not found. Run scripts/setup.ps1 first." -ForegroundColor Yellow
}

& .\.venv\Scripts\Activate.ps1
python -m pip install -r docs/requirements.txt
python -m sphinx_autobuild docs docs/_build/html
