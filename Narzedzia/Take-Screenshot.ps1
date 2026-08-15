# Zrzut ekranu do folderu Obsidian na Windows lab (.57).
# Uruchom w PowerShell na hoście z pulpitem. Nie trzyma haseł.
param(
    [string]$DestDir = "C:\Users\Administrator\Documents\Obsidian\Screenshots"
)

New-Item -ItemType Directory -Force -Path $DestDir | Out-Null
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
$bitmap = New-Object System.Drawing.Bitmap $screen.Width, $screen.Height
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.CopyFromScreen($screen.X, $screen.Y, 0, 0, $screen.Size)
$name = "screen_{0:yyyy-MM-dd_HH-mm-ss}.png" -f (Get-Date)
$path = Join-Path $DestDir $name
$bitmap.Save($path)
$graphics.Dispose()
$bitmap.Dispose()
Write-Host "zapisano $path"

# Opcjonalnie: skopiuj na .133 (klucz SSH musi być już ustawiony)
# scp $path root@5.175.189.133:/root/obsidian-vault/Screenshots/
