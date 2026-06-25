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
