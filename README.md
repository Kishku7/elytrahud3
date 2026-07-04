# ElytraHud3

A **client-side** aviation-style flight HUD for elytra flight.

While you are gliding, ElytraHud3 draws a corner instrument cluster: **airspeed, altitude, vertical speed, an artificial horizon, a compass, and elytra durability**. Units toggle between imperial (default) and metric, every gauge is individually toggleable with optional titles and numeric value boxes, and the artificial horizon is roll-aware (compatible with Do a Barrel Roll). It is client-side only - safe to run without installing it on the server.


## Source

All source lives on one branch: [`minecraft-1.20-26.3`](https://github.com/Kishku7/elytrahud3/tree/minecraft-1.20-26.3)
(`main` is just this overview). It is a single unified source tree that builds every supported
Minecraft version (1.20 through 26.3) on every applicable loader - per-version/loader API drift is
absorbed at build time by codegen (Cog) + reflection facades, with thin per-version build cells laid
out `<Loader>/<mc-ver>/`. No Architectury.

## Loader / version support

| Loader | Minecraft | Notes |
| --- | --- | --- |
| **Fabric** | 1.20 - 26.3 | continuous (one build per render era) |
| **NeoForge** | 1.20.1 - 26.2 | 1.20/1.20.1 served by the Forge fork jar |
| **Forge** | 1.20, 1.20.1, 1.20.2-1.20.4, 1.20.6, 1.21.1, 1.21.5, 1.21.8 | ForgeGradle 6, ceiling 1.21.8; no Forge on 26.x |

**Forge exclusions (Forge's own limitation, not ElytraHud3's):** Forge removed its HUD/GUI-overlay
registration API on several transitional 1.21.x builds - **1.21 (Forge 51), 1.21.3 (53), 1.21.4 (54),
1.21.6 (56), 1.21.7 (57)** - so a HUD mod has no way to attach its overlay there. It is present only on
Forge 50/52/55/58 (the versions above). Forge also never shipped a 1.21.2 build and is discontinued
after 1.21.8. Fabric and NeoForge cover all of these Minecraft versions normally.

## Using ElytraHud3

Install it on the **client** (it does nothing on a server and does not need to be installed there). Equip and deploy an elytra and start gliding - the instrument cluster appears in the corner while you are fall-flying, and disappears when you land.

ElytraHud3 adds **no blocks, no items, and no commands** - it is a HUD overlay only.

### Configuration

Open the config screen through **Mod Menu** (Fabric, if Mod Menu is installed) or the loader's mod config entry (NeoForge / Forge). The screen is a plain vanilla screen (no YACL) and lets you:

- Toggle each gauge (airspeed, altitude, vertical speed, artificial horizon, compass, durability).
- Toggle gauge titles and numeric value boxes.
- Switch units between imperial and metric.

### Dependencies

- **Fabric API** - required on Fabric builds.
- **Mod Menu** and **Do a Barrel Roll** - optional (Do a Barrel Roll enables the roll-aware horizon).

## Downloads

- Modrinth: https://modrinth.com/mod/elytrahud3
- Releases: https://github.com/Kishku7/elytrahud3/releases

By Kishku7, MIT licensed. Based on elytrahud-rework by inorganic / wancor1 (MIT).
