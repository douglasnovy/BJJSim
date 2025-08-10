Param(
    [switch]$Force
)

$ErrorActionPreference = "Stop"

Write-Host "Creating virtual environment (.venv)" -ForegroundColor Cyan
if (Test-Path .venv) {
    if ($Force) { Remove-Item -Recurse -Force .venv }
}
python -m venv .venv

Write-Host "Activating virtual environment" -ForegroundColor Cyan
& .\.venv\Scripts\Activate.ps1

Write-Host "Upgrading pip" -ForegroundColor Cyan
python -m pip install --upgrade pip

Write-Host "Installing dev tooling (ruff, black, mypy, pytest, pre-commit)" -ForegroundColor Cyan
pip install ruff black mypy pytest pre-commit

Write-Host "Installing pre-commit hooks" -ForegroundColor Cyan
pre-commit install

Write-Host "Installing project package and dependencies (-e .)" -ForegroundColor Cyan
pip install -e .

Write-Host "Done. To activate later: .\\.venv\\Scripts\\Activate.ps1" -ForegroundColor Green
