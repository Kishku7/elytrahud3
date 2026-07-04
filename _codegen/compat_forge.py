"""compat_forge.py -- Forge glue emitters (client + entry), SINGLE SOURCE.

Forge has no 26 twin (FG6 ceiling 1.21.8), so unlike fabric/neoforge these cannot derive from a
26 master. Instead the ONE Forge client (and ONE Forge entry) is assembled here from shared pieces
written ONCE + the genuinely per-era drift, driven by Cog `ver`. There are NOT four client sources:
the class body (`ensureClient`, the HUD render lambda body, the tick sampler body) is a single
shared definition; only the four things that actually differ across Forge's overlay-API eras are
per-era -- the imports, the javadoc, the `init` wiring, the registration call, and the tick-event
type. Each of those is a genuine loader-API difference (compile-verified), so it is Cog-selected.

Client eras (glue-API map, elytrahud3.md; EventBus boundary pinned by javap, mod-version-gates.md):
  igui        1.20-1.20.4 (Forge 46-49) : RegisterGuiOverlaysEvent/IGuiOverlay, string id,
                                           TickEvent.ClientTickEvent (phase END), classic bus,
                                           ModLoadingContext.get() extension point.
                                           (the 1.20.1 jar is also the NeoForge <=1.20.1 jar -- fork point)
  layered106  1.20.6 (Forge 50)         : AddGuiOverlayLayersEvent getLayeredDraw().addBelow(
                                           PRE_SLEEP_STACK, id, HOTBAR, layer); injected ctx; Post tick.
  addclassic  1.21-1.21.5 (Forge 52-55) : anchor-FREE getLayeredDraw().add(id, layer) -- the
                                           anchor-relative addBelow does not resolve at event time on
                                           52/55 (addBelow false-PASS trap; KEEP the anchor-free form);
                                           injected ctx, classic bus, Post tick.
  addeb7      1.21.6+ (Forge 56+, cell 1.21.8) : same add form; EventBus 7 BusGroup listeners.

Entry eras:
  classic   1.20/1.20.1 (46/47) : no-arg ctor + FMLJavaModLoadingContext.get() (undeprecated there).
  injected  1.20.4+ (49.2+)     : ctor(FMLJavaModLoadingContext) injection (the .get() statics are
                                  deprecated-for-removal from 49.2; the context IS a ModLoadingContext
                                  so the client glue reaches registerExtensionPoint through it).
ConfigManager (FMLPaths) + Common (holder) are version-invariant plain files in cog_sources/forge.
"""

import compat_core as core


# --------------------------------------------------------------------------- #
# shared client pieces (each written ONCE)
# --------------------------------------------------------------------------- #

_HEAD = """public final class ElytraHud3ForgeClient {
    private ElytraHud3ForgeClient() {}"""

_ENSURE_CLIENT = """    private static void ensureClient() {
        if (Common.client == null) {
            Common.client = Minecraft.getInstance();
        }
        if (Common.hudRenderer == null && Common.client != null) {
            Common.hudRenderer = new HudRenderer(Common.client);
        }
    }"""

# HUD gate + render, shared by every registration form (16-space indent, inside the layer lambda).
_RENDER_BODY = """                ElytraHudConfig config = Common.CONFIG;
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
                Common.hudRenderer.render(graphics, partialTick);"""

# tick sampler, shared by every tick handler (8-space indent, inside onClientTick).
_TICK_BODY = """        ElytraHudConfig config = Common.CONFIG;
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
        }"""


# --------------------------------------------------------------------------- #
# per-era drift (the ONLY things that differ across the overlay-API eras)
# --------------------------------------------------------------------------- #

def _client_era(ver):
    v = core._vt(ver)
    if v < (1, 20, 5):
        return "igui"
    if v < (1, 21):
        return "layered106"
    if v >= (1, 21, 10):
        return "addeb7bus"
    if v >= (1, 21, 6):
        return "addeb7"
    return "addclassic"


_IMPORTS = {
    "igui": """import net.minecraft.client.Minecraft;
import net.minecraftforge.client.ConfigScreenHandler;
import net.minecraftforge.client.event.RegisterGuiOverlaysEvent;
import net.minecraftforge.client.gui.overlay.VanillaGuiOverlay;
import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.event.TickEvent;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fml.ModLoadingContext;""",
    "layered106": """import net.minecraft.client.Minecraft;
import net.minecraft.resources.ResourceLocation;
import net.minecraftforge.client.ConfigScreenHandler;
import net.minecraftforge.client.event.AddGuiOverlayLayersEvent;
import net.minecraftforge.client.gui.overlay.ForgeLayeredDraw;
import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.event.TickEvent;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;""",
    "addclassic": """import net.minecraft.client.Minecraft;
import net.minecraft.resources.ResourceLocation;
import net.minecraftforge.client.ConfigScreenHandler;
import net.minecraftforge.client.event.AddGuiOverlayLayersEvent;
import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.event.TickEvent;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;""",
    "addeb7": """import net.minecraft.client.Minecraft;
import net.minecraft.resources.ResourceLocation;
import net.minecraftforge.client.ConfigScreenHandler;
import net.minecraftforge.client.event.AddGuiOverlayLayersEvent;
import net.minecraftforge.event.TickEvent;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;""",
}

_JAVADOC = {
    "igui": """/**
 * Forge 1.20/1.20.1 client bootstrap. HUD via {@link RegisterGuiOverlaysEvent} IGuiOverlay below
 * the hotbar; tick via {@link TickEvent.ClientTickEvent} (phase END); config screen via the
 * {@link ConfigScreenHandler.ConfigScreenFactory} extension point. Render delta is a float.
 * (The 1.20.1 jar also runs on NeoForge 1.20.1 -- the fork point -- which shares the
 * net.minecraftforge namespace and mods.toml format.)
 */""",
    "layered106": """/**
 * Forge 1.20.6 client bootstrap. Forge 1.20.6 (50.x) replaced RegisterGuiOverlaysEvent/IGuiOverlay
 * with the vanilla LayeredDraw system: add a {@link net.minecraft.client.gui.LayeredDraw.Layer}
 * below the hotbar via {@link AddGuiOverlayLayersEvent}#getLayeredDraw().addBelow(...). Tick is the
 * split {@link TickEvent.ClientTickEvent.Post}; config screen via {@link ConfigScreenHandler}.
 * LayeredDraw.Layer renders with a float partialTick (DeltaTracker is 1.21+).
 */""",
    "addclassic": """/**
 * Forge 1.21.1-1.21.5 (52.x-55.x) client bootstrap. HUD is a LayeredDraw layer attached with the
 * anchor-FREE 2-arg getLayeredDraw().add(newLayer, layer) -- the anchor-relative addBelow/addAbove
 * overloads fail at AddGuiOverlayLayersEvent time on 52.x/55.x ("Expected layer ... was not found
 * in stack minecraft:vanilla_root"), silently rendering nothing; the anchor-free add needs no
 * existing target and draws after the vanilla in-game layers, which is what we want (verified
 * against forge-1.21.1-52.1.14 and forge-1.21.5-55.1.10 ForgeLayeredDraw -- KEEP this form).
 * Tick is the split {@link TickEvent.ClientTickEvent.Post}; config screen via
 * {@link ConfigScreenHandler}. LayeredDraw.Layer renders with a float partialTick.
 */""",
    "addeb7": """/**
 * Forge 1.21.6+ (56.x+) client bootstrap. Forge 56 rewrote the event bus (EventBus 7.x BusGroup):
 * mod-bus events are subscribed via {@code Event.getBus(modBus).addListener(...)}, game-bus events
 * via the event's static {@code BUS}. HUD = the anchor-free LayeredDraw add (same form as
 * 51.x-55.x); tick = TickEvent.ClientTickEvent.Post (game bus); config via ConfigScreenHandler.
 */""",
}


_IMPORTS["addeb7bus"] = _IMPORTS["addeb7"]

_JAVADOC["addeb7bus"] = """/**
 * Forge 1.21.10+ (60.x+) client bootstrap. Same EventBus-7 model as 1.21.8, but Forge 60
 * deprecated-for-removal getBus(BusGroup) and exposes a static BUS per event, so the mod-bus
 * AddGuiOverlayLayersEvent listener registers via AddGuiOverlayLayersEvent.BUS (game-bus tick via
 * TickEvent.ClientTickEvent.Post.BUS as before). HUD = anchor-free LayeredDraw add; config via
 * ConfigScreenHandler. 1.21.11 also carries the ResourceLocation->Identifier rename.
 */"""


def _init(era):
    if era == "igui":
        return """    public static void init(IEventBus modBus) {
        modBus.addListener(ElytraHud3ForgeClient::registerOverlays);
        MinecraftForge.EVENT_BUS.addListener(ElytraHud3ForgeClient::onClientTick);
        ModLoadingContext.get().registerExtensionPoint(ConfigScreenHandler.ConfigScreenFactory.class,
            () -> new ConfigScreenHandler.ConfigScreenFactory(
                (mc, parent) -> new ElytraHudConfigScreen(parent)));
    }"""
    if era == "addeb7":
        return """    public static void init(FMLJavaModLoadingContext context) {
        // Injected context: BusGroup + extension point without the deprecated .get() statics.
        AddGuiOverlayLayersEvent.getBus(context.getModBusGroup()).addListener(ElytraHud3ForgeClient::addGuiLayers);
        TickEvent.ClientTickEvent.Post.BUS.addListener(ElytraHud3ForgeClient::onClientTick);
        context.registerExtensionPoint(ConfigScreenHandler.ConfigScreenFactory.class,
            () -> new ConfigScreenHandler.ConfigScreenFactory(
                (mc, parent) -> new ElytraHudConfigScreen(parent)));
    }"""
    if era == "addeb7bus":
        return """    public static void init(FMLJavaModLoadingContext context) {
        // Forge 60+ (1.21.10+): getBus(BusGroup) is deprecated-for-removal; each event exposes
        // a static BUS. Register the mod-bus overlay + game-bus tick on their BUS; the injected
        // context still supplies the config-screen extension point.
        AddGuiOverlayLayersEvent.BUS.addListener(ElytraHud3ForgeClient::addGuiLayers);
        TickEvent.ClientTickEvent.Post.BUS.addListener(ElytraHud3ForgeClient::onClientTick);
        context.registerExtensionPoint(ConfigScreenHandler.ConfigScreenFactory.class,
            () -> new ConfigScreenHandler.ConfigScreenFactory(
                (mc, parent) -> new ElytraHudConfigScreen(parent)));
    }"""
    # layered106 + addclassic share the injected-context classic-bus init
    return """    public static void init(FMLJavaModLoadingContext context) {
        // Injected context (49.2+ style): mod bus + extension point without the deprecated .get()s.
        context.getModEventBus().addListener(ElytraHud3ForgeClient::addGuiLayers);
        MinecraftForge.EVENT_BUS.addListener(ElytraHud3ForgeClient::onClientTick);
        context.registerExtensionPoint(ConfigScreenHandler.ConfigScreenFactory.class,
            () -> new ConfigScreenHandler.ConfigScreenFactory(
                (mc, parent) -> new ElytraHudConfigScreen(parent)));
    }"""


def _register(era, ver):
    if era == "igui":
        return ("""    private static void registerOverlays(RegisterGuiOverlaysEvent event) {
        event.registerBelow(VanillaGuiOverlay.HOTBAR.id(), "elytrahud3_hud",
            (gui, graphics, partialTick, screenWidth, screenHeight) -> {
"""
                + _RENDER_BODY + """
            });
    }""")
    id_expr = core.make_id(ver, "forge", "Common.MODID", '"hud"')
    if era == "layered106":
        return ("""    private static void addGuiLayers(AddGuiOverlayLayersEvent event) {
        event.getLayeredDraw().addBelow(
            ForgeLayeredDraw.PRE_SLEEP_STACK,
            """ + id_expr + """,
            ForgeLayeredDraw.HOTBAR,
            (graphics, partialTick) -> {
"""
                + _RENDER_BODY + """
            });
    }""")
    # addclassic + addeb7 share the anchor-free add register
    return ("""    private static void addGuiLayers(AddGuiOverlayLayersEvent event) {
        event.getLayeredDraw().add(
            """ + id_expr + """,
            (graphics, partialTick) -> {
"""
            + _RENDER_BODY + """
            });
    }""")


def _tick(era):
    if era == "igui":
        return ("""    private static void onClientTick(TickEvent.ClientTickEvent event) {
        if (event.phase != TickEvent.Phase.END) {
            return;
        }
"""
                + _TICK_BODY + """
    }""")
    return ("""    private static void onClientTick(TickEvent.ClientTickEvent.Post event) {
"""
            + _TICK_BODY + """
    }""")


def emit_client(cog, ver, codegen):
    era = _client_era(ver)
    # The id-import must follow the mojmap ResourceLocation->Identifier rename (1.21.11+);
    # every era except igui (string ids) references an id, so swap in the era-correct import.
    imports = _IMPORTS[era]
    if era != "igui":
        imports = imports.replace(
            "import net.minecraft.resources.ResourceLocation;", core.id_import(ver))
    parts = [
        "package dev.kishku.elytrahud3;",
        "",
        imports,
        "",
        _JAVADOC[era],
        _HEAD,
        "",
        _init(era),
        "",
        _ENSURE_CLIENT,
        "",
        _register(era, ver),
        "",
        _tick(era),
        "}",
    ]
    core.emit(cog, "\n".join(parts))


# --------------------------------------------------------------------------- #
# entry -- single source (classic no-arg ctor vs injected-context ctor)
# --------------------------------------------------------------------------- #

def _injected(ver):
    # ctor context injection exists from Forge 49.2 (MC 1.20.4); the forge cells below that are
    # 1.20 (46) / 1.20.1 (47) where the .get() statics are the undeprecated norm. The orphan
    # Forge 51 line (MC 1.21, no injection) has NO cell -- do not add one without rechecking.
    return core._vt(ver) >= (1, 20, 4)


def emit_entry(cog, ver, codegen):
    if _injected(ver):
        imports = """import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;
import net.minecraftforge.fml.loading.FMLEnvironment;"""
        ctor = """    // Forge 49.2+ injects the context into the mod ctor and deprecates-for-removal the .get()
    // statics; FMLJavaModLoadingContext extends ModLoadingContext (javap-verified 50/52/55/58),
    // so the client glue reaches registerExtensionPoint through this same instance.
    public ElytraHud3Forge(FMLJavaModLoadingContext context) {
        Common.CONFIG = ConfigManager.getConfig();
        if (FMLEnvironment.dist == Dist.CLIENT) {
            ElytraHud3ForgeClient.init(context);
        }
    }"""
    else:
        imports = """import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;
import net.minecraftforge.fml.loading.FMLEnvironment;"""
        ctor = """    public ElytraHud3Forge() {
        Common.CONFIG = ConfigManager.getConfig();
        if (FMLEnvironment.dist == Dist.CLIENT) {
            IEventBus modBus = FMLJavaModLoadingContext.get().getModEventBus();
            ElytraHud3ForgeClient.init(modBus);
        }
    }"""
    parts = [
        "package dev.kishku.elytrahud3;",
        "",
        imports,
        "",
        "@Mod(Common.MODID)",
        "public class ElytraHud3Forge {",
        ctor,
        "}",
    ]
    core.emit(cog, "\n".join(parts))
