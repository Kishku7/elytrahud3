# Changelog

All notable changes to ElytraHud3 are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.0.0/). Jars are named `<mod_version>+<mc-family>`.
Versioning policy is universal across all mods and is NOT restated here -- see Memory/minecraft/mod-rules.md.

## [Unreleased]

## [1.2.11] - 2026-08-05

### Changed
- **Fabric 26.3 cell moved to MC 26.3-snapshot-7** (from snapshot-6): fabric-api
  `0.156.1+26.3` -> `0.156.2+26.3`, resource `pack_format` `94` -> `95`, exclusive window
  `[26.3-alpha.6, 26.3-alpha.7)` -> `[26.3-alpha.7, 26.3-alpha.8)`. Every 26.3 snapshot bumps
  pack_format by one, so each jar stays snapshot-exclusive. No other cell changed.

### Notes
- **No source change required.** snapshot-7's breaking surfaces were checked against this mod and
  none are touched: the trailing `Prediction` argument on `LivingEntity.drop(ItemStack, boolean)` /
  `Inventory.placeItemBackInInventory`, the client-side `LocalPlayer.drop(boolean)` return type
  going `boolean` -> `void`, the `InteractionResult.SwingSource` `CLIENT`/`SERVER` ->
  `PREDICTED`/`SERVER_ONLY` rename together with the deletion of `ServerboundSwingPacket`, and the
  32 new concrete slab/stair blocks plus the filled-map colour component removals.
## [1.2.10] - 2026-07-31

### Fixed
- **Full D1-D22 doctrine re-audit found + fixed real live-boot and resource-pack bugs across
  9 cells.** Rebuilt and republished the affected (loader, MC) pairs:
  - **D3 claim-gate over-claims (4 cells), root-caused via built-jar manifest inspection:**
    `Forge/1.21.1` claimed MC `[1.21,1.21.2)` needing javafml 52+, but MC 1.21.0 shipped Forge
    51.0.33/javafml 51 -- narrowed to `[1.21.1,1.21.2)`. `Forge/1.21.8` claimed
    `[1.21.6,1.21.9)` needing javafml 58+, but 1.21.6/1.21.7 are permanent orphan Forge builds
    -- narrowed to `[1.21.8,1.21.9)`. `Forge/1.20.6` claimed `[1.20.5,1.21)` but Forge never
    shipped MC 1.20.5 -- narrowed to `[1.20.6,1.21)`. `NeoForge/1.21.1` had the same shape
    (`[1.21,1.21.2)` vs the neo 21.1 floor, MC 1.21.0 ships neo 21.0.x) -- narrowed to
    `[1.21.1,1.21.2)`. Each of these previously refused to boot on part of its claimed range.
  - **D3a NeoForge 26.1 over-blocking floor:** relaxed `[26.1.2.0-beta,)` -> `[26.1.0-alpha,)`
    -- the mod's actual NeoForge glue uses no 26.1.2-specific API, so the tighter floor was
    silently blocking 26.1 and 26.1.1 users for no reason.
  - **D4 pack.mcmeta dead-zone (5 cells) -- the mod had never gotten the 2026-07-12 doctrine
    correction every sibling mod already carries.** `Fabric/1.21.11`, `NeoForge/1.21.10`,
    `NeoForge/1.21.11` were shipping the WRONG resource-major pack.mcmeta (should ship NONE --
    both loaders synthesise correct metadata in the 1.21.9-1.21.11 dead zone);
    `Forge/1.21.10`/`1.21.11` were shipping the wrong major too (corrected to the DATA-major
    form, 88/94). A present-but-wrong pack.mcmeta drops the mod's WHOLE resource pack on
    Forge/NeoForge -- HUD gauge textures and lang were gone for every live user on those
    versions. Verified in every rebuilt jar (unzip-checked) and client-render smoketested.

### Changed
- Version 1.2.9 -> **1.2.10** on the 10 affected cells only (Forge 1.20.6/1.21.1/1.21.8/
  1.21.10/1.21.11, NeoForge 1.21.1/1.21.10/1.21.11/26.1, Fabric 1.21.11); every other cell is
  byte-unchanged and stays at its prior published version. All 10 rebuilt `-Xlint:all` zero
  warnings; client-render smoketested on Raider (all 10 CELL PASS, HUD instruments verified by
  eye in every screenshot).

## [1.2.9] - 2026-07-28

### Fixed
- **The ModMenu pin was wrong on two of the three 26.x rows.** The Fabric 26 cell carried a
  SINGLE `mod_menu_version=18.0.0` used for 26.1, 26.2 and 26.3 alike -- but ModMenu ships a
  separate major per MC line (18.x = 26.1, 20.x = 26.2, 21.x = 26.3), and an older major is
  INTERMEDIARY-named against a newer mojmap MC. So 26.2 and 26.3 were compiling against
  26.1-era ModMenu and only got away with it because EH3 touches just the ModMenuApi surface.
  `mod_menu_version` is now a PER-26.X matrix value in `scripts/build-fabric.ps1`
  (**26.1 -> 18.0.0, 26.2 -> 20.0.1, 26.3 -> 21.0.0-alpha.1**), passed through as `-P`.
  Same root cause as the ASR 26.1 build failure.

### Changed
- Version 1.2.8 -> **1.2.9**; Fabric 26.1 / 26.2 / 26.3 rebuilt against the correct ModMenu.

## [1.2.8] - 2026-07-28

### Changed
- **Fabric 26.3 cell moved to MC 26.3-snapshot-6** (from snapshot-5): fabric-api
  `0.155.3+26.3` -> `0.156.1+26.3`, `pack_format` `93` -> `94`, exclusive pin
  `26.3-alpha.5` -> `26.3-alpha.6`.

### Notes
- **No source change required.** The whole tree was scanned against every snapshot-6 breaking
  surface (worldgen noise overhaul, Entity invulnerability split, `startSleeping` void ->
  boolean, `SharedSuggestionProvider` filter parameter, `InputWithModifiers.getDigit()`
  removal, options-screen reshuffle, terrain multidraw path, block-entity loot helpers) with
  zero hits.

## [1.2.7] - 2026-07-27

### Changed
- NeoForge 26 cells rebuilt against the now-PUBLISHED NeoForge builds: 26.1 -> 26.1.2.87, 26.2 -> 26.2.0.35-beta (previously 26.1.2.30-beta / 26.2.0.1-beta). The [26.1.2.0-beta,) floor is unchanged.
- mavenLocal() removed from the NeoForge/26 cell; the cell README example build command no longer pins the superseded loader build.
- No source or behaviour change. Server-boot smoketested on NeoForge 26.1.2 and 26.2.

## [1.2.6] - 2026-07-23

### Fixed
- **HUD no longer flashes on the creative/spectator fly toggle.** Double-tapping the jump key (the
  vanilla creative/spectator "toggle fly" gesture) while an elytra is in the **vanilla chest slot**
  made vanilla optimistically start an elytra glide for a moment -- it sets the fall-flying flag and
  asks the server, which then rejects it -- and ElytraHud3 briefly drew the HUD before the server
  correction cleared it. The visibility gate now also requires the player to NOT be in
  creative/spectator flight (`!getAbilities().flying`); a real elytra glide never overlaps creative
  fly, so the transient blip no longer draws while a true glide still shows normally. This only
  occurred with the elytra in the vanilla chest slot -- it does NOT happen when the elytra is worn
  via the **Elytra Trinket** mod's trinket slot (that leaves the chest slot empty, so vanilla never
  attempts the glide-start). The fix uses vanilla APIs only and adds NO dependency on Elytra Trinket.


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
