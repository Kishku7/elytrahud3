"""compat_core.py -- loader-agnostic, version-keyed drift brain for the SHARED Java files.

DESIGN (EH3-specific, decided Stage 1 2026-07-03): the plain 26-era twins in _codegen/cog_sources/master/
are the MASTERS. Pre-26 forms are DERIVED from the master text by exact-anchored line transforms
(every transform asserts its anchor exists, so master drift breaks the build loudly instead of
silently). The 26 cells srcDir _codegen/cog_sources/master directly and never run cog; pre-26 cells build
from cog-materialized gen/ trees (scripts/cog-gen.ps1).

Era axes (MC 1.20 - 1.21.11 pre-26 cells; javap-verified, see MATRIX.md "Era model"):
  gfx        : GuiGraphicsExtractor + .text()   @26   | GuiGraphics + .drawString()  pre-26
  blit       : RenderPipelines.GUI_TEXTURED+tint @1.21.6 | RenderType::guiTextured @1.21.2 | legacy
  pose       : 2D Matrix3x2fStack @1.21.6        | 3D PoseStack + Axis.ZP below
  id         : Identifier @1.21.11 (mojmap rename) | ResourceLocation.fromNamespaceAndPath @1.21
               (Forge backported the factory at 1.20.4/49.2 and deprecated the ctor there)
               | new ResourceLocation below
  tick delta : DeltaTracker @1.21               | float partialTick below
  McCompat   : 26 = reflection try-both-names (mojmap runtime, bridges the 26.1->26.2 renames);
               pre-26 = DIRECT calls (getMainCamera/setScreen exist plainly 1.20-1.21.11).
               NEVER reflection-by-mojmap-name on pre-26 Fabric: the runtime is INTERMEDIARY,
               name lookups silently miss (the BvCompat lesson).
"""

import io
import os


def _vt(ver):
    return tuple(int(x) for x in ver.split("-")[0].split("."))


def is26(ver):
    return _vt(ver) >= (26,)


def has_delta_tracker(ver):
    return _vt(ver) >= (1, 21)


def renamed_identifier(ver):
    # MOJMAP ResourceLocation->Identifier rename lands at MC 1.21.11 (javap/runtime-verified:
    # NeoForge 21.10.64 VanillaGuiLayers.HOTBAR is still ResourceLocation-typed -> a jar
    # compiled at 1.21.11 NoSuchFieldErrors on 1.21.9/1.21.10 mojmap runtimes). Fabric pre-26
    # spans the rename via intermediary, so only mojmap-runtime cells (NeoForge) below
    # 1.21.11 need the ResourceLocation flavor. True for the whole 26 line as well.
    return _vt(ver) >= (1, 21, 11)


def nf_ctor_dist(ver):
    # NeoForge @Mod ctor era: the injected-Dist 3-arg ctor (IEventBus, ModContainer, Dist)
    # is used from the 1.21.9 line (present on 21.9/21.10 per M1; FMLEnvironment.dist is
    # GONE at 21.11 so 1.21.9+ all take the injected Dist). Decoupled from the Identifier
    # rename, which lands later (1.21.11).
    return _vt(ver) >= (1, 21, 9)


def blit_era(ver):
    v = _vt(ver)
    if v >= (1, 21, 6):
        return "pipeline"
    if v >= (1, 21, 2):
        return "rendertype"
    return "legacy"


def pose2d(ver):
    return _vt(ver) >= (1, 21, 6)


def has_rl_factory(ver, loader=None):
    # ResourceLocation.fromNamespaceAndPath exists from 1.21 in vanilla. Forge backported the
    # factories at 1.20.4 (49.2+) AND deprecated-for-removal the two-arg ctor, so forge targets
    # switch a line earlier (zero -Xlint:all deprecation warnings). NeoForge/Fabric 1.20.x keep
    # the undeprecated ctor.
    if loader == "forge" and _vt(ver) >= (1, 20, 4):
        return True
    return _vt(ver) >= (1, 21)


def repo_root(codegen):
    return os.path.dirname(os.path.abspath(codegen))


def read_twin(codegen, rel):
    path = os.path.join(repo_root(codegen), rel.replace("/", os.sep))
    with io.open(path, "r", encoding="ascii", newline=None) as f:
        return f.read()


def sub(text, old, new, count=None, optional=False):
    """Anchored replace: fails loudly if the anchor is missing or the count is unexpected."""
    n = text.count(old)
    if n == 0:
        if optional:
            return text
        raise AssertionError("anchor missing: %r" % old)
    if count is not None and n != count:
        raise AssertionError("expected %d occurrence(s) of %r, found %d" % (count, old, n))
    return text.replace(old, new)


def emit(cog, text):
    for ln in text.rstrip("\n").split("\n"):
        cog.outl(ln.rstrip())


def make_id(ver, loader, ns_expr, path_expr):
    """Java expression constructing an id from (namespace, path) expressions, era+loader-correct."""
    idt = "Identifier" if renamed_identifier(ver) else "ResourceLocation"
    if renamed_identifier(ver) or has_rl_factory(ver, loader):
        return "%s.fromNamespaceAndPath(%s, %s)" % (idt, ns_expr, path_expr)
    return "new ResourceLocation(%s, %s)" % (ns_expr, path_expr)


def id_import(ver):
    return "import net.minecraft.resources.%s;" % ("Identifier" if renamed_identifier(ver) else "ResourceLocation")


# ---------------------------------------------------------------------------
# shared file: HudRenderer.java (master: _codegen/cog_sources/master twin)
# ---------------------------------------------------------------------------

_POSE3D_IMPORTS = "import com.mojang.blaze3d.vertex.PoseStack;\nimport com.mojang.math.Axis;\n"

_COMPASS_2D = (
    "        var matrices = graphics.pose();\n"
    "\n"
    "        matrices.pushMatrix();\n"
    "        matrices.translate((float) centerX, (float) centerY);\n"
    "        matrices.rotate(angleRadians);\n"
    "        matrices.translate((float) -centerX, (float) -centerY);"
)

_COMPASS_3D = (
    "        PoseStack pose = graphics.pose();\n"
    "\n"
    "        pose.pushPose();\n"
    "        pose.translate((float) centerX, (float) centerY, 0.0f);\n"
    "        pose.mulPose(Axis.ZP.rotation(angleRadians));\n"
    "        pose.translate((float) -centerX, (float) -centerY, 0.0f);"
)

_HELPER_2D = (
    "        graphics.pose().pushMatrix();\n"
    "        graphics.pose().translate((float) centerX, (float) centerY);\n"
    "        graphics.pose().rotate(angleRad);\n"
    "        graphics.pose().translate((float) -centerX, (float) -centerY);"
)

_HELPER_3D = (
    "        PoseStack pose = graphics.pose();\n"
    "        pose.pushPose();\n"
    "        pose.translate((float) centerX, (float) centerY, 0.0f);\n"
    "        pose.mulPose(Axis.ZP.rotation(angleRad));\n"
    "        pose.translate((float) -centerX, (float) -centerY, 0.0f);"
)


def _apply_gfx_text(t, ver):
    if not is26(ver):
        t = sub(t, "GuiGraphicsExtractor", "GuiGraphics")
        # HudRenderHelper draws no text; HudRenderer does. Optional keeps one helper for both.
        t = sub(t, "graphics.text(", "graphics.drawString(", optional=True)
    return t


def _apply_blit(t, ver):
    era = blit_era(ver)
    if era == "pipeline":
        return t
    if era == "rendertype":
        t = sub(t, "import net.minecraft.client.renderer.RenderPipelines;",
                "import net.minecraft.client.renderer.RenderType;", count=1)
        t = sub(t, "graphics.blit(RenderPipelines.GUI_TEXTURED, ",
                "graphics.blit(RenderType::guiTextured, ")
    else:
        t = sub(t, "import net.minecraft.client.renderer.RenderPipelines;\n", "", count=1)
        t = sub(t, "graphics.blit(RenderPipelines.GUI_TEXTURED, ", "graphics.blit(")
    t = sub(t, ", 256, 256, -1);", ", 256, 256);")
    return t


def _apply_id(t, ver, loader):
    if renamed_identifier(ver):
        return t
    if has_rl_factory(ver, loader):
        return sub(t, "Identifier", "ResourceLocation")
    t = sub(t, "import net.minecraft.resources.Identifier;",
            "import net.minecraft.resources.ResourceLocation;", count=1)
    t = sub(t, "private static final Identifier WIDGETS_TEXTURE",
            "private static final ResourceLocation WIDGETS_TEXTURE", count=1)
    t = sub(t, 'Identifier.fromNamespaceAndPath(Common.MODID, "textures/hud_widgets.png")',
            'new ResourceLocation(Common.MODID, "textures/hud_widgets.png")', count=1)
    return t


def emit_hud_renderer(cog, loader, ver, codegen):
    t = read_twin(codegen, "_codegen/cog_sources/master/src/main/java/dev/kishku/elytrahud3/HudRenderer.java")
    t = _apply_gfx_text(t, ver)
    t = _apply_blit(t, ver)
    t = _apply_id(t, ver, loader)
    if not has_delta_tracker(ver):
        t = sub(t, "import net.minecraft.client.DeltaTracker;\n", "", count=1)
        t = sub(t, "DeltaTracker tickDelta", "float tickDelta", count=1)
        t = sub(t, "(double) tickDelta.getGameTimeDeltaTicks()", "(double) tickDelta", count=1)
    if not pose2d(ver):
        t = sub(t, "import net.minecraft.client.Minecraft;",
                _POSE3D_IMPORTS + "import net.minecraft.client.Minecraft;", count=1)
        t = sub(t, _COMPASS_2D, _COMPASS_3D, count=1)
        t = sub(t, "        matrices.popMatrix();", "        pose.popPose();", count=1)
    emit(cog, t)


def emit_hud_render_helper(cog, loader, ver, codegen):
    t = read_twin(codegen, "_codegen/cog_sources/master/src/main/java/dev/kishku/elytrahud3/HudRenderHelper.java")
    t = _apply_gfx_text(t, ver)
    t = _apply_blit(t, ver)
    t = _apply_id(t, ver, loader)
    if not pose2d(ver):
        t = sub(t, "import net.minecraft.client.gui.",
                _POSE3D_IMPORTS + "import net.minecraft.client.gui.", count=1)
        t = sub(t, _HELPER_2D, _HELPER_3D, count=5)
        t = sub(t, "        graphics.pose().popMatrix();", "        pose.popPose();", count=5)
    emit(cog, t)


# ---------------------------------------------------------------------------
# shared file: McCompat.java -- 26 = reflection twin; pre-26 = DIRECT calls
# ---------------------------------------------------------------------------

_MCCOMPAT_DIRECT = """package dev.kishku.elytrahud3;

import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.client.renderer.GameRenderer;

/**
 * Pre-26 form of the cross-version accessor shim: on MC 1.20 - 1.21.11 the two APIs the 26 line
 * bridges reflectively (GameRenderer.getMainCamera(), Minecraft.setScreen(Screen)) exist plainly,
 * so this emits DIRECT calls. Reflection-by-mojmap-name is FORBIDDEN here: pre-26 Fabric runs
 * intermediary at runtime, where mojmap name lookups silently return null.
 */
final class McCompat {
    private McCompat() {}

    /** Active render camera, or null. Takes the GameRenderer as Object so callers stay era-neutral. */
    static Object mainCamera(Object gameRenderer) {
        if (gameRenderer == null) {
            return null;
        }
        return ((GameRenderer) gameRenderer).getMainCamera();
    }

    static void setScreen(Minecraft mc, Screen screen) {
        mc.setScreen(screen);
    }
}
"""


def emit_mc_compat(cog, loader, ver, codegen):
    if is26(ver):
        emit(cog, read_twin(codegen, "_codegen/cog_sources/master/src/main/java/dev/kishku/elytrahud3/McCompat.java"))
    else:
        emit(cog, _MCCOMPAT_DIRECT)
