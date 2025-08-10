Param(
    [int]$Port = 8000,
    [string]$BindHost = "127.0.0.1",
    [int]$MaxTries = 15,
    [int]$DelayMs = 250
)

$ErrorActionPreference = "Stop"

function Test-PortFree {
    param([string]$H, [int]$P)
    try {
        $client = New-Object System.Net.Sockets.TcpClient
        $client.Connect($H, $P)
        $client.Close()
        return $false
    }
    catch {
        return $true
    }
}

if (-not (Test-Path .venv)) {
    Write-Host "Virtual env not found. Run scripts/setup.ps1 first." -ForegroundColor Yellow
}

& .\.venv\Scripts\Activate.ps1

while (-not (Test-PortFree -H $BindHost -P $Port)) {
    $Port++
    if ($Port -gt 65500) { throw "No free port found" }
}

Write-Host "Starting server on http://${BindHost}:${Port}" -ForegroundColor Cyan

$env:UVICORN_WORKERS = "1"
$p = Start-Process -FilePath python -ArgumentList "-m", "uvicorn", "bjjsim.web.app:create_app", "--factory", "--host", $BindHost, "--port", $Port -PassThru -NoNewWindow

$ok = $false
for ($i = 0; $i -lt $MaxTries; $i++) {
    try {
        $r = Invoke-WebRequest -Uri "http://${BindHost}:${Port}/api/sim/state" -UseBasicParsing -TimeoutSec 2
        if ($r.StatusCode -eq 200) { $ok = $true; break }
    }
    catch { }
    Start-Sleep -Milliseconds $DelayMs
}

if (-not $ok) {
    try { Stop-Process -Id $p.Id -Force } catch { }
    throw "Server did not become ready in time"
}

Write-Host "Server ready: http://${BindHost}:${Port}" -ForegroundColor Green
Write-Host "Press Ctrl+C in this window to stop."

Start-Process "http://${BindHost}:${Port}/"
Wait-Process -Id $p.Id
