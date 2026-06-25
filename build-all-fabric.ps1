# build-all-fabric.ps1 -- build the unified Fabric source for every 26.x target.
# Usage: pwsh build-all-fabric.ps1 [26.1 26.2 26.3]   (no args = all)
param([string[]]$Versions)
$ErrorActionPreference = "Stop"
$repo   = Split-Path -Parent $MyInvocation.MyCommand.Path
$fabric = Join-Path $repo "Fabric"
$dist   = Join-Path $repo "dist"
New-Item -ItemType Directory -Force -Path $dist | Out-Null

$matrix = [ordered]@{
  "26.1" = @{ mc = "26.1.2";          api = "0.152.1+26.1.2"; loader = "0.18.6"; dep = ">=26.1 <26.2" }
  "26.2" = @{ mc = "26.2";            api = "0.152.1+26.2";   loader = "0.19.3"; dep = ">=26.2- <26.3" }
  "26.3" = @{ mc = "26.3-snapshot-1"; api = "0.153.1+26.3";   loader = "0.19.3"; dep = ">=26.3- <26.4" }
}
if (-not $Versions -or $Versions.Count -eq 0) { $Versions = @($matrix.Keys) }
$modver = (Select-String -Path (Join-Path $fabric "gradle.properties") -Pattern '^mod_version=(.+)$').Matches[0].Groups[1].Value

foreach ($v in $Versions) {
  $m = $matrix[$v]; if (-not $m) { throw "Unknown version '$v'" }
  Write-Host "=== Fabric build for $v  (mc=$($m.mc)  api=$($m.api)) ==="
  Push-Location $fabric
  & ".\gradlew.bat" clean build "-Pminecraft_version=$($m.mc)" "-Pfabric_version=$($m.api)" "-Ploader_version=$($m.loader)" "-Pmc_dep=$($m.dep)" --no-daemon
  $rc = $LASTEXITCODE
  Pop-Location
  if ($rc -ne 0) { throw "Fabric build FAILED for $v (rc=$rc)" }
  $jar = Get-ChildItem (Join-Path $fabric "build\libs") -Filter "elytrahud3-*.jar" |
         Where-Object { $_.Name -notmatch 'sources' } | Sort-Object LastWriteTime | Select-Object -Last 1
  $dest = Join-Path $dist ("elytrahud3-{0}+{1}-fabric.jar" -f $modver, $v)
  Copy-Item $jar.FullName $dest -Force
  Write-Host "  -> $dest"
}
Write-Host "All Fabric builds complete. Jars in $dist"
