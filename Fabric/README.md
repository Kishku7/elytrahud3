# ElytraHud3 - Fabric (Minecraft 26.2 (pre-release))

Client-only elytra flight HUD, **Fabric** loader builds for the Minecraft 26.2 (pre-release) line. Fabric only on this line (Quilt not supported - see below).
Standalone - no Architectury, no shared `common` module.

## Builds

| Version folder | Built against | JDK | Covers | Registration |
| --- | --- | --- | --- | --- |
| [`26.2/`](26.2) | 26.2-rc-2 (loader 0.19.3, fabric-api 0.152.0+26.2) | 25 | 26.2 line | `HudElementRegistry` |

Each row is its own folder with a README and a standalone Gradle build. The HUD render code
(`HudRenderer` / `HudRenderHelper`) is shared across builds; only per-version render-API adaptations
and the per-loader registration glue differ.

## Excluded / not built

- **Quilt** is not supported on the 26.x line - Quilt retired Quilted Fabric API (and Quilt Mappings) at 26.1, so the Fabric API compatibility path ElytraHud3 depends on is no longer provided on Quilt for 26.x. (Quilt remains supported on the 1.20.x and 1.21.x branches.)

## Build

```
cd <version>
./gradlew build      # Windows: .\gradlew.bat build
```

Output: `build/libs/elytrahud3-*.jar`.
