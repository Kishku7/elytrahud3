// SHARED SOURCE -- canonical location: _codegen/cog_sources/fabric (version-invariant Fabric glue).
// Copied verbatim into each pre-26 cell's gen/ by scripts/cog-gen.ps1; check-sync guards the
// Fabric/26 twin.
package dev.kishku.elytrahud3;

import com.terraformersmc.modmenu.api.ConfigScreenFactory;
import com.terraformersmc.modmenu.api.ModMenuApi;

public class ElytraHudModMenu implements ModMenuApi {
    @Override
    public ConfigScreenFactory<?> getModConfigScreenFactory() {
        return ElytraHudConfigScreen::new;
    }
}
