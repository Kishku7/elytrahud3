# build-neoforge.ps1 -- ALL NeoForge builds: pre-26 cells (cog-gen -> gradle) AND the 26 line (matrix).
# Usage: pwsh -File scripts\build-neoforge.ps1 [1.21.8 26.2 ...]   (no args = everything; no 26.3 -- loader gap)
# NeoForge <=1.20.1 has NO cell: the Forge 1.20.1 jar serves it (fork point, tagged forge+neoforge).
param([Parameter(ValueFromRemainingArguments)][string[]]$Only)
$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path $PSScriptRoot -Parent
$dist = Join-Path $repoRoot 'dist'
New-Item -ItemType Directory -Force -Path $dist | Out-Null
$prog = Join-Path $repoRoot 'scripts\_build-neoforge-progress.txt'
Remove-Item $prog -ErrorAction SilentlyContinue

# ---- pre-26 cells (cog-materialized; per-cell gradle.properties pin org.gradle.java.home) ----
$cells = @('1.20.4','1.20.6','1.21','1.21.1','1.21.2','1.21.5','1.21.8','1.21.10','1.21.11')
# ---- 26 line (matrix; cell NeoForge/26 srcDirs _codegen/cog_sources/master directly, no cog).
#      pf = per-26.X resource pack_format (authoritative: Memory/knowledge/pack-formats.md) ----
$matrix26 = [ordered]@{
    '26.1' = @{ mc='26.1.2'; neo='26.1.2.30-beta'; neoRange='[26.1.2.0-beta,)'; mcRange='[26.1,26.2)'; pf='84' }
    '26.2' = @{ mc='26.2';   neo='26.2.0.1-beta';  neoRange='[26.2.0-alpha,)';  mcRange='[26.2,26.3)'; pf='88' }
}
if ($Only) {
    $cells = $cells | Where-Object { $Only -contains $_ }
    $keys26 = @($matrix26.Keys) | Where-Object { $Only -contains $_ }
} else {
    $keys26 = @($matrix26.Keys)
}

foreach ($v in $cells) {
    $cell = Join-Path $repoRoot ('NeoForge\' + $v)
    if (-not (Test-Path $cell)) { Add-Content $prog "$v MISSING-CELL"; continue }
    Add-Content $prog "=== $v START $(Get-Date -Format HH:mm:ss) ==="
    & pwsh -NoProfile -File (Join-Path $PSScriptRoot 'cog-gen.ps1') -Cell ('NeoForge/' + $v) *>> $prog
    if ($LASTEXITCODE -ne 0) { Add-Content $prog "$v COG-FAIL"; continue }
    Push-Location $cell
    Get-ChildItem "$cell\build\libs\*.jar" -ErrorAction SilentlyContinue | Remove-Item -Force
    & "$cell\gradlew.bat" clean build --console=plain *> "$cell\_build.log"
    $code = $LASTEXITCODE
    Pop-Location
    $jar = Get-ChildItem "$cell\build\libs\*.jar" -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -notmatch 'sources|dev|slim' } | Select-Object -First 1
    $warn = (Select-String -Path "$cell\_build.log" -CaseSensitive -Pattern 'warning:|warning\b.*\[' -ErrorAction SilentlyContinue | Measure-Object).Count
    if ($code -eq 0 -and $jar) {
        Copy-Item $jar.FullName (Join-Path $dist $jar.Name) -Force
        Add-Content $prog "$v OK -> $($jar.Name) (warnings: $warn)"
    } else {
        Add-Content $prog "$v FAIL exit=$code (see NeoForge\$v\_build.log)"
    }
}

$cell26 = Join-Path $repoRoot 'NeoForge\26'
$modver = (Select-String -Path (Join-Path $cell26 'gradle.properties') -Pattern '^mod_version=(.+)$').Matches[0].Groups[1].Value
foreach ($v in $keys26) {
    $m = $matrix26[$v]
    Add-Content $prog "=== $v START $(Get-Date -Format HH:mm:ss) (mc=$($m.mc), neo=$($m.neo), pf=$($m.pf)) ==="
    $env:PACK_FORMAT = $m.pf
    Push-Location $cell26
    Get-ChildItem "$cell26\build\libs\*.jar" -ErrorAction SilentlyContinue | Remove-Item -Force
    & "$cell26\gradlew.bat" clean build "-Pminecraft_version=$($m.mc)" "-Pneo_version=$($m.neo)" `
        "-Pneoforge_range=$($m.neoRange)" "-Pmc_range=$($m.mcRange)" --console=plain *> "$cell26\_build_$v.log"
    $code = $LASTEXITCODE
    Pop-Location
    Remove-Item Env:PACK_FORMAT -ErrorAction SilentlyContinue
    $jar = Get-ChildItem "$cell26\build\libs" -Filter 'elytrahud3-*.jar' -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -notmatch 'sources|slim' } | Sort-Object LastWriteTime | Select-Object -Last 1
    $warn = (Select-String -Path "$cell26\_build_$v.log" -CaseSensitive -Pattern 'warning:|warning\b.*\[' -ErrorAction SilentlyContinue | Measure-Object).Count
    if ($code -eq 0 -and $jar) {
        $dest = Join-Path $dist ("elytrahud3-{0}+{1}-neoforge.jar" -f $modver, $v)
        Copy-Item $jar.FullName $dest -Force
        Add-Content $prog "$v OK -> $(Split-Path $dest -Leaf) (warnings: $warn)"
    } else {
        Add-Content $prog "$v FAIL exit=$code (see NeoForge\26\_build_$v.log)"
    }
}
Add-Content $prog "ALLDONE $(Get-Date -Format HH:mm:ss)"
