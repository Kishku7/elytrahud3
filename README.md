# ElytraHud3 -- unified line (MC 1.20 - 26.3)

Aviation-style flight HUD for elytras: a corner instrument cluster (airspeed, altitude, vertical
speed, artificial horizon, compass, durability) shown while gliding. Imperial/metric toggle,
*Do a Barrel Roll* roll-aware horizon. Pure Java, no Kotlin/YACL. License MIT.

This is the **unified `minecraft-1.20-26.3` branch**: ONE source tree builds every supported MC
version (1.20 through 26.3) on every applicable loader. Per-version/loader API drift is absorbed at
build time by codegen (Cog) + reflection facades, so there are no per-version source forks -- only
thin per-version build "cells".

## Layout

| Dir | Contents |
|-----|----------|
| `shared_common/` | MC-agnostic shared code (`ElytraHudConfig`) + shared assets (lang, textures, icon). One source of truth. |
| `shared_minecraft/` | MC-coupled shared client code (`HudData`, `HudRenderer`, `HudRenderHelper`, `ElytraHudConfigScreen`, `McCompat`) -- newest-era master; older eras are derived. |
| `_codegen/` | Cog brains (`compat_core.py` + per-loader `compat_*.py`) + `cog_sources/`. Encodes every version/loader drift axis. |
| `<Loader>/<mc-ver>/` | Thin per-version build cells (`Fabric/1.21.5`, `Forge/1.20.2`, `NeoForge/26`, ...). Each holds only its era's build wiring + manifest; its Java is cog-materialized into `gen/`. |
| `scripts/` | `build-{fabric,forge,neoforge}.ps1` walkers, `cog-gen.ps1`, `check-sync.ps1`. |
| `dist/` | Build output: `elytrahud3-<ver>+<mc>-<loader>.jar`. |

Edit ONLY `_codegen/`, `shared_common/`, `shared_minecraft/`, and the 26-line twins -- never a `gen/`
tree or a build output. `scripts/check-sync.ps1` guards the cog materialization against the twins.

## Build

```
pwsh scripts/build-fabric.ps1              # all Fabric cells + the 26 matrix
pwsh scripts/build-neoforge.ps1            # all NeoForge cells + the 26 matrix
pwsh scripts/build-forge.ps1               # all Forge cells (no 26 -- FG6 ceiling 1.21.8)
pwsh scripts/build-fabric.ps1 1.21.5 26.2  # a subset
```

Toolchains are pinned per cell (`org.gradle.java.home` + loader plugin): JDK 17 (1.20.x Forge),
JDK 21 (1.21.x), JDK 25 (26.x). Fabric = fabric-loom; NeoForge = ModDevGradle (>= 20.5) / NeoGradle 7
(1.20.4); Forge = ForgeGradle 6. Never Architectury, never Stonecutter.

## Supported versions

| Loader | MC coverage | Notes |
|--------|-------------|-------|
| **Fabric** | 1.20 - 26.3-snapshot-2 (continuous) | intermediary runtime spans rename boundaries; one jar per render era |
| **NeoForge** | 1.20.1 - 26.2 (+ 1.21.10) | <= 1.20.1 served by the Forge 1.20.1 fork jar (tagged forge+neoforge); dedicated 1.21.10 (pre-`Identifier`-rename) cell |
| **Forge** | 1.20, 1.20.1, **1.20.2 - 1.20.4**, 1.20.6, 1.21.1, 1.21.5, 1.21.8 | FG6 ceiling is 1.21.8; no Forge on 26.x |

**Known loader gaps (not bugs):**
- Forge **1.21**, **1.21.3**, **1.21.4**, **1.21.6**, **1.21.7** -- ORPHAN Forge builds (51/53/54/56/57):
  the HUD/GUI-overlay registration API is absent (present only at Forge 50/52/55/58). A HUD mod has no
  hook to attach there.
- Forge **1.21.2** -- MinecraftForge never shipped a 1.21.2 build. Forge is dead after 1.21.8.
- NeoForge **1.21.9** -- the 21.9.16-beta transitional build is not client-test-gateable; the Fabric
  `+1.21.11` jar still covers MC 1.21.9/1.21.10. No NeoForge build for 26.3 yet.

Each jar declares an honest, closed MC + loader-floor range; 26.x jars ship the `min_format`/`max_format`
range-form `pack.mcmeta`. Client-gated per (loader, version) on the Raider client-test harness (HUD
rendered + screenshot-verified in-world).
