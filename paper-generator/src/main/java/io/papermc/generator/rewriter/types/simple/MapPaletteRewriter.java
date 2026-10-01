package io.papermc.generator.rewriter.types.simple;

import com.mojang.logging.LogUtils;
import io.papermc.typewriter.replace.SearchMetadata;
import io.papermc.typewriter.replace.SearchReplaceRewriter;
import java.awt.Color;
import net.minecraft.world.level.material.MapColor;
import org.jspecify.annotations.Nullable;
import org.slf4j.Logger;

public class MapPaletteRewriter extends SearchReplaceRewriter {

    private static final Logger LOGGER = LogUtils.getLogger();
    private static final boolean UPDATING = Boolean.getBoolean("paper.updatingMinecraft");

    @Override
    protected void insert(SearchMetadata metadata, StringBuilder builder) {
        int count = 0;
        for (@Nullable MapColor mapColor : MapColor.MATERIAL_COLORS) {
            if (mapColor == null) {
                continue;
            }

            for (MapColor.Brightness brightness : MapColor.Brightness.values()) {
                builder.append(metadata.indent());
                Color color = new Color(mapColor.calculateARGBColor(brightness), true);
                if (color.getAlpha() != 0xFF) {
                    builder.append("new %s(0x%08X, true),".formatted(color.getClass().getSimpleName(), color.getRGB()));
                } else {
                    builder.append("new %s(0x%06X),".formatted(color.getClass().getSimpleName(), color.getRGB() & 0x00FFFFFF));
                }
                builder.append('\n');
                count++;
            }
        }

        if (UPDATING) {
            LOGGER.warn("共有 {} 种地图颜色，如有变化请检查 CraftMapView#render 并更新 CraftMapColorCache 中的 md5 哈希", count);
        }
    }
}
