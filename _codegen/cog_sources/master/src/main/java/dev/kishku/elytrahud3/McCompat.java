package dev.kishku.elytrahud3;

import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.resources.Identifier;

import java.lang.reflect.Method;

/**
 * Cross-version accessors for the handful of Minecraft APIs Mojang renamed between
 * MC 26.1 and 26.2. Resolved reflectively (and cached) so a single source -- and a single
 * jar -- works on both. Renames handled:
 *   GameRenderer.getMainCamera()  (26.1)  ->  mainCamera()        (26.2)
 *   Minecraft.setScreen(Screen)   (26.1)  ->  setScreenAndShow(Screen) (26.2)
 *   blit(RenderPipeline, ...) (up to 26.3) -> blit(GuiPipeline, ...) (26.4)
 */
final class McCompat {
    private McCompat() {}

    private static Method camMethod;
    private static Method setScreenMethod;
    private static Method blitMethod;
    private static Object guiTextured;

    /** Active render camera, or null. Takes the GameRenderer as Object to avoid compile binding. */
    static Object mainCamera(Object gameRenderer) {
        if (gameRenderer == null) {
            return null;
        }
        try {
            if (camMethod == null) {
                camMethod = findMethod(gameRenderer.getClass(), "getMainCamera", "mainCamera");
            }
            return camMethod != null ? camMethod.invoke(gameRenderer) : null;
        } catch (Throwable t) {
            return null;
        }
    }

    /**
     * Textured GUI blit. The pipeline argument changed type at 26.4 (RenderPipelines.GUI_TEXTURED, a
     * RenderPipeline, became GuiPipeline.TEXTURED), and blit() takes whichever type the running
     * Minecraft has, so both the pipeline and the call are resolved reflectively and cached.
     */
    static void blit(GuiGraphicsExtractor g, Identifier texture, int x, int y, float u, float v,
                     int width, int height, int texWidth, int texHeight, int color) {
        try {
            if (blitMethod == null) {
                resolveBlit();
            }
            if (blitMethod != null) {
                blitMethod.invoke(g, guiTextured, texture, x, y, u, v, width, height, texWidth, texHeight, color);
            }
        } catch (ReflectiveOperationException ignored) {
            // nothing sensible to draw with; the HUD simply skips this quad
        }
    }

    private static void resolveBlit() {
        String[][] holders = {
                {"net.minecraft.client.gui.GuiPipeline", "TEXTURED"},
                {"net.minecraft.client.renderer.pipeline.RenderPipelines", "GUI_TEXTURED"},
                {"net.minecraft.client.renderer.RenderPipelines", "GUI_TEXTURED"}};
        for (String[] holder : holders) {
            try {
                guiTextured = Class.forName(holder[0]).getField(holder[1]).get(null);
                break;
            } catch (ReflectiveOperationException ignored) {
                // try the next holder
            }
        }
        if (guiTextured == null) {
            return;
        }
        for (Method m : GuiGraphicsExtractor.class.getMethods()) {
            Class<?>[] p = m.getParameterTypes();
            if (m.getName().equals("blit") && p.length == 11 && p[0].isInstance(guiTextured)
                    && p[1] == Identifier.class && p[10] == int.class) {
                blitMethod = m;
                return;
            }
        }
    }

    static void setScreen(Minecraft mc, Screen screen) {
        try {
            if (setScreenMethod == null) {
                setScreenMethod = findMethod(Minecraft.class, "setScreen", "setScreenAndShow", Screen.class);
            }
            if (setScreenMethod != null) {
                setScreenMethod.invoke(mc, screen);
            }
        } catch (Throwable t) {
            // ignore
        }
    }

    private static Method findMethod(Class<?> owner, String name1, String name2, Class<?>... params) {
        for (String name : new String[]{name1, name2}) {
            try {
                Method m = owner.getMethod(name, params);
                m.setAccessible(true);
                return m;
            } catch (NoSuchMethodException ignored) {
                // try next candidate
            }
        }
        return null;
    }
}
