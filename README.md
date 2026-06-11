# ElytraHud3

Aviation-style flight HUD for Minecraft elytras — **Fabric** and **NeoForge**, Minecraft 26.1.

A corner instrument cluster that appears while you're gliding: airspeed, altitude, vertical
speed, an artificial horizon, a compass, and elytra durability. Units toggle between imperial
(default) and metric. The artificial horizon stays correct while banking under
[Do a Barrel Roll](https://modrinth.com/mod/do-a-barrel-roll).

## Loaders

- **Fabric** (`fabric/`) — Minecraft 26.1. Requires Fabric API. ModMenu optional (for the config screen).
- **NeoForge** (`neoforge/`) — Minecraft 26.1.2. No extra dependencies; config screen via the mods list.

Pure Java on both loaders — no Kotlin / Fabric Language Kotlin / YACL runtime dependencies. About
90% of the code is shared; each loader carries only a thin entrypoint and registration layer.

## Building

Each loader is an independent Gradle project (JDK 25):

```
cd fabric    && ./gradlew build
cd neoforge  && ./gradlew build
```

Jars are written to each project's `build/libs/`.

## Configuration

Every element is individually toggleable, alongside an imperial/metric units switch. Open the
config screen via ModMenu (Fabric) or the NeoForge mods list, or edit `config/elytrahud3.json`
directly.

## Do a Barrel Roll compatibility

The HUD reads camera roll from Do a Barrel Roll's public API (`RollCamera`) by reflection — a soft,
optional dependency. No DABR code is bundled; without it installed the HUD simply renders level.

## Credits & license

- Derived from [elytrahud-rework](https://github.com/wancor1/elytrahud-rework) by inorganic (MIT).
- Flight-instrument HUD design inspired by [neo-elytra-hud](https://modrinth.com/mod/neo-elytra-hud) (CC0).
- Roll compatibility via [Do a Barrel Roll](https://codeberg.org/enjarai/do-a-barrel-roll) by enjarai
  (GPL-3.0) — used only through its public API; no GPL code is included.

Licensed under the MIT License. See [LICENSE](LICENSE).
