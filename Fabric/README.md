# ElytraHud3 -- Fabric (26.x)

Fabric platform glue for the unified 26.x line. Shared code is pulled from `../shared_common` and
`../shared_minecraft` via `srcDir`; this folder holds only Fabric-specific files:
`Common` (ClientModInitializer), `ConfigManager` (FabricLoader config dir), `ElytraHudModMenu`,
and the templated `fabric.mod.json`.

Build a single target (run from the repo root via the matrix script, or directly):

```
.\gradlew.bat build -Pminecraft_version=26.2 -Pfabric_version=0.152.1+26.2 -Ploader_version=0.19.3 -Pmc_dep=">=26.2- <26.3"
```

Supported MC: 26.1.2, 26.2, 26.3-snapshot-1. Toolchain: fabric-loom 1.15.5, JDK 25.
