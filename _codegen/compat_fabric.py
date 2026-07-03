"""compat_fabric.py -- Fabric glue emitters (Common entrypoint).

Eras (glue-API map, elytrahud3.md, boot-verified in the 1.1.x line):
  <=1.21.5 : HudRenderCallback.EVENT + ClientTickEvents.END_WORLD_TICK (verbatim published body;
             the render lambda's param types are INFERRED, so the same text binds
             (GuiGraphics, float) on 1.20.x and (GuiGraphics, DeltaTracker) on 1.21+).
  1.21.6+  : HudElementRegistry.attachElementBefore(VanillaHudElements.HOTBAR); ResourceLocation
             until the 1.21.9 Identifier rename. (fabric-api deprecated HudRenderCallback at the
             1.21.6 line -- registry form starts THERE, found by -Xlint:all 2026-07-03.)
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
 * Pre-1.21.6 Fabric client entrypoint. Registers HUD rendering via the legacy
 * {@link HudRenderCallback} (HudElementRegistry/VanillaHudElements does not exist before 1.21.6)
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
    # HudElementRegistry/VanillaHudElements ship from the 1.21.6-line fabric-api (rendering-v1
    # 23.x, verified in the cached module jars 2026-07-03), where HudRenderCallback is already
    # deprecated -- so the registry form starts at 1.21.6, NOT 1.21.9. Below 1.21.6 the registry
    # does not exist and HudRenderCallback is undeprecated.
    if core._vt(ver) >= (1, 21, 6):
        t = core.read_twin(codegen, "Fabric/26/src/main/java/dev/kishku/elytrahud3/Common.java")
        if not core.is26(ver):
            # fabric-api pre-26 still names the tick event END_WORLD_TICK.
            t = core.sub(t, "END_LEVEL_TICK", "END_WORLD_TICK", count=2)
        if not core.renamed_identifier(ver):
            # 1.21.6-1.21.8: same registry API, ResourceLocation id type (factory era).
            t = core.sub(t, "Identifier", "ResourceLocation")
        core.emit(cog, t)
    else:
        t = _LEGACY_COMMON
        if core._vt(ver) >= (1, 21, 5):
            # fabric-api 0.128.x+1.21.5 already deprecates HudRenderCallback, but its replacement
            # (hud/HudElementRegistry) moved packages MID-1.21.5-line (rendering-v1 12.x root pkg ->
            # 16.x hud pkg) and would demand a fabric-api floor this jar does not declare
            # (depends: fabric-api "*"). The callback is the only form valid across the whole
            # claimed fabric-api range -- keep it, narrowest suppression, boot-proven in 1.1.x.
            t = core.sub(t,
                         "    @Override\n    public void onInitializeClient() {",
                         "    // fabric-api 0.128.x+1.21.5 deprecates HudRenderCallback; the replacement moved packages\n"
                         "    // mid-line and needs a fabric-api floor this jar does not demand (depends: fabric-api *).\n"
                         "    @SuppressWarnings(\"deprecation\")\n"
                         "    @Override\n    public void onInitializeClient() {",
                         count=1)
        core.emit(cog, t)
