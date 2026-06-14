# ElytraHud3

## Branches

- [26.2](https://github.com/Kishku7/elytrahud3/tree/26.2)
- [26.1.2](https://github.com/Kishku7/elytrahud3/tree/26.1.2)

[![Discord](https://img.shields.io/badge/Discord-Join-5865F2?logo=discord&logoColor=white)](https://discord.gg/2ZxzbCzAHe)

An aviation-style flight HUD for elytra flight.

While you're gliding, ElytraHud3 shows a corner instrument cluster: airspeed, altitude,
vertical speed, an artificial horizon, a compass, and elytra durability. Units toggle
between imperial and metric, every gauge is individually toggleable, and the artificial
horizon is roll-aware (compatible with Do a Barrel Roll). Client-side only.

## Supported platforms

Source for each Minecraft version lives on its own branch, named for the version.
`main` (this branch) is just the overview.

| Branch    | Minecraft       | Fabric | NeoForge |
| ---       | ---             | :---:  | :---:    |
| `26.1.2`  | 26.1 - 26.1.2   | Yes    | Yes      |

Dependencies: Fabric API (Fabric builds). ModMenu and Do a Barrel Roll are optional.

## Building from source

Check out the branch for your Minecraft version, then build each loader:

    cd fabric   && ./gradlew build
    cd neoforge && ./gradlew build

## Downloads

- Modrinth: https://modrinth.com/mod/elytrahud3
- Releases: https://github.com/Kishku7/elytrahud3/releases

By Kishku7, MIT licensed. Based on elytrahud-rework by inorganic / wancor1 (MIT).