"""compat_neoforge.py -- NeoForge glue emitters (entry + client).

Eras (glue-API map, elytrahud3.md, boot-verified in the 1.1.x line):
  entry:
    26        : ctor (ModContainer, IEventBus, Dist)                      [master = NeoForge/26 twin]
    1.21.9-11 : ctor (IEventBus, ModContainer, Dist)  -- FMLEnvironment.dist field GONE at 21.11
    <=1.21.8  : ctor (IEventBus, ModContainer) + FMLEnvironment.dist check
  client:
    26        : RegisterGuiLayersEvent/VanillaGuiLayers + ClientTickEvent.Post + IConfigScreenFactory,
                Identifier                                                 [master = NeoForge/26 twin]
    20.5-21.8 : same event shape; ResourceLocation (factory from 1.21; the NeoForge 1.20.x line did
                NOT backport the RL factories, so 1.20.6 keeps the ctor)
    20.4      : RegisterGuiOverlaysEvent/IGuiOverlay + TickEvent.ClientTickEvent (phase END) +
                ConfigScreenHandler (NeoGradle7-era API)                   [verbatim published body]
Common (holder) + ConfigManager are version-invariant plain files in cog_sources/neoforge.
"""

import compat_core as core

_NF204_CLIENT = """package dev.kishku.elytrahud3;

import net.minecraft.client.Minecraft;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.ModContainer;
import net.neoforged.neoforge.client.ConfigScreenHandler;
import net.neoforged.neoforge.client.event.RegisterGuiOverlaysEvent;
import net.neoforged.neoforge.client.gui.overlay.VanillaGuiOverlay;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.event.TickEvent;

/**
 * NeoForge 1.20.4 (NeoForge 20.4) client bootstrap. Pre-LayeredDraw: HUD is a
 * {@link RegisterGuiOverlaysEvent} IGuiOverlay drawn below the hotbar; tick is the legacy
 * {@link TickEvent.ClientTickEvent} (phase END); config screen via the old
 * {@link ConfigScreenHandler.ConfigScreenFactory} extension point. Render delta is a float.
 */
public final class ElytraHud3NeoForgeClient {
    private ElytraHud3NeoForgeClient() {}

    public static void init(ModContainer mod, IEventBus bus) {
        bus.addListener(ElytraHud3NeoForgeClient::registerOverlays);
        NeoForge.EVENT_BUS.addListener(ElytraHud3NeoForgeClient::onClientTick);
        mod.registerExtensionPoint(ConfigScreenHandler.ConfigScreenFactory.class,
            () -> new ConfigScreenHandler.ConfigScreenFactory(
                (mc, parent) -> new ElytraHudConfigScreen(parent)));
    }

    private static void ensureClient() {
        if (Common.client == null) {
            Common.client = Minecraft.getInstance();
        }
        if (Common.hudRenderer == null && Common.client != null) {
            Common.hudRenderer = new HudRenderer(Common.client);
        }
    }

    private static void registerOverlays(RegisterGuiOverlaysEvent event) {
        event.registerBelow(VanillaGuiOverlay.HOTBAR.id(), "elytrahud3_hud",
            (gui, graphics, partialTick, screenWidth, screenHeight) -> {
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
                Common.hudRenderer.render(graphics, partialTick);
            });
    }

    private static void onClientTick(TickEvent.ClientTickEvent event) {
        if (event.phase != TickEvent.Phase.END) {
            return;
        }
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
"""


def emit_entry(cog, ver, codegen):
    t = core.read_twin(codegen, "NeoForge/26/src/main/java/dev/kishku/elytrahud3/ElytraHud3NeoForge.java")
    if not core.is26(ver):
        if core.renamed_identifier(ver):
            t = core.sub(t, "public ElytraHud3NeoForge(ModContainer mod, IEventBus bus, Dist dist) {",
                         "public ElytraHud3NeoForge(IEventBus bus, ModContainer mod, Dist dist) {", count=1)
        else:
            t = core.sub(t, "public ElytraHud3NeoForge(ModContainer mod, IEventBus bus, Dist dist) {",
                         "public ElytraHud3NeoForge(IEventBus bus, ModContainer mod) {", count=1)
            t = core.sub(t, "if (dist.isClient()) {",
                         "if (FMLEnvironment.dist == Dist.CLIENT) {", count=1)
            t = core.sub(t, "import net.neoforged.fml.common.Mod;",
                         "import net.neoforged.fml.common.Mod;\nimport net.neoforged.fml.loading.FMLEnvironment;", count=1)
    core.emit(cog, t)


def emit_client(cog, ver, codegen):
    if core._vt(ver) < (1, 20, 5):
        core.emit(cog, _NF204_CLIENT)
        return
    t = core.read_twin(codegen, "NeoForge/26/src/main/java/dev/kishku/elytrahud3/ElytraHud3NeoForgeClient.java")
    if not core.renamed_identifier(ver):
        if core.has_rl_factory(ver, "neoforge"):
            t = core.sub(t, "Identifier", "ResourceLocation")
        else:
            t = core.sub(t, "import net.minecraft.resources.Identifier;",
                         "import net.minecraft.resources.ResourceLocation;", count=1)
            t = core.sub(t, 'Identifier.fromNamespaceAndPath(Common.MODID, "hud")',
                         'new ResourceLocation(Common.MODID, "hud")', count=1)
    core.emit(cog, t)
