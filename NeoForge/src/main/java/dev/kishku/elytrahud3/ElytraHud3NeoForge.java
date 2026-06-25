package dev.kishku.elytrahud3;

import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.ModContainer;
import net.neoforged.fml.common.Mod;

@Mod(Common.MODID)
public class ElytraHud3NeoForge {
    public ElytraHud3NeoForge(ModContainer mod, IEventBus bus, Dist dist) {
        Common.CONFIG = ConfigManager.getConfig();
        if (dist.isClient()) {
            ElytraHud3NeoForgeClient.init(mod, bus);
        }
    }
}
