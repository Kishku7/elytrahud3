package dev.kishku.elytrahud3;

import net.minecraft.client.Minecraft;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.item.Items;

import java.lang.reflect.Method;

public class HudData {
    public double speed = 0.0;
    public double verticalSpeed = 0.0;
    public double durability = 1.0;
    public int currentDurability = 0;
    public double height = 0.0;
    public double yaw = 180.0;
    public double pitch = 0.0;
    public float roll = 0.0f;

    private Double prevYPosition = null;

    public void update() {
        Minecraft client = Common.client;
        if (client == null) {
            return;
        }
        var player = client.player;
        if (player == null) {
            return;
        }

        speed = player.getDeltaMovement().length() * 20.0;

        double currentYPosition = player.getY();
        if (prevYPosition != null) {
            verticalSpeed = (currentYPosition - prevYPosition) * 20.0;
        } else {
            verticalSpeed = 0.0;
        }
        prevYPosition = currentYPosition;

        height = player.getY();
        yaw = player.getYRot();
        pitch = player.getXRot();
        roll = getRoll(client);

        var chestSlot = player.getItemBySlot(EquipmentSlot.CHEST);
        if (!chestSlot.isEmpty() && chestSlot.getItem() == Items.ELYTRA) {
            int maxDamage = chestSlot.getMaxDamage();
            if (maxDamage > 0) {
                currentDurability = maxDamage - chestSlot.getDamageValue();
                durability = (double) currentDurability / maxDamage;
            } else {
                currentDurability = 0;
                durability = 1.0;
            }
        } else {
            durability = 0.0;
            currentDurability = 0;
        }
    }

    // --- "Do a Barrel Roll" soft-dependency roll readout (reflection; no hard link) ---
    private static boolean checked = false;
    // DABR Fabric API: Camera implements RollCamera -> float doABarrelRoll$getRoll()
    private static Method cameraRollMethod = null;
    // Fallback: some roll mods expose a plain getRoll() on the camera entity
    private static Method entityRollMethod = null;

    private static void resolveMethods(Minecraft client) {
        Object cam;
        try {
            cam = McCompat.mainCamera(client.gameRenderer);
        } catch (Throwable t) {
            cam = null;
        }
        Object ent;
        try {
            ent = client.getCameraEntity();
        } catch (Throwable t) {
            ent = null;
        }
        if (cam == null && ent == null) {
            return; // nothing to inspect yet; retry next tick
        }
        if (cam != null) {
            try {
                cameraRollMethod = cam.getClass().getMethod("doABarrelRoll$getRoll");
            } catch (Throwable t) {
                cameraRollMethod = null;
            }
        }
        if (ent != null) {
            try {
                entityRollMethod = ent.getClass().getMethod("getRoll");
            } catch (Throwable t) {
                entityRollMethod = null;
            }
        }
        checked = true;
    }

    public static float getRoll(Minecraft client) {
        if (!checked) {
            resolveMethods(client);
        }
        if (cameraRollMethod != null) {
            try {
                Object cam = McCompat.mainCamera(client.gameRenderer);
                if (cam != null) {
                    return (Float) cameraRollMethod.invoke(cam);
                }
            } catch (Throwable t) {
                // fall through
            }
        }
        if (entityRollMethod != null) {
            try {
                Object ent = client.getCameraEntity();
                if (ent != null) {
                    return (Float) entityRollMethod.invoke(ent);
                }
            } catch (Throwable t) {
                // fall through
            }
        }
        return 0.0f;
    }
}
