# ElytraHud3

A **client-side** aviation-style flight HUD for elytra flight.

While you're gliding, ElytraHud3 shows a corner instrument cluster: airspeed, altitude,
vertical speed, an artificial horizon, a compass, and elytra durability. Units toggle
between imperial and metric, every gauge is individually toggleable, and the artificial
horizon is roll-aware (compatible with Do a Barrel Roll). Client-side only - safe to run
without installing it on the server.

## Branches

Source for each Minecraft line lives on its own branch. `main` (this branch) is just the overview.
Each branch is organized loader-on-top: `Fabric/<version>/` and `NeoForge/<version>/`, every build
self-contained and standalone (no Architectury, no shared `common` module).

| Branch                                                            | Minecraft       | Status      |
| ---                                                               | ---             | ---         |
| [`1.20.x`](https://github.com/Kishku7/elytrahud3/tree/1.20.x)     | 1.20.x          | Planned     |
| [`1.21.x`](https://github.com/Kishku7/elytrahud3/tree/1.21.x)     | 1.21.x          | Planned     |
| [`26.1`](https://github.com/Kishku7/elytrahud3/tree/26.1)         | 26.1 - 26.1.2   | Available   |
| [`26.2`](https://github.com/Kishku7/elytrahud3/tree/26.2)         | 26.2 (pre)      | Pre-release |

## Support

- **Loaders:** Fabric (and Quilt) + NeoForge, all client-side.
- **Dependencies:** Fabric API (Fabric builds). ModMenu and Do a Barrel Roll are optional.

[![Discord](https://img.shields.io/badge/Discord-Join-5865F2?logo=discord&logoColor=white)](https://discord.gg/2ZxzbCzAHe)

## Downloads

- Modrinth: https://modrinth.com/mod/elytrahud3
- Releases: https://github.com/Kishku7/elytrahud3/releases
- Discord: https://discord.gg/2ZxzbCzAHe

By Kishku7, MIT licensed. Based on elytrahud-rework by inorganic / wancor1 (MIT).
