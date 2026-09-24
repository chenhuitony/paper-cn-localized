package org.bukkit.craftbukkit.entity;

import com.google.common.base.Preconditions;
import java.util.UUID;
import net.minecraft.Optionull;
import net.minecraft.world.entity.EntityReference;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.ai.attributes.Attributes;
import org.bukkit.craftbukkit.CraftServer;
import org.bukkit.craftbukkit.inventory.CraftInventorySaddledHorse;
import org.bukkit.entity.AbstractHorse;
import org.bukkit.entity.AnimalTamer;
import org.bukkit.entity.Horse;
import org.bukkit.inventory.AbstractHorseInventory;

public abstract class CraftAbstractHorse extends CraftAnimals implements AbstractHorse {

    public CraftAbstractHorse(CraftServer server, net.minecraft.world.entity.animal.equine.AbstractHorse entity) {
        super(server, entity);
    }

    @Override
    public net.minecraft.world.entity.animal.equine.AbstractHorse getHandle() {
        return (net.minecraft.world.entity.animal.equine.AbstractHorse) this.entity;
    }

    @Override
    public void setVariant(Horse.Variant variant) {
        throw new UnsupportedOperationException("不支持。");
    }

    @Override
    public int getDomestication() {
        return this.getHandle().getTemper();
    }

    @Override
    public void setDomestication(int value) {
        Preconditions.checkArgument(value >= 0 && value <= this.getMaxDomestication(), "驯化等级 (%s) 必须介于 %s 与 %s（最大驯化值）之间", value, 0, this.getMaxDomestication());
        this.getHandle().setTemper(value);
    }

    @Override
    public int getMaxDomestication() {
        return this.getHandle().getMaxTemper();
    }

    @Override
    public void setMaxDomestication(int value) {
        Preconditions.checkArgument(value > 0, "驯服上限（%s）不能小于等于零", value);
        this.getHandle().maxDomestication = value;
    }

    @Override
    public double getJumpStrength() {
        return this.getHandle().getAttributeValue(Attributes.JUMP_STRENGTH);
    }

    @Override
    public void setJumpStrength(double strength) {
        Preconditions.checkArgument(strength >= 0, "跳跃强度（%s）不能小于零", strength);
        this.getHandle().getAttribute(Attributes.JUMP_STRENGTH).setBaseValue(strength);
    }

    @Override
    public boolean isTamed() {
        return this.getHandle().isTamed();
    }

    @Override
    public void setTamed(boolean tamed) {
        this.getHandle().setTamed(tamed);
    }

    @Override
    public AnimalTamer getOwner() {
        if (this.getOwnerUUID() == null) return null;
        return this.getServer().getOfflinePlayer(this.getOwnerUUID());
    }

    @Override
    public void setOwner(AnimalTamer owner) {
        if (owner != null) {
            this.setTamed(true);
            this.getHandle().setTarget(null, null);
            this.setOwnerUUID(owner.getUniqueId());
        } else {
            this.setTamed(false);
            this.setOwnerUUID(null);
        }
    }

    @Override
    public UUID getOwnerUniqueId() {
        return this.getOwnerUUID();
    }

    public UUID getOwnerUUID() {
        return Optionull.map(this.getHandle().getOwnerReference(), EntityReference::getUUID);
    }

    public void setOwnerUUID(UUID uuid) {
        this.getHandle().owner = uuid == null ? null : EntityReference.of(uuid);
    }

    @Override
    public boolean isEatingHaystack() {
        return this.getHandle().isEating();
    }

    @Override
    public void setEatingHaystack(boolean eatingHaystack) {
        this.getHandle().setEating(eatingHaystack);
    }

    @Override
    public AbstractHorseInventory getInventory() {
        return new CraftInventorySaddledHorse(
            this.getHandle().inventory,
            this.getHandle().createEquipmentSlotContainer(EquipmentSlot.BODY),
            this.getHandle().createEquipmentSlotContainer(EquipmentSlot.SADDLE)
        );
    }

    @Override
    public boolean isEatingGrass() {
        return this.getHandle().isEating();
    }

    @Override
    public void setEatingGrass(boolean eating) {
        this.getHandle().setEating(eating);
    }

    @Override
    public boolean isRearing() {
        return this.getHandle().isStanding();
    }

    @Override
    public void setRearing(boolean rearing) {
        if (rearing) {
            this.getHandle().setStanding(Integer.MAX_VALUE);
        } else {
            this.getHandle().clearStanding();
        }
    }

    @Override
    public boolean isEating() {
        return this.getHandle().isMouthOpen();
    }

    @Override
    public void setEating(boolean eating) {
       this.getHandle().setMouthOpen(eating);
    }
}
