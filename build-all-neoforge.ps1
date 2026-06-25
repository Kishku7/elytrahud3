# build-all-neoforge.ps1 -- build the unified NeoForge source for every supported 26.x target.
# Usage: pwsh build-all-neoforge.ps1 [26.1 26.2]   (no args = all). MC 26.3 has no NeoForge yet.
param([string[]]$Versions)
$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent $MyInvocation.MyCommand.Path
$nf   = Join-Path $repo "NeoForge"
$dist = Join-Path $repo "dist"
New-Item -ItemType Directory -Force -Path $dist | Out-Null

$matrix = [ordered]@{
  "26.1" = @{ mc = "26.1.2"; neo = "26.1.2.30-beta"; neoRange = "[26.1.2.0-beta,)"; mcRange = "[26.1,26.2)" }
  "26.2" = @{ mc = "26.2";   neo = "26.2.0.1-beta";  neoRange = "[26.2.0-alpha,)"; mcRange = "[26.2,26.3)" }
}
if (-not $Versions -or $Versions.Count -eq 0) { $Versions = @($matrix.Keys) }
$modver = (Select-String -Path (Join-Path $nf "gradle.properties") -Pattern '^mod_version=(.+)$').Matches[0].Groups[1].Value

foreach ($v in $Versions) {
  $m = $matrix[$v]; if (-not $m) { throw "Unknown NeoForge version '$v'" }
  Write-Host "=== NeoForge build for $v  (neoforge=$($m.neo)) ==="
  Push-Location $nf
  & ".\gradlew.bat" clean build "-Pminecraft_version=$($m.mc)" "-Pneo_version=$($m.neo)" "-Pneoforge_range=$($m.neoRange)" "-Pmc_range=$($m.mcRange)" --no-daemon
  $rc = $LASTEXITCODE
  Pop-Location
  if ($rc -ne 0) { throw "NeoForge build FAILED for $v (rc=$rc)" }
  $jar = Get-ChildItem (Join-Path $nf "build\libs") -Filter "elytrahud3-*.jar" |
         Where-Object { $_.Name -notmatch 'sources|slim' } | Sort-Object LastWriteTime | Select-Object -Last 1
  $dest = Join-Path $dist ("elytrahud3-{0}+{1}-neoforge.jar" -f $modver, $v)
  Copy-Item $jar.FullName $dest -Force
  Write-Host "  -> $dest"
}
Write-Host "All NeoForge builds complete. Jars in $dist"
