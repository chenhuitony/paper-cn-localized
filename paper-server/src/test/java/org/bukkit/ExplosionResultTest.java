package org.bukkit;

import static org.junit.jupiter.api.Assertions.*;
import net.minecraft.world.level.Explosion;
import org.bukkit.craftbukkit.CraftExplosionResult;
import org.junit.jupiter.api.Test;

@org.bukkit.support.environment.Normal // Paper - test changes - missing test suite annotation
public class ExplosionResultTest {

    @Test
    public void testMatchingEnum() {
        for (ExplosionResult result : ExplosionResult.values()) {
            assertNotNull(Explosion.BlockInteraction.valueOf(result.name()), "Bukkit 结果没有对应的 NMS 枚举：" + result);
        }
    }

    @Test
    public void testToBukkit() {
        for (Explosion.BlockInteraction effect : Explosion.BlockInteraction.values()) {
            assertNotNull(CraftExplosionResult.toExplosionResult(effect), "NMS 爆炸效果没有对应的 Bukkit 枚举：" + effect);
        }
    }
}
