$ErrorActionPreference = "Stop"

function Test-PythonCommand {
    param(
        [string]$Command,
        [string[]]$Arguments = @()
    )

    $previousPreference = $ErrorActionPreference
    try {
        $ErrorActionPreference = "SilentlyContinue"
        & $Command @Arguments *> $null
        return $LASTEXITCODE -eq 0
    } catch {
        return $false
    } finally {
        $ErrorActionPreference = $previousPreference
    }
}

$runner = $null

if (Get-Command python -ErrorAction SilentlyContinue) {
    if (Test-PythonCommand "python" @("--version")) {
        $runner = "python"
    }
}

if (-not $runner -and (Get-Command py -ErrorAction SilentlyContinue)) {
    if (Test-PythonCommand "py" @("-3", "--version")) {
        $runner = "py"
    }
}

if (-not $runner) {
    Write-Host "Python no esta instalado. Instala Python 3.11+ antes de compilar."
    exit 1
}

$runningApp = Get-Process ER_Save_Manager_v2_Nexus -ErrorAction SilentlyContinue
if ($runningApp) {
    Write-Host "Cerrando ER_Save_Manager_v2_Nexus.exe para poder recompilar..."
    $runningApp | Stop-Process -Force
}

if ($runner -eq "py") {
    py -3 -m pip install -r requirements.txt
    py -3 -m PyInstaller --clean --noconfirm EldenRingSaveManager-Nexus.spec
} else {
    python -m pip install -r requirements.txt
    python -m PyInstaller --clean --noconfirm EldenRingSaveManager-Nexus.spec
}

$packageRoot = Join-Path (Get-Location) "dist_nexus"
$payloadDir = Join-Path $packageRoot "ER_Save_Manager_v2_Nexus"
$zipPath = Join-Path $packageRoot "ER_Save_Manager_v2_Nexus_v1.0.0-sote.zip"

New-Item -ItemType Directory -Force -Path $payloadDir | Out-Null

Copy-Item -Force "dist\ER_Save_Manager_v2_Nexus.exe" (Join-Path $payloadDir "ER_Save_Manager_v2_Nexus.exe")
Copy-Item -Force "README_NEXUS.md" (Join-Path $payloadDir "README_NEXUS.md")
Copy-Item -Force "LICENSE" (Join-Path $payloadDir "LICENSE.txt")
Copy-Item -Force "CREDITS.md" (Join-Path $payloadDir "CREDITS.md")
Copy-Item -Force "NOTICE.md" (Join-Path $payloadDir "NOTICE.md")
Copy-Item -Force "SECURITY.md" (Join-Path $payloadDir "SECURITY.md")

if (Test-Path $zipPath) {
    Remove-Item -LiteralPath $zipPath -Force
}

Compress-Archive -Path (Join-Path $payloadDir "*") -DestinationPath $zipPath

Write-Host "Nexus package generated at: $zipPath"
