$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

if (Test-Path ".venv\Scripts\python.exe") {
    $Python = Join-Path $Root ".venv\Scripts\python.exe"
} else {
    $Python = "python"
}

$env:PYTHONPATH = ".;src"
$LogDir = Join-Path $Root "logs"
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null

& $Python "scripts\scanner.py" *>> (Join-Path $LogDir "scan.log")
exit $LASTEXITCODE
