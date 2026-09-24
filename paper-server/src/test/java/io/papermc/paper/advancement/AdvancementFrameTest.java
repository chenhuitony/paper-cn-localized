package io.papermc.paper.advancement;

import net.kyori.adventure.text.format.NamedTextColor;
import net.minecraft.advancements.AdvancementType;
import net.minecraft.network.chat.contents.TranslatableContents;
import org.bukkit.support.environment.Normal;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

@Normal
public class AdvancementFrameTest {

    @Test
    public void test() {
        for (final AdvancementType advancementType : AdvancementType.values()) {
            final NamedTextColor expectedColor = NamedTextColor.NAMES.value(net.minecraft.network.chat.TextColor.fromLegacyFormat(advancementType.getChatColor()).toString());
            final String expectedTranslationKey = ((TranslatableContents) advancementType.getDisplayName().getContents()).getKey();
            final var frame = PaperAdvancementDisplay.asPaperFrame(advancementType);
            assertEquals(expectedTranslationKey, frame.translationKey(), "翻译键应一致");
            assertEquals(expectedColor, frame.color(), "框颜色应一致");
            assertEquals(advancementType.getSerializedName(), AdvancementDisplay.Frame.NAMES.key(frame));
        }
    }
}
