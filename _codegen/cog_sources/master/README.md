# _codegen/cog_sources/master

MC-COUPLED shared client source. Compiles against each loader's mojmap-native Minecraft (26.x is
unobfuscated, so one source serves both loaders). Pulled into each loader build via `srcDir`.
EDIT HERE ONLY; never edit a build output.

- `HudData` -- per-tick player/flight sampling.
- `HudRenderer` / `HudRenderHelper` -- gauge rendering.
- `ElytraHudConfigScreen` -- vanilla-widget config screen.
- `McCompat` -- reflective 26.1.x <-> 26.2/26.3 cross-version shim (the reason no per-version forks are needed).
