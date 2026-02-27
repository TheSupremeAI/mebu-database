# Creates a desktop shortcut for MEBU Analytics Platform
# Run once: Right-click → Run with PowerShell

$exePath   = "D:\Claude Project\MEBU Database\MEBU_Analytics.exe"
$shortcut  = "$env:USERPROFILE\Desktop\MEBU Analytics.lnk"

$wsh   = New-Object -ComObject WScript.Shell
$link  = $wsh.CreateShortcut($shortcut)
$link.TargetPath       = $exePath
$link.WorkingDirectory = "D:\Claude Project\MEBU Database"
$link.Description      = "MEBU Residue Hydrocracking Analytics Platform"
$link.IconLocation     = $exePath
$link.Save()

Write-Host "Desktop shortcut created at: $shortcut" -ForegroundColor Green
Read-Host "Press Enter to close"
