package dev.kishku.elytrahud3;

import net.minecraft.client.Minecraft;
import net.minecraft.resources.Identifier;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.ModContainer;
import net.neoforged.neoforge.client.event.ClientTickEvent;
import net.neoforged.neoforge.client.event.RegisterGuiLayersEvent;
import net.neoforged.neoforge.client.gui.IConfigScreenFactory;
import net.neoforged.neoforge.client.gui.VanillaGuiLayers;
import net.neoforged.neoforge.common.NeoForge;

/** NeoForge client bootstrap: HUD layer + per-tick data update + config screen (no ModMenu needed). */
public final class ElytraHud3NeoForgeClient {
    private ElytraHud3NeoForgeClient() {}

    public static void init(ModContainer mod, IEventBus bus) {
        Common.client = Minecraft.getInstance();
        Common.hudRenderer = new HudRenderer(Common.client);

        // HUD layer registration (mod bus)
        bus.addListener(ElytraHud3NeoForgeClient::registerGuiLayers);

        // Per-tick HUD data update (game bus)
        NeoForge.EVENT_BUS.addListener(ElytraHud3NeoForgeClient::onClientTick);

        // In-game config screen via NeoForge's own mod-list hook (no ModMenu / YACL).
        mod.registerExtensionPoint(IConfigScreenFactory.class,
            (container, parent) -> new ElytraHudConfigScreen(parent));
    }

    private static void registerGuiLayers(RegisterGuiLayersEvent event) {
        // Draw just below the hotbar (equivalent to Fabric's attachElementBefore(HOTBAR)).
        // graphics/delta types are inferred from GuiLayer.render so we stay mapping-agnostic.
        event.registerBelow(
            VanillaGuiLayers.HOTBAR,
            Identifier.fromNamespaceAndPath(Common.MODID, "hud"),
            (graphics, delta) -> {
                ElytraHudConfig config = Common.CONFIG;
                Minecraft client = Common.client;
                if (config == null || !config.modEnabled || client == null) {
                    return;
                }
                var player = client.player;
                if (player == null) {
                    return;
                }
                if (!config.alwaysDisplayHud && !player.isFallFlying()) {
                    return;
                }
                Common.hudRenderer.render(graphics, delta);
            });
    }

    private static void onClientTick(ClientTickEvent.Post event) {
        ElytraHudConfig config = Common.CONFIG;
        if (config == null || !config.modEnabled) {
            return;
        }
        var player = Minecraft.getInstance().player;
        if (player == null) {
            return;
        }
        if (player.isFallFlying() || config.alwaysDisplayHud) {
            Common.hudData.update();
        }
    }
}
