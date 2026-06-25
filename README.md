# ElytraHud3 -- MC 26.x (unified line)

Aviation-style flight HUD for elytras: a corner instrument cluster (airspeed, altitude, vertical
speed, artificial horizon, compass, durability) shown while gliding. Imperial/metric toggle,
*Do a Barrel Roll* roll-aware horizon. Pure Java, no Kotlin/YACL. License MIT.

This is the **unified 26.x branch**. One source tree builds every supported MC 26.x version on both
loaders; per-version differences are absorbed at runtime by `McCompat` (reflective shim), so there are
no per-version source forks.

## Layout

| Dir | Contents |
|-----|----------|
| `shared_common/` | MC-agnostic shared code (`ElytraHudConfig`) + shared assets (lang, textures, icon). Single source of truth. |
| `shared_minecraft/` | MC-coupled shared client code (`HudData`, `HudRenderer`, `HudRenderHelper`, `ElytraHudConfigScreen`, `McCompat`). Identical across loaders + versions. |
| `Fabric/` | Fabric platform glue only (`Common` entrypoint, `ConfigManager`, `ElytraHudModMenu`, `fabric.mod.json`). |
| `NeoForge/` | NeoForge platform glue only (`Common`, `ConfigManager`, `ElytraHud3NeoForge`, `ElytraHud3NeoForgeClient`, `neoforge.mods.toml`). |

Each loader build pulls the two `shared_*` trees in via `srcDir`, so the shared code lives in exactly
one place. Edit the canonical copy under `shared_common/` or `shared_minecraft/` -- never a build output.

## Build

Per-platform scripts loop the supported-version matrix and stage jars to `dist/`:

```
pwsh build-all-fabric.ps1            # 26.1.2, 26.2, 26.3-snapshot-1
pwsh build-all-neoforge.ps1          # 26.1.2, 26.2   (NeoForge has no 26.3 yet)
pwsh build-all-fabric.ps1 26.2       # a single target
```

Toolchain: JDK 25. Fabric = fabric-loom 1.15.5; NeoForge = ModDevGradle 2.0.140.

## Supported versions

| Loader | MC versions |
|--------|-------------|
| Fabric | 26.1.2, 26.2, 26.3-snapshot-1 (alpha) |
| NeoForge | 26.1.2, 26.2 |
