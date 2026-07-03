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
        // NOTE: do NOT touch Minecraft.getInstance() here -- during @Mod construction it can be null.
        bus.addListener(ElytraHud3NeoForgeClient::registerGuiLayers);
        NeoForge.EVENT_BUS.addListener(ElytraHud3NeoForgeClient::onClientTick);
        mod.registerExtensionPoint(IConfigScreenFactory.class,
            (container, parent) -> new ElytraHudConfigScreen(parent));
    }

    /** Resolve the client + renderer lazily; getInstance() is reliably non-null by first tick/frame. */
    private static void ensureClient() {
        if (Common.client == null) {
            Common.client = Minecraft.getInstance();
        }
        if (Common.hudRenderer == null && Common.client != null) {
            Common.hudRenderer = new HudRenderer(Common.client);
        }
    }

    private static void registerGuiLayers(RegisterGuiLayersEvent event) {
        // Draw just below the hotbar (equivalent to Fabric's attachElementBefore(HOTBAR)).
        event.registerBelow(
            VanillaGuiLayers.HOTBAR,
            Identifier.fromNamespaceAndPath(Common.MODID, "hud"),
            (graphics, delta) -> {
                ElytraHudConfig config = Common.CONFIG;
                if (config == null || !config.modEnabled) {
                    return;
                }
                ensureClient();
                Minecraft client = Common.client;
                if (client == null || Common.hudRenderer == null) {
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
        ensureClient();
        if (Common.client == null) {
            return;
        }
        var player = Common.client.player;
        if (player == null) {
            return;
        }
        if (player.isFallFlying() || config.alwaysDisplayHud) {
            Common.hudData.update();
        }
    }
}
