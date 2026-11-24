package dev.kishku.elytrahud3;

import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents;
import net.fabricmc.fabric.api.client.rendering.v1.hud.HudElement;
import net.fabricmc.fabric.api.client.rendering.v1.hud.HudElementRegistry;
import net.fabricmc.fabric.api.client.rendering.v1.hud.VanillaHudElements;
import net.minecraft.client.DeltaTracker;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.resources.Identifier;

import java.lang.reflect.Proxy;

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
            hudElement()
        );
    }

    /**
     * The HUD element callback changed shape at 26.4 (render(graphics, DeltaTracker) became
     * extractRenderState(graphics)), so one source builds the element through a proxy that answers
     * whichever of the two methods this fabric-api calls.
     */
    private static HudElement hudElement() {
        return (HudElement) Proxy.newProxyInstance(HudElement.class.getClassLoader(), new Class<?>[]{HudElement.class},
            (proxy, method, args) -> {
                switch (method.getName()) {
                    case "render", "extractRenderState" -> draw((GuiGraphicsExtractor) args[0],
                            args.length > 1 ? (DeltaTracker) args[1] : client.getDeltaTracker());
                    case "equals" -> {
                        return proxy == args[0];
                    }
                    case "hashCode" -> {
                        return System.identityHashCode(proxy);
                    }
                    case "toString" -> {
                        return "ElytraHud3 HUD element";
                    }
                    default -> {
                        // Updatable.update(DeltaTracker): nothing to do
                    }
                }
                return null;
            });
    }

    private static void draw(GuiGraphicsExtractor graphics, DeltaTracker tickDelta) {
        if (CONFIG == null || !CONFIG.modEnabled) {
            return;
        }
        var player = client.player;
        if (player == null) {
            return;
        }
        if (!CONFIG.alwaysDisplayHud && !(player.isFallFlying() && !player.getAbilities().flying)) {
            return;
        }
        hudRenderer.render(graphics, tickDelta);
    }
}
