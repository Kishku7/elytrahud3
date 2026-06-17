# ElytraHud3 - NeoForge (Minecraft 26.2 (pre-release))

Client-only elytra flight HUD, **NeoForge** loader builds for the Minecraft 26.2 (pre-release) line.
Standalone - no Architectury, no shared `common` module.

## Builds

| Version folder | Built against | JDK | Covers | Registration |
| --- | --- | --- | --- | --- |
| [`26.2/`](26.2) | a local NeoForge 26.2 alpha (no public NeoForge 26.2 yet) | 25 | 26.2 line | `RegisterGuiLayersEvent` |

Each row is its own folder with a README and a standalone Gradle build. The HUD render code
(`HudRenderer` / `HudRenderHelper`) is shared across builds; only per-version render-API adaptations
and the per-loader registration glue differ.

## Build

```
cd <version>
./gradlew build      # Windows: .\gradlew.bat build
```

Output: `build/libs/elytrahud3-*.jar`.
