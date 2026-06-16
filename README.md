# ElytraHud3 - branch `26.2`

Client-only elytra-flight HUD mod. This branch holds the **Minecraft 26.2 line** (pre-release).

Builds are standalone per loader - no Architectury, no shared `common` module.

## Layout

| Path             | Loader   | Minecraft   |
| ---              | ---      | ---         |
| `Fabric/26.2/`   | Fabric   | 26.2 (pre)  |
| `NeoForge/26.2/` | NeoForge | 26.2 (pre)  |

See each folder's README for build details.

## Build

```
cd Fabric/26.2   && ./gradlew build
cd NeoForge/26.2 && ./gradlew build
```

Requires JDK 25 (Minecraft 26.x toolchain).

## Links

- Other branches: [`26.1`](https://github.com/Kishku7/elytrahud3/tree/26.1), [`1.20.x`](https://github.com/Kishku7/elytrahud3/tree/1.20.x), [`1.21.x`](https://github.com/Kishku7/elytrahud3/tree/1.21.x)
- Overview: [`main`](https://github.com/Kishku7/elytrahud3/tree/main)
- Modrinth: https://modrinth.com/mod/elytrahud3
- Discord: https://discord.gg/2ZxzbCzAHe

MIT licensed. Based on elytrahud-rework by inorganic / wancor1 (MIT).
