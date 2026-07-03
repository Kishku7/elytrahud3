# cog-gen.ps1 -- materialize a pre-26 build cell's gen/ tree from the one shared source.
# Usage: pwsh -File scripts\cog-gen.ps1 -Cell Fabric/1.21.8
# The 26 cells do NOT use cog-gen (they srcDir shared_minecraft directly; compat cannot affect 26).
# gen/ is disposable build output (gitignored). Edit ONLY _codegen + shared_minecraft (+ 26 twins).
# EH3 has NO mixins and NO generated per-version resources: gen/ = java + pack.mcmeta only
# (assets/lang/icon are MC-agnostic and srcDir'd from shared_common by every cell).
param(
    [Parameter(Mandatory)][string]$Cell            # <Loader>/<mcver>, e.g. Fabric/1.21.8
)
$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path $PSScriptRoot -Parent
$parts  = $Cell -split '[/\\]'
$LoaderDir = $parts[0]; $McVer = $parts[1]
$Loader = $LoaderDir.ToLower()                     # fabric | forge | neoforge
$cg  = Join-Path $repoRoot '_codegen'
$cs  = Join-Path $cg 'cog_sources'
$cell = Join-Path $repoRoot ($LoaderDir + '\' + $McVer)
if (-not (Test-Path $cell)) { throw "cell not found: $cell" }
$gen  = Join-Path $cell 'gen'
$pkg  = 'dev\kishku\elytrahud3'
$genJ = Join-Path $gen ('src\main\java\' + $pkg)
$genR = Join-Path $gen 'src\main\resources'

# ---- 1. wipe gen/, copy shared_minecraft java verbatim (HudData + ElytraHudConfigScreen ride
#         along unchanged; the drift files are overwritten by the cog stubs in step 2) ----
Remove-Item $gen -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path $genJ, $genR | Out-Null
Copy-Item (Join-Path $repoRoot ('shared_minecraft\src\main\java\' + $pkg + '\*')) $genJ -Recurse -Force

# ---- 2. overwrite drift files with the cog-instrumented shared stubs ----
Copy-Item (Join-Path $cs 'shared\*') $genJ -Recurse -Force

# ---- 3. loader glue (cog stubs + version-invariant plain files) ----
Copy-Item (Join-Path $cs ($Loader + '\*')) $genJ -Recurse -Force

# ---- 4. pack.mcmeta (per-version resource pack_format; authoritative: Memory/knowledge/pack-formats.md.
#         The 1.1.x jars shipped pf=8 everywhere -- that bug dies here.) ----
$packFormats = @{
    '1.20'=15; '1.20.1'=15; '1.20.2'=18; '1.20.3'=22; '1.20.4'=22; '1.20.5'=32; '1.20.6'=32;
    '1.21'=34; '1.21.1'=34; '1.21.2'=42; '1.21.3'=42; '1.21.4'=46; '1.21.5'=55;
    '1.21.6'=63; '1.21.7'=64; '1.21.8'=64; '1.21.9'=69; '1.21.10'=69; '1.21.11'=75
}
$pf = $packFormats[$McVer]
if (-not $pf) { throw "no pack_format for $McVer -- extend the table (knowledge/pack-formats.md)" }
('{"pack":{"description":"elytrahud3 resources","pack_format":' + $pf + '}}') |
    Set-Content (Join-Path $genR 'pack.mcmeta') -Encoding ascii

# ---- 5. run cog on every marker file in gen ----
$env:PYTHONDONTWRITEBYTECODE = '1'
Get-ChildItem (Join-Path $gen 'src\main\java') -Recurse -File -Filter *.java |
    Where-Object { (Get-Content $_.FullName -Raw) -match '\[\[\[cog' } | ForEach-Object {
        & cog -r -D loader=$Loader -D ver=$McVer -D codegen=$cg $_.FullName | Out-Null
        if ($LASTEXITCODE -ne 0) { throw ("cog failed: " + $_.FullName) }
    }
Write-Host ("cog-gen OK: {0} (pf={1})" -f $Cell, $pf)
