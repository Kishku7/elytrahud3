# ElytraHud3 - Fabric 26.2 (Minecraft 26.2 line)

Client-only elytra flight HUD - **Fabric** build for Minecraft **26.2 line**.
Standalone build (no Architectury, no shared `common` module).

- **Covers:** 26.2 line
- **Built against:** 26.2-rc-2 (loader 0.19.3, fabric-api 0.152.0+26.2)
- **Toolchain:** JDK 25, fabric-loom, mojmap mappings.
- **Rendering:** 2D `Matrix3x2fStack` pose.
- **Registration:** `HudElementRegistry`.

## Build

```
./gradlew build      # Windows: .\gradlew.bat build
```

Output: `build/libs/elytrahud3-*.jar`.

## Dependencies

- **Fabric API** - required.
- **Mod Menu**, **Do a Barrel Roll** - optional.
