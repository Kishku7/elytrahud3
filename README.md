# ElytraHud3 - branch `26.2`

Client-only aviation-style elytra flight HUD. This branch holds the Minecraft **26.2 (pre-release)** source.
Pure Java, no mixins, Do a Barrel Roll compatible. Standalone per loader - no Architectury, no shared
`common` module. Mojang (mojmap) mappings throughout.

> **Pre-release line.** Published to Modrinth as **beta** only; no GitHub release is cut until 26.2 is stable. The NeoForge build targets a local NeoForge 26.2 alpha (no public NeoForge 26.2 exists yet).

## Platforms

- [`Fabric/`](Fabric) - 1 build(s); see its README for versions and exclusions.
- [`NeoForge/`](NeoForge) - 1 build(s); see its README for versions and exclusions.

## Not supported on this line

- **Forge** is not built for the 26.x line - ForgeGradle 6 cannot build unobfuscated Minecraft 26.x and there is no FG7.
- **Quilt** is not supported on the 26.x line - Quilt retired Quilted Fabric API (and Quilt Mappings) at 26.1, so the Fabric API compatibility path ElytraHud3 depends on is no longer provided on Quilt for 26.x. (Quilt remains supported on the 1.20.x and 1.21.x branches.)

## Build

Each loader/version folder is its own standalone Gradle project:

```
cd <Loader>/<version>
./gradlew build      # Windows: .\gradlew.bat build
```

Output jar: `build/libs/elytrahud3-*.jar`. Requires JDK 25 (Minecraft 26.x toolchain).

## Links

- Other branches: [`1.20.x`](https://github.com/Kishku7/elytrahud3/tree/1.20.x), [`1.21.x`](https://github.com/Kishku7/elytrahud3/tree/1.21.x), [`26.1`](https://github.com/Kishku7/elytrahud3/tree/26.1)
- Overview: [`main`](https://github.com/Kishku7/elytrahud3/tree/main)
- Modrinth: https://modrinth.com/mod/elytrahud3

MIT licensed. Based on elytrahud-rework by inorganic / wancor1 (MIT).
