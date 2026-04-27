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
    Write-Host "Python no esta instalado. Instala Python 3.11+ desde python.org o usa el ejecutable compilado."
    exit 1
}

if ($runner -eq "py") {
    py -3 -m pip install -r requirements.txt
    py -3 app.py
} else {
    python -m pip install -r requirements.txt
    python app.py
}
