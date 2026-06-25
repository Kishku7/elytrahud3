# ElytraHud3

A **client-side** aviation-style flight HUD for elytra flight.

While you are gliding, ElytraHud3 draws a corner instrument cluster: **airspeed, altitude, vertical speed, an artificial horizon, a compass, and elytra durability**. Units toggle between imperial (default) and metric, every gauge is individually toggleable with optional titles and numeric value boxes, and the artificial horizon is roll-aware (compatible with Do a Barrel Roll). It is client-side only - safe to run without installing it on the server.


## Branches

Source for each Minecraft line lives on its own branch; `main` (this branch) is just the overview.
Every branch is organized **loader-on-top**: each loader has its own folder (`Fabric/`, `Forge/`,
`NeoForge/`) with a sub-folder per Minecraft version. Every build is self-contained and standalone -
no Architectury, no shared `common` module.

| Branch | Minecraft | Loaders |
| --- | --- | --- |
| [`1.20.x`](https://github.com/Kishku7/elytrahud3/tree/1.20.x) | 1.20.1 - 1.20.6 | Fabric (+ Quilt), Forge, NeoForge |
| [`1.21.x`](https://github.com/Kishku7/elytrahud3/tree/1.21.x) | 1.21 - 1.21.11 | Fabric (+ Quilt), Forge, NeoForge |
| [`26`](https://github.com/Kishku7/elytrahud3/tree/26) | 26.1 -> 26.3-snapshot-1 | Fabric, NeoForge |

Open a branch and read its README for the loaders, versions, and any version exclusions in that line.

## Loader support

- **Fabric** (and **Quilt**) on the 1.20.x and 1.21.x lines; **Fabric only** on 26.x.
- **Forge** on 1.20.x and 1.21.x (ForgeGradle 6; not available on 26.x).
- **NeoForge** on every line.

Quilt is not offered on the 26.x line: Quilt retired Quilted Fabric API at 26.1, so the Fabric API
path ElytraHud3 depends on is no longer provided on Quilt for 26.x. Forge is not offered on 26.x:
ForgeGradle 6 cannot build unobfuscated Minecraft 26.x and there is no FG7.

## Using ElytraHud3

Install it on the **client** (it does nothing on a server and does not need to be installed there). Equip and deploy an elytra and start gliding - the instrument cluster appears in the corner while you are fall-flying, and disappears when you land.

ElytraHud3 adds **no blocks, no items, and no commands** - it is a HUD overlay only.

### Configuration

Open the config screen through **Mod Menu** (Fabric, if Mod Menu is installed) or the loader's mod config entry (NeoForge). The screen is a plain vanilla screen (no YACL) and lets you:

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
