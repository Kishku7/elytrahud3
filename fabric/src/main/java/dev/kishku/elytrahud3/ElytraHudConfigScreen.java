package dev.kishku.elytrahud3;

import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.components.CycleButton;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.network.chat.Component;

import java.util.function.Consumer;
import java.util.function.Supplier;

public class ElytraHudConfigScreen extends Screen {
    private final Screen parent;

    public ElytraHudConfigScreen(Screen parent) {
        super(Component.literal("ElytraHud3 Settings"));
        this.parent = parent;
    }

    @Override
    protected void init() {
        ElytraHudConfig c = ConfigManager.getConfig();
        int colW = 150;
        int rowH = 24;
        int top = 40;
        int leftX = this.width / 2 - 155;
        int rightX = this.width / 2 + 5;

        addToggle(leftX, top + rowH * 0, colW, "Mod Enabled", () -> c.modEnabled, v -> c.modEnabled = v);
        addToggle(leftX, top + rowH * 1, colW, "Always Show HUD", () -> c.alwaysDisplayHud, v -> c.alwaysDisplayHud = v);
        addToggle(leftX, top + rowH * 2, colW, "Imperial Units", () -> c.imperialUnits, v -> c.imperialUnits = v);
        addToggle(leftX, top + rowH * 3, colW, "Show Titles", () -> c.renderTitles, v -> c.renderTitles = v);
        addToggle(leftX, top + rowH * 4, colW, "Show Values", () -> c.renderValues, v -> c.renderValues = v);
        addToggle(leftX, top + rowH * 5, colW, "Airspeed", () -> c.renderAirspeed, v -> c.renderAirspeed = v);

        addToggle(rightX, top + rowH * 0, colW, "Horizon", () -> c.renderHorizon, v -> c.renderHorizon = v);
        addToggle(rightX, top + rowH * 1, colW, "Durability", () -> c.renderDurability, v -> c.renderDurability = v);
        addToggle(rightX, top + rowH * 2, colW, "Altitude", () -> c.renderAltitude, v -> c.renderAltitude = v);
        addToggle(rightX, top + rowH * 3, colW, "Vertical Speed", () -> c.renderVertical, v -> c.renderVertical = v);
        addToggle(rightX, top + rowH * 4, colW, "Compass", () -> c.renderCompass, v -> c.renderCompass = v);

        addRenderableWidget(
            Button.builder(Component.literal("Done"), b -> this.onClose())
                .bounds(this.width / 2 - 75, this.height - 32, 150, 20)
                .build()
        );
    }

    private void addToggle(int x, int y, int w, String label, Supplier<Boolean> get, Consumer<Boolean> set) {
        addRenderableWidget(
            CycleButton.onOffBuilder(get.get())
                .create(x, y, w, 20, Component.literal(label),
                    (btn, val) -> {
                        set.accept(val);
                        ConfigManager.save();
                    })
        );
    }

    @Override
    public void onClose() {
        ConfigManager.save();
        if (this.minecraft != null) {
            this.minecraft.setScreen(parent);
        }
    }
}
