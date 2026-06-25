package dev.kishku.elytrahud3;

import net.minecraft.client.DeltaTracker;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.renderer.RenderPipelines;
import net.minecraft.resources.Identifier;
import net.minecraft.util.Mth;

public class HudRenderer {
    private static final Identifier WIDGETS_TEXTURE =
        Identifier.fromNamespaceAndPath(Common.MODID, "textures/hud_widgets.png");

    private final Minecraft client;

    private double displayedSpeed = 0.0;
    private double displayedDur = 1.0;
    private double displayedHeight = 0.0;
    private double displayedVertical = 0.0;
    private double displayedYaw = 180.0;
    private double displayedPitch = 0.0;
    private float displayedRoll = 0.0f;

    public HudRenderer(Minecraft client) {
        this.client = client;
    }

    public void render(GuiGraphicsExtractor graphics, DeltaTracker tickDelta) {
        ElytraHudConfig config = Common.CONFIG;
        if (config == null || !config.modEnabled) {
            return;
        }
        HudData hudData = Common.hudData;

        int rateX = 10;
        int durX = 10;
        int vertX = 10;

        displayedSpeed = Mth.lerp((double) tickDelta.getGameTimeDeltaTicks(), displayedSpeed, hudData.speed);
        displayedDur = hudData.durability;
        displayedHeight = hudData.height;
        displayedVertical = hudData.verticalSpeed;
        displayedYaw = hudData.yaw * -1.0 + 180.0;
        displayedPitch = hudData.pitch;
        displayedRoll = hudData.roll;

        boolean imperial = config.imperialUnits;
        int intAirspeed = (int) Math.round(displayedSpeed * (imperial ? 2.23694 : 3.6));
        int intDur = hudData.currentDurability;
        int intHeight = (int) Math.round(displayedHeight * (imperial ? 3.28084 : 1.0));
        int intVertical = (int) Math.round(displayedVertical * (imperial ? 3.28084 : 1.0));
        int intPitch = (int) Math.round(displayedPitch);

        int defaultY = config.renderValues ? 15 : 10;
        int scaledWidth = client.getWindow().getGuiScaledWidth();
        int scaledHeight = client.getWindow().getGuiScaledHeight();

        if (config.renderAirspeed) {
            rateX += 102;
            durX += 102;
            int speedometerX = 10;
            int speedometerY = 100 + defaultY;
            int yPos = scaledHeight - speedometerY;
            double speedToRender = Math.min(displayedSpeed, 80.0);
            renderMeter(graphics, speedometerX + 50, yPos + 50, (float) (speedToRender * 4.5), intAirspeed, config);
        }

        if (config.renderHorizon) {
            durX += 52;
            int rateY = 50 + defaultY;
            int yPos = scaledHeight - rateY;
            int intPitchY = Math.max(-44, Math.min(44, intPitch / 2));
            renderHorizon(graphics, rateX + 25, yPos + 25, displayedRoll, intPitch, config, intPitchY);
        }

        if (config.renderDurability) {
            int durY = 50 + defaultY;
            int topPoint = scaledHeight - durY + 2;
            int bottomPoint = topPoint + 44;
            int yCoordinate = (int) (topPoint + (1.0 - displayedDur) * (bottomPoint - topPoint));
            renderBar(graphics, durX, scaledHeight - durY, yCoordinate, intDur, config);
        }

        if (config.renderAltitude) {
            vertX += 102;
            int altitudeX = 10 + 100;
            int altitudeY = 100 + defaultY;
            int xPos = scaledWidth - altitudeX;
            int yPos = scaledHeight - altitudeY;
            renderDoubleMeter(graphics, xPos + 50, yPos + 50,
                (float) (displayedHeight * 0.36),
                (float) (displayedHeight * 3.6),
                intHeight, config);
        }

        if (config.renderVertical) {
            int vertSize = 50;
            vertX += vertSize;
            int vertY = vertSize + defaultY;
            int xPos = scaledWidth - vertX;
            int yPos = scaledHeight - vertY;
            double verticalToRender = Math.max(-5.0, Math.min(5.0, displayedVertical));
            renderVerticalMeter(graphics, xPos + 25, yPos + 25,
                (float) ((verticalToRender + 5.0) * 25.0 + 145.0) % 360.0f,
                intVertical, config);
        }

        if (config.renderCompass) {
            int compassX = 10;
            int compassY = 15;
            renderCompass(graphics, compassX + 50, compassY + 50, (float) Math.toRadians(displayedYaw));
            int intYaw = (((int) Math.round(hudData.yaw) + 180) % 360 + 360) % 360;
            graphics.text(client.font, String.format("%3d°", intYaw), compassX + 37, compassY - 6, -1);
        }
    }

    private void renderMeter(GuiGraphicsExtractor graphics, int centerX, int centerY, float angleDegrees, int valueInt, ElytraHudConfig config) {
        int defaultY = config.renderValues ? 15 : 10;
        int scaledHeight = client.getWindow().getGuiScaledHeight();
        int yPos = scaledHeight - (100 + defaultY);

        graphics.blit(RenderPipelines.GUI_TEXTURED, WIDGETS_TEXTURE, centerX - 50, yPos, 0f, 0f, 100, 100, 256, 256, -1);

        HudRenderHelper.renderMeter(graphics, centerX, centerY, angleDegrees);

        graphics.blit(RenderPipelines.GUI_TEXTURED, WIDGETS_TEXTURE, centerX - 5, centerY - 5, 215f, 73f, 10, 10, 256, 256, -1);

        if (config.renderTitles) {
            graphics.blit(RenderPipelines.GUI_TEXTURED, WIDGETS_TEXTURE, centerX - 17, yPos - 10, 215f, 0f, 34, 9, 256, 256, -1);
        }

        if (config.renderValues) {
            int valueX = centerX - 10;
            int valueY = yPos + 101;
            graphics.blit(RenderPipelines.GUI_TEXTURED, WIDGETS_TEXTURE, valueX, valueY, 215f, 165f, 21, 11, 256, 256, -1);
            graphics.text(client.font, String.format("%3d", valueInt), valueX + 2, valueY + 2, -1);
        }
    }

    private void renderVerticalMeter(GuiGraphicsExtractor graphics, int centerX, int centerY, float angleDegrees, int valueInt, ElytraHudConfig config) {
        int defaultY = config.renderValues ? 15 : 10;
        int scaledHeight = client.getWindow().getGuiScaledHeight();
        int yPos = scaledHeight - (50 + defaultY);

        graphics.blit(RenderPipelines.GUI_TEXTURED, WIDGETS_TEXTURE, centerX - 25, yPos, 100f, 50f, 50, 50, 256, 256, -1);

        HudRenderHelper.renderVerticalMeter(graphics, centerX, centerY, angleDegrees);

        graphics.blit(RenderPipelines.GUI_TEXTURED, WIDGETS_TEXTURE, centerX - 3, centerY - 3, 215f, 99f, 6, 6, 256, 256, -1);

        if (config.renderTitles) {
            graphics.blit(RenderPipelines.GUI_TEXTURED, WIDGETS_TEXTURE, centerX - 14, yPos - 10, 215f, 27f, 28, 9, 256, 256, -1);
        }

        if (config.renderValues) {
            int valueX = centerX - 10;
            int valueY = yPos + 51;
            graphics.blit(RenderPipelines.GUI_TEXTURED, WIDGETS_TEXTURE, valueX, valueY, 215f, 165f, 21, 11, 256, 256, -1);
            graphics.text(client.font, String.format("%3d", valueInt), valueX + 2, valueY + 2, -1);
        }
    }

    private void renderHorizon(GuiGraphicsExtractor graphics, int centerX, int centerY, float angleRoll, int valueInt, ElytraHudConfig config, int pitchOffset) {
        int defaultY = config.renderValues ? 15 : 10;
        int scaledHeight = client.getWindow().getGuiScaledHeight();
        int yPos = scaledHeight - (50 + defaultY);

        int horizonY = 41 + pitchOffset;
        graphics.blit(RenderPipelines.GUI_TEXTURED, WIDGETS_TEXTURE, centerX - 25, yPos, 100f, 100f, 50, 50, 256, 256, -1);

        int[][] horizonList = {
            {1, 10, 20}, {1, 16, 17}, {1, 22, 14}, {1, 24, 13}, {1, 26, 12},
            {1, 30, 10}, {1, 32, 9}, {2, 34, 8}, {1, 36, 7}, {1, 38, 6},
            {3, 40, 5}, {3, 42, 4}, {5, 44, 3}
        };

        int horizonX = 0;
        for (int[] row : horizonList) {
            graphics.blit(RenderPipelines.GUI_TEXTURED, WIDGETS_TEXTURE, centerX - 22 + horizonX, yPos + 3 - 3 + row[2], 170f + horizonX, (float) (horizonY + row[2]), row[0], row[1], 256, 256, -1);
            horizonX += row[0];
        }
        for (int i = horizonList.length - 1; i >= 0; i--) {
            int[] row = horizonList[i];
            graphics.blit(RenderPipelines.GUI_TEXTURED, WIDGETS_TEXTURE, centerX - 22 + horizonX, yPos + 3 - 3 + row[2], 170f + horizonX, (float) (horizonY + row[2]), row[0], row[1], 256, 256, -1);
            horizonX += row[0];
        }

        HudRenderHelper.renderHorizon(graphics, centerX, centerY, angleRoll);

        if (config.renderTitles) {
            graphics.blit(RenderPipelines.GUI_TEXTURED, WIDGETS_TEXTURE, centerX - 15, yPos - 10, 215f, 179f, 29, 9, 256, 256, -1);
        }

        if (config.renderValues) {
            int valueX = centerX - 10;
            int valueY = yPos + 51;
            graphics.blit(RenderPipelines.GUI_TEXTURED, WIDGETS_TEXTURE, valueX, valueY, 215f, 165f, 21, 11, 256, 256, -1);
            graphics.text(client.font, String.format("%3d", valueInt), valueX + 2, valueY + 2, -1);
        }
    }

    private void renderBar(GuiGraphicsExtractor graphics, int x, int yPos, int yCoordinate, int valueInt, ElytraHudConfig config) {
        graphics.blit(RenderPipelines.GUI_TEXTURED, WIDGETS_TEXTURE, x, yPos, 150f, 0f, 15, 50, 256, 256, -1);
        graphics.blit(RenderPipelines.GUI_TEXTURED, WIDGETS_TEXTURE, x + 4, yCoordinate, 215f, 56f, 4, 3, 256, 256, -1);

        if (config.renderTitles) {
            graphics.blit(RenderPipelines.GUI_TEXTURED, WIDGETS_TEXTURE, x, yPos - 10, 215f, 18f, 15, 9, 256, 256, -1);
        }

        if (config.renderValues) {
            int valueX = x - 3;
            int valueY = yPos + 51;
            graphics.blit(RenderPipelines.GUI_TEXTURED, WIDGETS_TEXTURE, valueX, valueY, 215f, 165f, 21, 11, 256, 256, -1);
            graphics.text(client.font, String.format("%3d", valueInt), valueX + 2, valueY + 2, -1);
        }
    }

    private void renderDoubleMeter(GuiGraphicsExtractor graphics, int centerX, int centerY, float angle1, float angle2, int valueInt, ElytraHudConfig config) {
        int defaultY = config.renderValues ? 15 : 10;
        int scaledHeight = client.getWindow().getGuiScaledHeight();
        int yPos = scaledHeight - (100 + defaultY);

        graphics.blit(RenderPipelines.GUI_TEXTURED, WIDGETS_TEXTURE, centerX - 50, yPos, 0f, 100f, 100, 100, 256, 256, -1);

        HudRenderHelper.renderDoubleMeterNeedle1(graphics, centerX, centerY, angle1);
        HudRenderHelper.renderDoubleMeterNeedle2(graphics, centerX, centerY, angle2);

        graphics.blit(RenderPipelines.GUI_TEXTURED, WIDGETS_TEXTURE, centerX - 5, centerY - 5, 215f, 83f, 10, 10, 256, 256, -1);

        if (config.renderTitles) {
            graphics.blit(RenderPipelines.GUI_TEXTURED, WIDGETS_TEXTURE, centerX - 16, yPos - 10, 215f, 36f, 32, 9, 256, 256, -1);
        }

        if (config.renderValues) {
            int valueX = centerX - 10;
            int valueY = yPos + 101;
            graphics.blit(RenderPipelines.GUI_TEXTURED, WIDGETS_TEXTURE, valueX, valueY, 215f, 165f, 21, 11, 256, 256, -1);
            graphics.text(client.font, String.format("%3d", valueInt), valueX + 2, valueY + 2, -1);
        }
    }

    private void renderCompass(GuiGraphicsExtractor graphics, int centerX, int centerY, float angleRadians) {
        var matrices = graphics.pose();

        matrices.pushMatrix();
        matrices.translate((float) centerX, (float) centerY);
        matrices.rotate(angleRadians);
        matrices.translate((float) -centerX, (float) -centerY);
        graphics.blit(RenderPipelines.GUI_TEXTURED, WIDGETS_TEXTURE, centerX - 50, centerY - 50, 100f, 150f, 100, 100, 256, 256, -1);
        matrices.popMatrix();

        graphics.blit(RenderPipelines.GUI_TEXTURED, WIDGETS_TEXTURE, centerX - 5, centerY - 47, 215f, 59f, 6, 5, 256, 256, -1);
        graphics.blit(RenderPipelines.GUI_TEXTURED, WIDGETS_TEXTURE, centerX - 5, centerY - 6, 215f, 64f, 10, 9, 256, 256, -1);
        graphics.blit(RenderPipelines.GUI_TEXTURED, WIDGETS_TEXTURE, centerX - 15, centerY - 58, 215f, 45f, 26, 11, 256, 256, -1);
    }
}
