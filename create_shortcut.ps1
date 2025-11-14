param(
    [string]$LinkName = "Airport Tracker",
    [string]$TargetScript = "start_background.ps1"
)

$desktop = [Environment]::GetFolderPath('Desktop')
$wsh = New-Object -ComObject WScript.Shell
$shortcut = $wsh.CreateShortcut("$desktop\$LinkName.lnk")
$fullTarget = Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Definition) $TargetScript
$shortcut.TargetPath = "powershell.exe"
$shortcut.Arguments = "-ExecutionPolicy Bypass -File `"$fullTarget`""
$shortcut.WorkingDirectory = Split-Path -Parent $fullTarget
$shortcut.IconLocation = "$fullTarget,0"
$shortcut.Save()
Write-Host "Shortcut created on desktop: $desktop\$LinkName.lnk"