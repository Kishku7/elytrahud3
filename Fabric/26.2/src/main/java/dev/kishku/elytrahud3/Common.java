package dev.kishku.elytrahud3;

import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents;
import net.fabricmc.fabric.api.client.rendering.v1.hud.HudElementRegistry;
import net.fabricmc.fabric.api.client.rendering.v1.hud.VanillaHudElements;
import net.minecraft.client.Minecraft;
import net.minecraft.resources.Identifier;

public class Common implements ClientModInitializer {
    public static final String MODID = "elytrahud3";

    public static ElytraHudConfig CONFIG;
    public static HudData hudData = new HudData();
    public static Minecraft client;
    public static HudRenderer hudRenderer;

    @Override
    public void onInitializeClient() {
        CONFIG = ConfigManager.getConfig();
        client = Minecraft.getInstance();
        hudRenderer = new HudRenderer(client);

        // END_LEVEL_TICK supplies the ClientLevel; grab the client ourselves.
        ClientTickEvents.END_LEVEL_TICK.register(level -> {
            Minecraft mc = Minecraft.getInstance();
            var player = mc.player;
            if (player == null || CONFIG == null || !CONFIG.modEnabled) {
                return;
            }
            if (player.isFallFlying() || CONFIG.alwaysDisplayHud) {
                hudData.update();
            }
        });

        HudElementRegistry.attachElementBefore(
            VanillaHudElements.HOTBAR,
            Identifier.fromNamespaceAndPath(MODID, "hud"),
            (graphics, tickDelta) -> {
                if (CONFIG == null || !CONFIG.modEnabled) {
                    return;
                }
                var player = client.player;
                if (player == null) {
                    return;
                }
                if (!CONFIG.alwaysDisplayHud && !player.isFallFlying()) {
                    return;
                }
                hudRenderer.render(graphics, tickDelta);
            }
        );
    }
}
