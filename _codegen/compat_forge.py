"""compat_forge.py -- Forge glue emitters (entry + client). Forge has no 26 cell (FG6 cannot
build 26.x), so unlike fabric/neoforge these eras are embedded verbatim from the proven,
boot-verified 1.1.x-line files rather than derived from a 26 twin.

Eras (glue-API map, elytrahud3.md; EventBus boundary pinned by javap, mod-version-gates.md):
  entry:
    <=1.21.5 (Forge <=55) : classic no-arg ctor + FMLJavaModLoadingContext.get().getModEventBus()
    1.21.6+  (Forge 56+)  : EventBus 7 -- ctor (FMLJavaModLoadingContext) + context.getModBusGroup()
  client:
    1.20/1.20.1 (46/47)   : RegisterGuiOverlaysEvent/IGuiOverlay + VanillaGuiOverlay.HOTBAR.id()
                            (this jar is also the NeoForge <=1.20.1 jar -- fork point)
    1.20.6 (50)           : AddGuiOverlayLayersEvent + getLayeredDraw().addBelow(PRE_SLEEP_STACK,
                            id, ForgeLayeredDraw.HOTBAR, layer); split TickEvent...Post
    1.21-1.21.5 (51-55)   : anchor-free getLayeredDraw().add(id, layer) -- the addBelow anchors do
                            not resolve at event time on 52/55 (the addBelow false-PASS trap;
                            KEEP the anchor-free form), classic bus
    1.21.6+ (56+, cell 1.21.8) : same layer form, EventBus 7 BusGroup listeners
  ConfigManager (FMLPaths, net.minecraftforge) + Common (holder) are version-invariant plain
  files in cog_sources/forge.
"""

import compat_core as core

_ENTRY_CLASSIC = """package dev.kishku.elytrahud3;

import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;
import net.minecraftforge.fml.loading.FMLEnvironment;

@Mod(Common.MODID)
public class ElytraHud3Forge {
    public ElytraHud3Forge() {
        Common.CONFIG = ConfigManager.getConfig();
        if (FMLEnvironment.dist == Dist.CLIENT) {
            IEventBus modBus = FMLJavaModLoadingContext.get().getModEventBus();
            ElytraHud3ForgeClient.init(modBus);
        }
    }
}
"""

_ENTRY_EB7 = """package dev.kishku.elytrahud3;

import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.eventbus.api.bus.BusGroup;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;
import net.minecraftforge.fml.loading.FMLEnvironment;

@Mod(Common.MODID)
public class ElytraHud3Forge {
    public ElytraHud3Forge(FMLJavaModLoadingContext context) {
        Common.CONFIG = ConfigManager.getConfig();
        if (FMLEnvironment.dist == Dist.CLIENT) {
            BusGroup modBus = context.getModBusGroup();
            ElytraHud3ForgeClient.init(modBus);
        }
    }
}
"""

_CLIENT_IGUI = """package dev.kishku.elytrahud3;

import net.minecraft.client.Minecraft;
import net.minecraftforge.client.ConfigScreenHandler;
import net.minecraftforge.client.event.RegisterGuiOverlaysEvent;
import net.minecraftforge.client.gui.overlay.VanillaGuiOverlay;
import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.event.TickEvent;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fml.ModLoadingContext;

/**
 * Forge 1.20/1.20.1 client bootstrap. HUD via {@link RegisterGuiOverlaysEvent} IGuiOverlay below
 * the hotbar; tick via {@link TickEvent.ClientTickEvent} (phase END); config screen via the
 * {@link ConfigScreenHandler.ConfigScreenFactory} extension point. Render delta is a float.
 * (The 1.20.1 jar also runs on NeoForge 1.20.1 -- the fork point -- which shares the
 * net.minecraftforge namespace and mods.toml format.)
 */
public final class ElytraHud3ForgeClient {
    private ElytraHud3ForgeClient() {}

    public static void init(IEventBus modBus) {
        modBus.addListener(ElytraHud3ForgeClient::registerOverlays);
        MinecraftForge.EVENT_BUS.addListener(ElytraHud3ForgeClient::onClientTick);
        ModLoadingContext.get().registerExtensionPoint(ConfigScreenHandler.ConfigScreenFactory.class,
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

_CLIENT_LAYERED_106 = """package dev.kishku.elytrahud3;

import net.minecraft.client.Minecraft;
import net.minecraft.resources.ResourceLocation;
import net.minecraftforge.client.ConfigScreenHandler;
import net.minecraftforge.client.event.AddGuiOverlayLayersEvent;
import net.minecraftforge.client.gui.overlay.ForgeLayeredDraw;
import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.event.TickEvent;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fml.ModLoadingContext;

/**
 * Forge 1.20.6 client bootstrap. Forge 1.20.6 (50.x) replaced RegisterGuiOverlaysEvent/IGuiOverlay
 * with the vanilla LayeredDraw system: add a {@link net.minecraft.client.gui.LayeredDraw.Layer}
 * below the hotbar via {@link AddGuiOverlayLayersEvent}#getLayeredDraw().addBelow(...). Tick is the
 * split {@link TickEvent.ClientTickEvent.Post}; config screen via {@link ConfigScreenHandler}.
 * LayeredDraw.Layer renders with a float partialTick (DeltaTracker is 1.21+).
 */
public final class ElytraHud3ForgeClient {
    private ElytraHud3ForgeClient() {}

    public static void init(IEventBus modBus) {
        modBus.addListener(ElytraHud3ForgeClient::addGuiLayers);
        MinecraftForge.EVENT_BUS.addListener(ElytraHud3ForgeClient::onClientTick);
        ModLoadingContext.get().registerExtensionPoint(ConfigScreenHandler.ConfigScreenFactory.class,
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

    private static void addGuiLayers(AddGuiOverlayLayersEvent event) {
        event.getLayeredDraw().addBelow(
            ForgeLayeredDraw.PRE_SLEEP_STACK,
            @ID_HUD@,
            ForgeLayeredDraw.HOTBAR,
            (graphics, partialTick) -> {
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

    private static void onClientTick(TickEvent.ClientTickEvent.Post event) {
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

_CLIENT_ADD_CLASSIC = """package dev.kishku.elytrahud3;

import net.minecraft.client.Minecraft;
import net.minecraft.resources.ResourceLocation;
import net.minecraftforge.client.ConfigScreenHandler;
import net.minecraftforge.client.event.AddGuiOverlayLayersEvent;
import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.event.TickEvent;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fml.ModLoadingContext;

/**
 * Forge 1.21-1.21.5 (51.x-55.x) client bootstrap. HUD is a LayeredDraw layer attached with the
 * anchor-FREE 2-arg getLayeredDraw().add(newLayer, layer) -- the anchor-relative addBelow/addAbove
 * overloads fail at AddGuiOverlayLayersEvent time on 52.x/55.x ("Expected layer ... was not found
 * in stack minecraft:vanilla_root"), silently rendering nothing; the anchor-free add needs no
 * existing target and draws after the vanilla in-game layers, which is what we want (verified
 * against forge-1.21.1-52.1.14 and forge-1.21.5-55.1.10 ForgeLayeredDraw -- KEEP this form).
 * Tick is the split {@link TickEvent.ClientTickEvent.Post}; config screen via
 * {@link ConfigScreenHandler}. LayeredDraw.Layer renders with a float partialTick.
 */
public final class ElytraHud3ForgeClient {
    private ElytraHud3ForgeClient() {}

    public static void init(IEventBus modBus) {
        modBus.addListener(ElytraHud3ForgeClient::addGuiLayers);
        MinecraftForge.EVENT_BUS.addListener(ElytraHud3ForgeClient::onClientTick);
        ModLoadingContext.get().registerExtensionPoint(ConfigScreenHandler.ConfigScreenFactory.class,
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

    private static void addGuiLayers(AddGuiOverlayLayersEvent event) {
        event.getLayeredDraw().add(
            @ID_HUD@,
            (graphics, partialTick) -> {
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

    private static void onClientTick(TickEvent.ClientTickEvent.Post event) {
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

_CLIENT_ADD_EB7 = """package dev.kishku.elytrahud3;

import net.minecraft.client.Minecraft;
import net.minecraft.resources.ResourceLocation;
import net.minecraftforge.client.ConfigScreenHandler;
import net.minecraftforge.client.event.AddGuiOverlayLayersEvent;
import net.minecraftforge.event.TickEvent;
import net.minecraftforge.eventbus.api.bus.BusGroup;
import net.minecraftforge.fml.ModLoadingContext;

/**
 * Forge 1.21.6+ (56.x+) client bootstrap. Forge 56 rewrote the event bus (EventBus 7.x BusGroup):
 * mod-bus events are subscribed via {@code Event.getBus(modBus).addListener(...)}, game-bus events
 * via the event's static {@code BUS}. HUD = the anchor-free LayeredDraw add (same form as
 * 51.x-55.x); tick = TickEvent.ClientTickEvent.Post (game bus); config via ConfigScreenHandler.
 */
public final class ElytraHud3ForgeClient {
    private ElytraHud3ForgeClient() {}

    public static void init(BusGroup modBus) {
        AddGuiOverlayLayersEvent.getBus(modBus).addListener(ElytraHud3ForgeClient::addGuiLayers);
        TickEvent.ClientTickEvent.Post.BUS.addListener(ElytraHud3ForgeClient::onClientTick);
        ModLoadingContext.get().registerExtensionPoint(ConfigScreenHandler.ConfigScreenFactory.class,
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

    private static void addGuiLayers(AddGuiOverlayLayersEvent event) {
        event.getLayeredDraw().add(
            @ID_HUD@,
            (graphics, partialTick) -> {
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

    private static void onClientTick(TickEvent.ClientTickEvent.Post event) {
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


def _eb7(ver):
    return core._vt(ver) >= (1, 21, 6)


def emit_entry(cog, ver, codegen):
    core.emit(cog, _ENTRY_EB7 if _eb7(ver) else _ENTRY_CLASSIC)


def emit_client(cog, ver, codegen):
    v = core._vt(ver)
    if v < (1, 20, 5):
        core.emit(cog, _CLIENT_IGUI)
        return
    if v < (1, 21):
        t = _CLIENT_LAYERED_106
    elif _eb7(ver):
        t = _CLIENT_ADD_EB7
    else:
        t = _CLIENT_ADD_CLASSIC
    id_expr = core.make_id(ver, "forge", "Common.MODID", '"hud"')
    core.emit(cog, core.sub(t, "@ID_HUD@", id_expr))
