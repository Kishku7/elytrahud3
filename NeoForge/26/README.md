# ElytraHud3 -- NeoForge (26.x)

NeoForge platform glue for the unified 26.x line. Shared code is pulled from `../shared_common` and
`../shared_minecraft` via `srcDir`; this folder holds only NeoForge-specific files:
`Common` (holder), `ConfigManager` (FMLPaths config dir), `ElytraHud3NeoForge`,
`ElytraHud3NeoForgeClient`, and the templated `neoforge.mods.toml`.

```
.\gradlew.bat build -Pminecraft_version=26.2 -Pneo_version=26.2.0.1-beta -Pneoforge_range="[26.2.0-alpha,)" -Pmc_range="[26.2,26.3)"
```

Supported MC: 26.1.2, 26.2. (NeoForge has no 26.3 build yet.) Toolchain: ModDevGradle 2.0.140, JDK 25.
