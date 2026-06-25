package dev.kishku.elytrahud3;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import net.neoforged.fml.loading.FMLPaths;

import java.nio.file.Files;
import java.nio.file.Path;

public final class ConfigManager {
    private static final Gson GSON = new GsonBuilder().setPrettyPrinting().create();
    private static final Path CONFIG_PATH = FMLPaths.CONFIGDIR.get().resolve("elytrahud3.json");

    private static ElytraHudConfig config = null;

    private ConfigManager() {}

    public static ElytraHudConfig getConfig() {
        if (config == null) {
            config = load();
        }
        return config;
    }

    public static void save() {
        try {
            Files.writeString(CONFIG_PATH, GSON.toJson(getConfig()));
        } catch (Exception e) {
            // ignore write failures
        }
    }

    private static ElytraHudConfig load() {
        try {
            if (Files.exists(CONFIG_PATH)) {
                ElytraHudConfig loaded = GSON.fromJson(Files.readString(CONFIG_PATH), ElytraHudConfig.class);
                if (loaded != null) {
                    return loaded;
                }
            }
        } catch (Exception e) {
            // fall through to defaults
        }
        return new ElytraHudConfig();
    }
}
