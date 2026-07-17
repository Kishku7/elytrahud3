# build-fabric.ps1 -- ALL Fabric builds: pre-26 cells (cog-gen -> gradle) AND the 26 line (matrix).
# Usage: pwsh -File scripts\build-fabric.ps1 [1.21.8 26.2 ...]   (no args = everything)
# Per-cell gradle.properties pin org.gradle.java.home; the 26 matrix cell pins JDK 25 toolchain.
param([Parameter(ValueFromRemainingArguments)][string[]]$Only)
$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path $PSScriptRoot -Parent
$dist = Join-Path $repoRoot 'dist'
New-Item -ItemType Directory -Force -Path $dist | Out-Null
$prog = Join-Path $repoRoot 'scripts\_build-fabric-progress.txt'
Remove-Item $prog -ErrorAction SilentlyContinue

# ---- pre-26 cells (cog-materialized) ----
$cells = @('1.20','1.20.4','1.20.6','1.21.1','1.21.2','1.21.5','1.21.8','1.21.11')
# ---- 26 line (matrix; cell Fabric/26 srcDirs shared_minecraft directly, no cog).
#      pf = per-26.X resource pack_format (authoritative: Memory/knowledge/pack-formats.md) ----
$matrix26 = [ordered]@{
    '26.1' = @{ mc='26.1.2';          api='0.152.1+26.1.2'; loader='0.18.6'; dep='>=26.1- <26.2'; pf='84' }
    '26.2' = @{ mc='26.2';            api='0.152.1+26.2';   loader='0.19.3'; dep='>=26.2- <26.3'; pf='88' }
  '26.3' = @{ mc='26.3-snapshot-4'; api='0.155.1+26.3';   loader='0.19.3'; dep='26.3-alpha.4'; pf='92' }
}
if ($Only) {
    $cells = $cells | Where-Object { $Only -contains $_ }
    $keys26 = @($matrix26.Keys) | Where-Object { $Only -contains $_ }
} else {
    $keys26 = @($matrix26.Keys)
}

foreach ($v in $cells) {
    $cell = Join-Path $repoRoot ('Fabric\' + $v)
    if (-not (Test-Path $cell)) { Add-Content $prog "$v MISSING-CELL"; continue }
    Add-Content $prog "=== $v START $(Get-Date -Format HH:mm:ss) ==="
    & pwsh -NoProfile -File (Join-Path $PSScriptRoot 'cog-gen.ps1') -Cell ('Fabric/' + $v) *>> $prog
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
        Add-Content $prog "$v FAIL exit=$code (see Fabric\$v\_build.log)"
    }
}

$cell26 = Join-Path $repoRoot 'Fabric\26'
$modver = (Select-String -Path (Join-Path $cell26 'gradle.properties') -Pattern '^mod_version=(.+)$').Matches[0].Groups[1].Value
foreach ($v in $keys26) {
    $m = $matrix26[$v]
    Add-Content $prog "=== $v START $(Get-Date -Format HH:mm:ss) (mc=$($m.mc), pf=$($m.pf)) ==="
    $env:PACK_FORMAT = $m.pf
    Push-Location $cell26
    Get-ChildItem "$cell26\build\libs\*.jar" -ErrorAction SilentlyContinue | Remove-Item -Force
    & "$cell26\gradlew.bat" clean build "-Pminecraft_version=$($m.mc)" "-Pfabric_version=$($m.api)" `
        "-Ploader_version=$($m.loader)" "-Pmc_dep=$($m.dep)" --console=plain *> "$cell26\_build_$v.log"
    $code = $LASTEXITCODE
    Pop-Location
    Remove-Item Env:PACK_FORMAT -ErrorAction SilentlyContinue
    $jar = Get-ChildItem "$cell26\build\libs" -Filter 'elytrahud3-*.jar' -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -notmatch 'sources' } | Sort-Object LastWriteTime | Select-Object -Last 1
    $warn = (Select-String -Path "$cell26\_build_$v.log" -CaseSensitive -Pattern 'warning:|warning\b.*\[' -ErrorAction SilentlyContinue | Measure-Object).Count
    if ($code -eq 0 -and $jar) {
        $dest = Join-Path $dist ("elytrahud3-{0}+{1}-fabric.jar" -f $modver, $v)
        Copy-Item $jar.FullName $dest -Force
        Add-Content $prog "$v OK -> $(Split-Path $dest -Leaf) (warnings: $warn)"
    } else {
        Add-Content $prog "$v FAIL exit=$code (see Fabric\26\_build_$v.log)"
    }
}
Add-Content $prog "ALLDONE $(Get-Date -Format HH:mm:ss)"
