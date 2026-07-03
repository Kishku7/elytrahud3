# check-sync.ps1 -- drift tripwire between the cog sources and their PLAIN 26 twins.
# The 26 cells never run cog, so shared_minecraft + Fabric/26 + NeoForge/26 keep plain masters.
# This materializes each cog stub at 26.1 and compares CODE (comments/blank/package lines ignored)
# against the plain twin; version-invariant plain cog_sources files are compared directly.
# Exit 1 on drift. Run before every commit.
$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path $PSScriptRoot -Parent
$cg = Join-Path $repoRoot '_codegen'
$tmp = Join-Path $env:TEMP ('eh3-checksync-' + [guid]::NewGuid().ToString('N').Substring(0,8))
New-Item -ItemType Directory -Force -Path $tmp | Out-Null

function Normalize($path) {
    $out = New-Object System.Collections.Generic.List[string]
    $inBlock = $false
    foreach ($ln in (Get-Content $path)) {
        $t = $ln.Trim()
        if ($inBlock) { if ($t -match '\*/') { $inBlock = $false }; continue }
        if ($t -match '^/\*' ) { if ($t -notmatch '\*/') { $inBlock = $true }; continue }
        if ($t -eq '' -or $t.StartsWith('//') -or $t.StartsWith('*') -or $t.StartsWith('package ')) { continue }
        $out.Add($t)
    }
    return $out
}

$sm = "$repoRoot\shared_minecraft\src\main\java\dev\kishku\elytrahud3"
$f26 = "$repoRoot\Fabric\26\src\main\java\dev\kishku\elytrahud3"
$n26 = "$repoRoot\NeoForge\26\src\main\java\dev\kishku\elytrahud3"

$pairs = @(
    @{ src="$cg\cog_sources\shared\HudRenderer.java";                loader='fabric';   cogit=$true;  plain="$sm\HudRenderer.java" },
    @{ src="$cg\cog_sources\shared\HudRenderHelper.java";            loader='fabric';   cogit=$true;  plain="$sm\HudRenderHelper.java" },
    @{ src="$cg\cog_sources\shared\McCompat.java";                   loader='fabric';   cogit=$true;  plain="$sm\McCompat.java" },
    @{ src="$cg\cog_sources\fabric\Common.java";                     loader='fabric';   cogit=$true;  plain="$f26\Common.java" },
    @{ src="$cg\cog_sources\fabric\ConfigManager.java";              loader='fabric';   cogit=$false; plain="$f26\ConfigManager.java" },
    @{ src="$cg\cog_sources\fabric\ElytraHudModMenu.java";           loader='fabric';   cogit=$false; plain="$f26\ElytraHudModMenu.java" },
    @{ src="$cg\cog_sources\neoforge\ElytraHud3NeoForge.java";       loader='neoforge'; cogit=$true;  plain="$n26\ElytraHud3NeoForge.java" },
    @{ src="$cg\cog_sources\neoforge\ElytraHud3NeoForgeClient.java"; loader='neoforge'; cogit=$true;  plain="$n26\ElytraHud3NeoForgeClient.java" },
    @{ src="$cg\cog_sources\neoforge\ConfigManager.java";            loader='neoforge'; cogit=$false; plain="$n26\ConfigManager.java" },
    @{ src="$cg\cog_sources\neoforge\Common.java";                   loader='neoforge'; cogit=$false; plain="$n26\Common.java" }
)

$env:PYTHONDONTWRITEBYTECODE = '1'
$fail = 0
foreach ($p in $pairs) {
    $name = (Split-Path (Split-Path $p.src -Parent) -Leaf) + '/' + (Split-Path $p.src -Leaf)
    if (-not (Test-Path $p.plain)) { Write-Host "MISSING plain twin: $name"; $fail++; continue }
    $work = Join-Path $tmp ((Split-Path $p.src -Leaf))
    Copy-Item $p.src $work -Force
    if ($p.cogit) {
        & cog -r -D ("loader=" + $p.loader) -D ver=26.1 -D codegen=$cg $work | Out-Null
        if ($LASTEXITCODE -ne 0) { Write-Host "COG FAIL: $name"; $fail++; continue }
    }
    $a = Normalize $work
    $b = Normalize $p.plain
    $diff = Compare-Object $a $b
    if ($diff) {
        Write-Host "DRIFT: $name ($($diff.Count) differing code lines)"
        $diff | Select-Object -First 6 | ForEach-Object { Write-Host ("  {0} {1}" -f $_.SideIndicator, $_.InputObject) }
        $fail++
    } else {
        Write-Host "OK: $name"
    }
}
Remove-Item $tmp -Recurse -Force
if ($fail -gt 0) { Write-Host "check-sync: $fail file(s) drifted"; exit 1 }
Write-Host 'check-sync: all twins in sync'
