$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot

$projectPython = Join-Path $PSScriptRoot 'venv\Scripts\python.exe'
if (-not (Test-Path $projectPython)) {
    $projectPython = (Get-Command python -ErrorAction Stop).Source
}

& $projectPython -c "import flask, waitress, PyInstaller" 2>$null
if ($LASTEXITCODE -ne 0) {
    & $projectPython -m pip install -r requirements-build.txt
    if ($LASTEXITCODE -ne 0) {
        throw 'Could not install build requirements. Check your internet connection and try again.'
    }
}

& $projectPython -m PyInstaller --noconfirm --onefile --windowed `
    --name LocalMovieStreamer `
    --add-data "templates;templates" `
    --add-data "static;static" `
    main.py
if ($LASTEXITCODE -ne 0) {
    throw 'PyInstaller build failed.'
}

Write-Host "Build complete: $PSScriptRoot\dist\LocalMovieStreamer.exe"
