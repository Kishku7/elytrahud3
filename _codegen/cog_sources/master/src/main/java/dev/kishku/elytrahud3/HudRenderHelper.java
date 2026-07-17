package dev.kishku.elytrahud3;

import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.renderer.RenderPipelines;
import net.minecraft.resources.Identifier;

public final class HudRenderHelper {
    private static final Identifier WIDGETS_TEXTURE =
        Identifier.fromNamespaceAndPath(Common.MODID, "textures/hud_widgets.png");

    private HudRenderHelper() {}

    public static void renderMeter(GuiGraphicsExtractor graphics, int centerX, int centerY, float angleDegrees) {
        float angleRad = (float) Math.toRadians(angleDegrees);
        graphics.pose().pushMatrix();
        graphics.pose().translate((float) centerX, (float) centerY);
        graphics.pose().rotate(angleRad);
        graphics.pose().translate((float) -centerX, (float) -centerY);
        graphics.blit(RenderPipelines.GUI_TEXTURED, WIDGETS_TEXTURE, centerX - 1, centerY - 42, 215f, 105f, 2, 42, 256, 256, -1);
        graphics.pose().popMatrix();
    }

    public static void renderVerticalMeter(GuiGraphicsExtractor graphics, int centerX, int centerY, float angleDegrees) {
        float angleRad = (float) Math.toRadians(angleDegrees);
        graphics.pose().pushMatrix();
        graphics.pose().translate((float) centerX, (float) centerY);
        graphics.pose().rotate(angleRad);
        graphics.pose().translate((float) -centerX, (float) -centerY);
        graphics.blit(RenderPipelines.GUI_TEXTURED, WIDGETS_TEXTURE, centerX - 1, centerY - 18, 215f, 147f, 2, 18, 256, 256, -1);
        graphics.pose().popMatrix();
    }

    public static void renderHorizon(GuiGraphicsExtractor graphics, int centerX, int centerY, float angleDegrees) {
        float angleRad = (float) Math.toRadians(angleDegrees);
        graphics.pose().pushMatrix();
        graphics.pose().translate((float) centerX, (float) centerY);
        graphics.pose().rotate(angleRad);
        graphics.pose().translate((float) -centerX, (float) -centerY);
        graphics.blit(RenderPipelines.GUI_TEXTURED, WIDGETS_TEXTURE, centerX - 13, centerY - 2, 215f, 176f, 26, 3, 256, 256, -1);
        graphics.pose().popMatrix();
    }

    public static void renderDoubleMeterNeedle1(GuiGraphicsExtractor graphics, int centerX, int centerY, float angleDegrees) {
        float angleRad = (float) Math.toRadians(angleDegrees);
        graphics.pose().pushMatrix();
        graphics.pose().translate((float) centerX, (float) centerY);
        graphics.pose().rotate(angleRad);
        graphics.pose().translate((float) -centerX, (float) -centerY);
        graphics.blit(RenderPipelines.GUI_TEXTURED, WIDGETS_TEXTURE, centerX - 1, centerY - 18, 215f, 147f, 2, 18, 256, 256, -1);
        graphics.pose().popMatrix();
    }

    public static void renderDoubleMeterNeedle2(GuiGraphicsExtractor graphics, int centerX, int centerY, float angleDegrees) {
        float angleRad = (float) Math.toRadians(angleDegrees);
        graphics.pose().pushMatrix();
        graphics.pose().translate((float) centerX, (float) centerY);
        graphics.pose().rotate(angleRad);
        graphics.pose().translate((float) -centerX, (float) -centerY);
        graphics.blit(RenderPipelines.GUI_TEXTURED, WIDGETS_TEXTURE, centerX - 1, centerY - 42, 215f, 105f, 2, 42, 256, 256, -1);
        graphics.pose().popMatrix();
    }
}
