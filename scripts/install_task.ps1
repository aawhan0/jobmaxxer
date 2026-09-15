$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$Runner = Join-Path $Root "scripts\run_scan.ps1"

$Action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$Runner`""
$Trigger = New-ScheduledTaskTrigger -Daily -At 9:00AM
$Settings = New-ScheduledTaskSettingsSet -StartWhenAvailable

Register-ScheduledTask -TaskName "Jobmaxxer Daily Scan" -Action $Action -Trigger $Trigger -Settings $Settings -Description "Run Jobmaxxer daily job scan" -Force
Write-Host "Jobmaxxer scheduled task installed for 9:00 AM daily."
