# shared_common

MC-AGNOSTIC shared source + shared assets. Single source of truth -- pulled into each loader build via
`srcDir`. EDIT HERE ONLY; never edit a build output.

- `src/main/java/.../ElytraHudConfig.java` -- the config POJO (no Minecraft imports).
- `src/main/resources/assets/elytrahud3/` -- lang, textures, icon (shared, identical across loaders/versions).
