# Changelog

All notable changes to ElytraHud3 are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.0.0/). Versions are `<mod_version>+<mc-family>`;
`mod_version` bumps only on a feature/behaviour change (a new MC-version port keeps the current
`mod_version`).

## [Unreleased]

## [1.2.5] - 2026-07-21

### Changed
- 26.3 Fabric cell retargeted `26.3-snapshot-3` -> `26.3-snapshot-5` (fabric-api 0.155.3+26.3,
  dep `26.3-alpha.5`, resource pack_format 93). HUD + config screen render clean in-world on the
  snapshot (headless client-harness eyeballed: all flight instruments draw).
- Sourced ModMenu from Modrinth's maven (`maven.modrinth:modmenu`) on the 26 cell instead of
  `maven.terraformersmc.com`, which stopped serving the 18.x ModMenu artifacts the config-screen
  entrypoint compiles against. Fabric-only (no NeoForge/Forge upstream on 26.3).
  Config screen + HUD compile clean against the snap-4 GLFW->SDL / renderpearl API changes.
- Build refactor (no behaviour change): eliminated the `_codegen/cog_sources/master/` and `_codegen/cog_sources/common/`
  source trees, folding them into the `_codegen/cog_sources` single source of truth (D16).

### Added
- `publish.json` for the shared `tools/mod-publish/publish.py` publisher; retired the per-version
  `_publish_eh3_*.py` one-offs.

## [1.2.4] - 2026-07-07
### Added
- MC `26.3-snapshot-3` support (Fabric), snapshot-3 exclusive. Published to Modrinth.

## [1.2.3] - 2026-07-06
### Added
- Forge coverage extended through 1.21.11 (was 1.21.8).
### Changed
- Full audit (D1-D13 + Q1-Q7) conformance pass; Modrinth description single-sourced from the README.

## [1.2.2] - 2026-07-04
### Changed
- Forge per-loader glue single-sourced (4 templates -> 1 assembly, byte-identical across the Forge cells).

## [1.2.1] - 2026-07-04
### Added
- Forge 1.20.2-1.20.4 cells; orphan-Forge versions mapped.
### Changed
- Unification revision on the single-source cog model; all cells `-Xlint:all` clean.

## [1.2.0]
### Changed
- Unified onto the single-source cog build model (one `minecraft-1.20-26.3` branch, per-loader cells
  generated from `_codegen`).

## [1.1.0] - 2026-06-16
### Added
- Backfill across the 1.20.x and 1.21.x lines (17 new jars), Fabric + NeoForge (+ Forge where available).

## [1.0.3+26.2]
### Added
- Stable MC 26.2 release (Fabric + NeoForge), client-only.

## [1.0.1] - 2026-06-14
### Changed
- MC 26.2-rc-2; repository restructured.

## [1.0.0] - 2026-06-11
### Added
- Initial release: aviation-style analog-gauge flight HUD for elytra flight. MC 26.1/26.2, Fabric +
  NeoForge, client-only. `McCompat` cross-version reflection shim (one source across 26.1.x/26.2).
  Do-a-Barrel-Roll compatible.
