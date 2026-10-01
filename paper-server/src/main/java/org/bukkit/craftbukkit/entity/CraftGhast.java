package org.bukkit.craftbukkit.entity;

import org.bukkit.craftbukkit.CraftServer;
import org.bukkit.entity.Ghast;

public class CraftGhast extends CraftMob implements Ghast, CraftEnemy {

    public CraftGhast(CraftServer server, net.minecraft.world.entity.monster.Ghast entity) {
        super(server, entity);
    }

    @Override
    public net.minecraft.world.entity.monster.Ghast getHandle() {
        return (net.minecraft.world.entity.monster.Ghast) this.entity;
    }

    @Override
    public boolean isCharging() {
        return this.getHandle().isCharging();
    }

    @Override
    public void setCharging(boolean flag) {
        this.getHandle().setCharging(flag);
    }

    @Override
    public int getExplosionPower() {
        return this.getHandle().getExplosionPower();
    }

    @Override
    public void setExplosionPower(int explosionPower) {
        com.google.common.base.Preconditions.checkArgument(explosionPower >= 0 && explosionPower <= 127, "爆炸威力必须在 0 到 127 之间");
        this.getHandle().setExplosionPower(explosionPower);
    }
}
