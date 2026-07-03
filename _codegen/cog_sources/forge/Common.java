// SHARED SOURCE -- canonical location: _codegen/cog_sources/forge (version-invariant Forge glue;
// no 26 twin, Forge ends at 1.21.8). Copied verbatim into each pre-26 forge cell's gen/ by
// scripts/cog-gen.ps1.
package dev.kishku.elytrahud3;

import net.minecraft.client.Minecraft;

/**
 * Loader-agnostic shared state holder. Populated by the platform entrypoint
 * (Fabric ClientModInitializer / NeoForge @Mod client init).
 */
public final class Common {
    public static final String MODID = "elytrahud3";

    public static ElytraHudConfig CONFIG;
    public static HudData hudData = new HudData();
    public static Minecraft client;
    public static HudRenderer hudRenderer;

    private Common() {}
}
