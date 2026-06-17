# ElytraHud3 - NeoForge 26.2 (Minecraft 26.2 line)

Client-only elytra flight HUD - **NeoForge** build for Minecraft **26.2 line**.
Standalone build (no Architectury, no shared `common` module).

- **Covers:** 26.2 line
- **Built against:** a local NeoForge 26.2 alpha (no public NeoForge 26.2 yet)
- **Toolchain:** JDK 25, ModDevGradle (MDG), mojmap mappings.
- **Rendering:** 2D `Matrix3x2fStack` pose.
- **Registration:** `RegisterGuiLayersEvent`.

## Build

```
./gradlew build      # Windows: .\gradlew.bat build
```

Output: `build/libs/elytrahud3-*.jar`.
