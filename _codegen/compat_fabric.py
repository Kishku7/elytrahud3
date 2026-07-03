"""compat_fabric.py -- Fabric glue emitters (Common entrypoint).

Eras (glue-API map, elytrahud3.md, boot-verified in the 1.1.x line):
  <=1.21.8 : HudRenderCallback.EVENT + ClientTickEvents.END_WORLD_TICK (verbatim published body;
             the render lambda's param types are INFERRED, so the same text binds
             (GuiGraphics, float) on 1.20.x and (GuiGraphics, DeltaTracker) on 1.21+).
  1.21.9+  : HudElementRegistry.attachElementBefore(VanillaHudElements.HOTBAR) + Identifier.
  26       : same registration; tick event renamed END_WORLD_TICK -> END_LEVEL_TICK.
Master for the 1.21.9+ form = the plain twin in Fabric/26 (check-sync guarded).
ElytraHudModMenu + ConfigManager are version-invariant plain files in cog_sources/fabric.
"""

import compat_core as core

_LEGACY_COMMON = """package dev.kishku.elytrahud3;

import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents;
import net.fabricmc.fabric.api.client.rendering.v1.HudRenderCallback;
import net.minecraft.client.Minecraft;

/**
 * Pre-1.21.9 Fabric client entrypoint. Registers HUD rendering via the legacy
 * {@link HudRenderCallback} (HudElementRegistry/VanillaHudElements does not exist before 1.21.9)
 * and tick sampling via ClientTickEvents. The shared HUD logic lives in HudRenderer/HudData.
 */
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

        // END_WORLD_TICK supplies the ClientLevel; grab the client ourselves.
        ClientTickEvents.END_WORLD_TICK.register(level -> {
            Minecraft mc = Minecraft.getInstance();
            var player = mc.player;
            if (player == null || CONFIG == null || !CONFIG.modEnabled) {
                return;
            }
            if (player.isFallFlying() || CONFIG.alwaysDisplayHud) {
                hudData.update();
            }
        });

        HudRenderCallback.EVENT.register((graphics, tickDelta) -> {
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
        });
    }
}
"""


def emit_common(cog, ver, codegen):
    if core.renamed_identifier(ver):
        t = core.read_twin(codegen, "Fabric/26/src/main/java/dev/kishku/elytrahud3/Common.java")
        if not core.is26(ver):
            # fabric-api on the 1.21.9-1.21.11 line still names the tick event END_WORLD_TICK.
            t = core.sub(t, "END_LEVEL_TICK", "END_WORLD_TICK", count=2)
        core.emit(cog, t)
    else:
        core.emit(cog, _LEGACY_COMMON)
