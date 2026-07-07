# ElytraHud3

**Need help or found a bug?** Report it at the [support forum](https://github.com/Kishku7/mod_support/issues).

ElytraHud3 is a **client-side** aviation-style flight HUD for elytra flight. While you glide it draws a
corner instrument cluster - airspeed, altitude, vertical speed, an artificial horizon, a compass, and
elytra durability - so you can fly your elytra on instruments instead of by guesswork.

This is my effort to keep one of my favorite mods alive - updated for the 26.x series and the newest Minecraft versions as they release.

Ships for **Fabric, NeoForge, and Forge** across Minecraft 1.20 through 26.x (Forge through 1.21.11; on 26.x it's Fabric and NeoForge). Client-side
only - safe to run without installing it on the server. Based on elytrahud-rework by inorganic / wancor1.
Licensed MIT.

**Download:** https://modrinth.com/mod/elytrahud3
**Source code:** [`minecraft-1.20-26.3` branch](https://github.com/Kishku7/elytrahud3/tree/minecraft-1.20-26.3)

## Why ElytraHud3

- **Fly on instruments.** A full six-gauge cluster - airspeed, altitude, vertical speed, artificial
  horizon, compass, and durability - appears the moment you start gliding and clears when you land.
- **Roll-aware horizon.** The artificial horizon tilts with your view and is compatible with Do a Barrel
  Roll, so aerobatics read correctly.
- **Your units, your layout.** Toggle imperial (default) or metric, and turn each gauge, its title, and
  its numeric readout on or off independently.
- **Lightweight and client-side.** Pure Java, about 33 KB, with no Kotlin / FLK / YACL runtime dependencies - no blocks, no items, no commands, no server install, just a HUD.
- **Everywhere you play.** Runs across Minecraft 1.20 through 26.x on Fabric, NeoForge, and Forge (Forge through 1.21.11).

## Usage

Install it on the **client** - it does nothing on a server and does not need to be installed there. Equip
and deploy an elytra and start gliding; the instrument cluster appears in the corner while you are
fall-flying and disappears when you land. ElytraHud3 adds no blocks, items, or commands - it is a HUD only.

Open the config screen through **Mod Menu** (Fabric) or the loader's mod-config entry (NeoForge / Forge) to
toggle individual gauges, their titles, and their numeric value boxes, and to switch between imperial and
metric units.

### Dependencies

- **Fabric API** - required on Fabric builds.
- **Mod Menu** and **Do a Barrel Roll** - optional (Do a Barrel Roll enables the roll-aware horizon).

## Credits and license

MIT. Based on elytrahud-rework by inorganic / wancor1 (MIT); ElytraHud3 modifications (c) Kishku7. Flight-HUD design inspired by neo-elytra-hud (CC0) and by Microsoft Flight Simulator's instrument styling; roll compatibility via Do a Barrel Roll's public API.
