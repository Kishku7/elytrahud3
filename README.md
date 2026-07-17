# ElytraHud3 - Build Guide (minecraft-1.20-26.3 branch)

This branch is the unified ElytraHud3 source tree. ONE source tree builds every supported Minecraft
version (1.20 through 26.3) on every applicable loader (Fabric, NeoForge, Forge). Per-version/loader API
drift is absorbed at build time by codegen (Cog) + reflection facades, so there are no per-version source
forks - only thin per-version build "cells" laid out `<Loader>/<mc-ver>/`. No Architectury, no Stonecutter.

For what ElytraHud3 is and how to use it, see the [landing page](https://github.com/Kishku7/elytrahud3).
Questions or bug reports: https://github.com/Kishku7/mod_support/issues

## What you need installed

ElytraHud3 builds on Windows using PowerShell build scripts and per-cell Gradle wrappers.

**Required:**

- **Windows + PowerShell 7 (`pwsh`)** - the build scripts are `.ps1` and call `gradlew.bat`.
- **Python 3 with Cog (`cogapp`) on `PATH`:**

      pip install cogapp

  Cog is the code generator that resolves cross-version API drift; the build scripts invoke it
  automatically, so it must be installed before you build. The generator brains are in `_codegen/`
  (`compat_core.py` + per-loader `compat_*.py`, pure Python, in-repo).
- **JDKs, installed and discoverable by Gradle's toolchain detection** (no foojay auto-download is
  configured, so install them yourself):
    - JDK 17 (Temurin/Adoptium) - the 1.20.x Forge cells
    - JDK 21 - the 1.21.x cells
    - JDK 25 - the 26.x cells

  Install all three to build the whole tree, or just the one(s) for the cells you care about.

**Provided for you (do NOT install manually):** each cell ships a Gradle wrapper (`gradlew.bat`), and
Gradle downloads the loader SDKs and dependencies on first build (Fabric Loom + Fabric API, NeoForge
ModDevGradle / NeoGradle 7, Forge ForgeGradle 6). An internet connection is required the first time each
cell is built.

## Layout

| Dir | Contents |
|-----|----------|
| `_codegen/cog_sources/common/` | MC-agnostic shared code (`ElytraHudConfig`) + shared assets (lang, textures, icon). One source of truth. |
| `_codegen/cog_sources/master/` | MC-coupled shared client code (`HudData`, `HudRenderer`, `HudRenderHelper`, `ElytraHudConfigScreen`, `McCompat`) - newest-era master; older eras are derived. |
| `_codegen/` | Cog brains (`compat_core.py` + per-loader `compat_*.py`) + `cog_sources/`. Encodes every version/loader drift axis. |
| `<Loader>/<mc-ver>/` | Thin per-version build cells (`Fabric/1.21.5`, `Forge/1.20.2`, `NeoForge/26`, ...). Each holds only its era's build wiring + manifest; its Java is cog-materialized into `gen/`. |
| `scripts/` | `build-{fabric,forge,neoforge}.ps1` walkers, `cog-gen.ps1`, `check-sync.ps1`. |
| `dist/` | Build output: `elytrahud3-<ver>+<mc>-<loader>.jar`. |

Edit ONLY `_codegen/`, `_codegen/cog_sources/common/`, `_codegen/cog_sources/master/`, and the 26-line twins - never a `gen/`
tree or a build output. `scripts/check-sync.ps1` guards the cog materialization against the twins.

## How to build

From the repo root, run the loader script for what you want. With no argument it builds every cell for
that loader into `dist/`; pass one or more versions to build a subset.

```
pwsh scripts/build-fabric.ps1              # all Fabric cells + the 26 matrix
pwsh scripts/build-neoforge.ps1            # all NeoForge cells + the 26 matrix
pwsh scripts/build-forge.ps1               # all Forge cells (EH3 builds through 1.21.11; no 26 -- no Forge on 26.x)
pwsh scripts/build-fabric.ps1 1.21.5 26.2  # a subset
```

Toolchains are pinned per cell (`org.gradle.java.home` + loader plugin): JDK 17 (1.20.x Forge), JDK 21
(1.21.x), JDK 25 (26.x). Fabric = fabric-loom; NeoForge = ModDevGradle (>= 20.5) / NeoGradle 7 (1.20.4);
Forge = ForgeGradle 6.

## How the code generation works

Cross-version API drift is resolved at build time by Cog, driven by `_codegen/`. The pre-26 build cells
srcDir a cog-materialized `gen/` tree rather than `_codegen/cog_sources/master` directly (which is why Cog must be
installed before building). Reflection facades handle drift only where the runtime is mojmap (26.x, all
loaders); everywhere the runtime is intermediary (pre-26 Fabric) or SRG (Forge/NeoForge 1.20.x) the same
logic is emitted as DIRECT compiled access via Cog - the loader remaps mojmap names at load, but reflection
strings never get remapped. `McCompat` is the worked example: a reflection twin on 26 cells, a direct-call
twin on every pre-26 cell.

## Supported versions

| Loader | MC coverage | Notes |
|--------|-------------|-------|
| **Fabric** | 1.20 - 26.3-snapshot-2 (continuous) | intermediary runtime spans rename boundaries; one jar per render era |
| **NeoForge** | 1.20.1 - 26.2 (+ 1.21.10, 1.21.11) | <= 1.20.1 served by the Forge 1.20.1 fork jar (tagged forge+neoforge); dedicated 1.21.10 (pre-`Identifier`-rename) + 1.21.11 cells |
| **Forge** | 1.20, 1.20.1, **1.20.2 - 1.20.4**, 1.20.6, 1.21.1, 1.21.5, 1.21.8, **1.21.10**, **1.21.11** | EH3 covers Forge through 1.21.11 (FG6 ceiling); no Forge on 26.x |

**Known loader gaps (not bugs):**
- Forge **1.21**, **1.21.3**, **1.21.4**, **1.21.6**, **1.21.7** - ORPHAN Forge builds (51/53/54/56/57):
  the HUD/GUI-overlay registration API is absent (present at Forge 50/52/55/58 and 60/61, but not these orphans). A HUD mod has no
  hook to attach there.
- Forge **1.21.2** - MinecraftForge never shipped a 1.21.2 build.
- Forge **1.21.10 / 1.21.11** - ARE built and shipped for ElytraHud3 (overlay API `AddGuiOverlayLayersEvent` / `ForgeLayeredDraw` present on forge 60/61, javap-verified). Forge **1.21.9** is beta-only (59.x) and skipped; the Fabric `+1.21.11` jar still covers MC 1.21.9.
- NeoForge **1.21.9** - the 21.9.16-beta transitional build is not client-test-gateable; the Fabric
  `+1.21.11` jar still covers MC 1.21.9/1.21.10. No NeoForge build for 26.3 yet.

Each jar declares an honest, closed MC + loader-floor range; 26.x jars ship the `min_format`/`max_format`
range-form `pack.mcmeta`. Client-gated per (loader, version) on the Raider client-test harness (HUD
rendered + screenshot-verified in-world).

## Credits / License

MIT. Based on elytrahud-rework by inorganic / wancor1 (MIT). ElytraHud3 maintained by Kishku7.
