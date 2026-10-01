package org.bukkit.potion;

import net.minecraft.core.registries.BuiltInRegistries;
import org.bukkit.craftbukkit.legacy.FieldRename;
import org.bukkit.craftbukkit.potion.CraftPotionEffectType;
import org.bukkit.support.environment.AllFeatures;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

@AllFeatures
public class PotionTest {

    @Test
    public void testEffectType() {
        BuiltInRegistries.MOB_EFFECT.listElements().forEach(reference -> {
            PotionEffectType bukkit = CraftPotionEffectType.minecraftHolderToBukkit(reference);

            assertNotNull(bukkit, "没有对应的 Bukkit 类型：" + reference.key());

            PotionEffectType byName = FieldRename.getByName_PotionEffectType(bukkit.getName());
            assertEquals(bukkit, byName, "按名称未返回相同类型：" + reference.key());
        });
    }
}
