# build-forge.ps1 -- walk the pre-26 Forge cells: cog-gen -> gradle build -> dist/.
# Usage: pwsh -File scripts\build-forge.ps1 [1.21.8 ...]   (no args = all pre-26 cells)
# Forge has no 26 line (FG6 ceiling 1.21.8). Coverage notes:
#   1.20.2 cell serves MC 1.20.2-1.20.4 (Forge 48/49, IGuiOverlay era) -- Forge-loader users there (2026-07-04).
#   1.21.5 cell = MC 1.21.5 only; 1.21.8 cell = MC 1.21.8 only.
# ORPHAN Forge builds (HUD-overlay registration API REMOVED -- only CustomizeGuiOverlayEvent +
#   RenderPlayerEvent present; EH3 has no HUD hook, verified by javap/compile 2026-07-04):
#   Forge 51 (1.21), 53 (1.21.3), 54 (1.21.4), 56 (1.21.6), 57 (1.21.7). The overlay API exists ONLY
#   at 50 (1.20.6), 52 (1.21.1), 55 (1.21.5), 58 (1.21.8) -- the versions with cells. Also 1.21.2 =
#   Forge never shipped; Forge dead after 1.21.8.
param([Parameter(ValueFromRemainingArguments)][string[]]$Only)
$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path $PSScriptRoot -Parent
$dist = Join-Path $repoRoot 'dist'
New-Item -ItemType Directory -Force -Path $dist | Out-Null
$prog = Join-Path $repoRoot 'scripts\_build-forge-progress.txt'
Remove-Item $prog -ErrorAction SilentlyContinue

$cells = @('1.20','1.20.1','1.20.2','1.20.6','1.21.1','1.21.5','1.21.8')
if ($Only) { $cells = $cells | Where-Object { $Only -contains $_ } }

foreach ($v in $cells) {
    $cell = Join-Path $repoRoot ('Forge\' + $v)
    if (-not (Test-Path $cell)) { Add-Content $prog "$v MISSING-CELL"; continue }
    Add-Content $prog "=== $v START $(Get-Date -Format HH:mm:ss) ==="
    & pwsh -NoProfile -File (Join-Path $PSScriptRoot 'cog-gen.ps1') -Cell ('Forge/' + $v) *>> $prog
    if ($LASTEXITCODE -ne 0) { Add-Content $prog "$v COG-FAIL"; continue }
    Push-Location $cell
    Get-ChildItem "$cell\build\libs\*.jar" -ErrorAction SilentlyContinue | Remove-Item -Force
    & "$cell\gradlew.bat" clean build --console=plain *> "$cell\_build.log"
    $code = $LASTEXITCODE
    Pop-Location
    $jar = Get-ChildItem "$cell\build\libs\*.jar" -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -notmatch 'sources|dev' } | Select-Object -First 1
    $warn = (Select-String -Path "$cell\_build.log" -CaseSensitive -Pattern 'warning:|warning\b.*\[' -ErrorAction SilentlyContinue | Measure-Object).Count
    if ($code -eq 0 -and $jar) {
        Copy-Item $jar.FullName (Join-Path $dist $jar.Name) -Force
        Add-Content $prog "$v OK -> $($jar.Name) (warnings: $warn)"
    } else {
        Add-Content $prog "$v FAIL exit=$code (see Forge\$v\_build.log)"
    }
}
Add-Content $prog "ALLDONE $(Get-Date -Format HH:mm:ss)"
