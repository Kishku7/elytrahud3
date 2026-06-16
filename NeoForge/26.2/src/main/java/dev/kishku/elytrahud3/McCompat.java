package dev.kishku.elytrahud3;

import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.screens.Screen;

import java.lang.reflect.Method;

/**
 * Cross-version accessors for the handful of Minecraft APIs Mojang renamed between
 * MC 26.1 and 26.2. Resolved reflectively (and cached) so a single source — and a single
 * jar — works on both. Renames handled:
 *   GameRenderer.getMainCamera()  (26.1)  ->  mainCamera()        (26.2)
 *   Minecraft.setScreen(Screen)   (26.1)  ->  setScreenAndShow(Screen) (26.2)
 */
final class McCompat {
    private McCompat() {}

    private static Method camMethod;
    private static Method setScreenMethod;

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
