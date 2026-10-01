package org.bukkit.craftbukkit.entity;

import com.google.common.base.Preconditions;
import net.minecraft.core.BlockPos;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.entity.projectile.FishingHook;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import org.bukkit.craftbukkit.CraftEquipmentSlot;
import org.bukkit.craftbukkit.CraftServer;
import org.bukkit.entity.Entity;
import org.bukkit.entity.FishHook;
import org.bukkit.inventory.EquipmentSlot;

public class CraftFishHook extends CraftProjectile implements FishHook {

    private double biteChance = -1;

    public CraftFishHook(CraftServer server, FishingHook entity) {
        super(server, entity);
    }

    @Override
    public FishingHook getHandle() {
        return (FishingHook) this.entity;
    }

    @Override
    public int getMinWaitTime() {
        return this.getHandle().minWaitTime;
    }

    @Override
    public void setMinWaitTime(int minWaitTime) {
        Preconditions.checkArgument(minWaitTime >= 0 && minWaitTime <= this.getMaxWaitTime(), "最小等待时间应在 %s 到 %s 之间（最大等待时间）", 0, this.getMaxWaitTime());
        FishingHook hook = this.getHandle();
        hook.minWaitTime = minWaitTime;
    }

    @Override
    public int getMaxWaitTime() {
        return this.getHandle().maxWaitTime;
    }

    @Override
    public void setMaxWaitTime(int maxWaitTime) {
        Preconditions.checkArgument(maxWaitTime >= 0 && maxWaitTime >= this.getMinWaitTime(), "最大等待时间应在 %s 到 %s 之间（最小等待时间）", 0, this.getMinWaitTime());
        FishingHook hook = this.getHandle();
        hook.maxWaitTime = maxWaitTime;
    }

    @Override
    public void setWaitTime(int min, int max) {
        Preconditions.checkArgument(min >= 0 && max >= 0 && min <= max, "最小/最大等待时间应大于或等于 0 和最小等待时间");
        this.getHandle().minWaitTime = min;
        this.getHandle().maxWaitTime = max;
    }

    @Override
    public int getMinLureTime() {
        return this.getHandle().minLureTime;
    }

    @Override
    public void setMinLureTime(int minLureTime) {
        Preconditions.checkArgument(minLureTime >= 0 && minLureTime <= this.getMaxLureTime(), "最小鱼饵时间（%s）应在 0 到 %s 之间（最大等待时间）", minLureTime, this.getMaxLureTime());
        this.getHandle().minLureTime = minLureTime;
    }

    @Override
    public int getMaxLureTime() {
        return this.getHandle().maxLureTime;
    }

    @Override
    public void setMaxLureTime(int maxLureTime) {
        Preconditions.checkArgument(maxLureTime >= 0 && maxLureTime >= this.getMinLureTime(), "最大鱼饵等待时间（%s）应大于或等于 0 和 %s（最小等待时间）", maxLureTime, this.getMinLureTime());
        this.getHandle().maxLureTime = maxLureTime;
    }

    @Override
    public void setLureTime(int min, int max) {
        Preconditions.checkArgument(min >= 0 && max >= 0 && min <= max, "最小/最大鱼饵时间应大于或等于 0 和最小等待时间。");
        this.getHandle().minLureTime = min;
        this.getHandle().maxLureTime = max;
    }

    @Override
    public float getMinLureAngle() {
        return this.getHandle().minLureAngle;
    }

    @Override
    public void setMinLureAngle(float minLureAngle) {
        Preconditions.checkArgument(minLureAngle <= this.getMaxLureAngle(), "最小鱼饵角度（%s）应小于 %s（最大鱼饵角度）", minLureAngle, this.getMaxLureAngle());
        this.getHandle().minLureAngle = minLureAngle;
    }

    @Override
    public float getMaxLureAngle() {
        return this.getHandle().maxLureAngle;
    }

    @Override
    public void setMaxLureAngle(float maxLureAngle) {
        Preconditions.checkArgument(maxLureAngle >= this.getMinLureAngle(), "最小鱼饵角度（%s）应小于 %s（最大鱼饵角度）", maxLureAngle, this.getMinLureAngle());
        this.getHandle().maxLureAngle = maxLureAngle;
    }

    @Override
    public void setLureAngle(float min, float max) {
        Preconditions.checkArgument(min <= max, "最小鱼饵角度（%s）应小于最大鱼饵角度（%s）", min, max);
        this.getHandle().minLureAngle = min;
        this.getHandle().maxLureAngle = max;
    }

    @Override
    public boolean isSkyInfluenced() {
        return this.getHandle().skyInfluenced;
    }

    @Override
    public void setSkyInfluenced(boolean skyInfluenced) {
        this.getHandle().skyInfluenced = skyInfluenced;
    }

    @Override
    public boolean isRainInfluenced() {
        return this.getHandle().rainInfluenced;
    }

    @Override
    public void setRainInfluenced(boolean rainInfluenced) {
        this.getHandle().rainInfluenced = rainInfluenced;
    }

    @Override
    public boolean getApplyLure() {
        return this.getHandle().applyLure;
    }

    @Override
    public void setApplyLure(boolean applyLure) {
        this.getHandle().applyLure = applyLure;
    }

    @Override
    public double getBiteChance() {
        FishingHook hook = this.getHandle();

        if (this.biteChance == -1) {
            if (hook.level().isRainingAt(BlockPos.containing(hook.position()).offset(0, 1, 0))) {
                return 1 / 300.0;
            }
            return 1 / 500.0;
        }
        return this.biteChance;
    }

    @Override
    public void setBiteChance(double chance) {
        Preconditions.checkArgument(chance >= 0 && chance <= 1, "叮咬概率必须在 0 到 1 之间");
        this.biteChance = chance;
    }

    @Override
    public boolean isInOpenWater() {
        return this.getHandle().outOfWaterTime < 10 && this.getHandle().calculateOpenWater(this.getHandle().blockPosition()); // Paper - isOpenWaterFishing is only calculated when a "fish" is approaching the hook
    }

    @Override
    public Entity getHookedEntity() {
        net.minecraft.world.entity.Entity hooked = this.getHandle().getHookedIn();
        return (hooked != null) ? hooked.getBukkitEntity() : null;
    }

    @Override
    public void setHookedEntity(Entity entity) {
        this.getHandle().setHookedEntity(entity != null ? ((CraftEntity) entity).getHandle() : null);
    }

    @Override
    public boolean pullHookedEntity() {
        FishingHook hook = this.getHandle();
        if (hook.getHookedIn() == null) {
            return false;
        }

        hook.pullEntity(hook.getHookedIn());
        return true;
    }

    @Override
    public HookState getState() {
        return HookState.values()[this.getHandle().currentState.ordinal()];
    }

    @Override
    public int getWaitTime() {
        return this.getHandle().timeUntilLured;
    }

    @Override
    public void setWaitTime(int ticks) {
        this.getHandle().timeUntilLured = ticks;
    }

    @Override
    public int getTimeUntilBite() {
        return this.getHandle().timeUntilHooked;
    }

    @Override
    public void setTimeUntilBite(final int ticks) {
        com.google.common.base.Preconditions.checkArgument(ticks >= 1, "无法将距离叮咬的时间设为小于 1（%s<1）", ticks);
        final FishingHook hook = this.getHandle();

        // Reset the fish angle hook only when this call "enters" the fish into the lure stage.
        final boolean alreadyInLuringPhase = hook.timeUntilHooked > 0 && hook.timeUntilLured <= 0;
        if (!alreadyInLuringPhase) {
            hook.fishAngle = net.minecraft.util.Mth.nextFloat(hook.getRandom(), hook.minLureAngle, hook.maxLureAngle);
            hook.timeUntilLured = 0;
        }

        hook.timeUntilHooked = ticks;
    }

    @Override
    public void resetFishingState() {
        final FishingHook hook = this.getHandle();
        hook.resetTimeUntilLured();
        hook.timeUntilHooked = 0; // Reset time until hooked, will be repopulated once lured time is ticked down.
    }

    @Override
    public int retrieve(EquipmentSlot slot) {
        Preconditions.checkArgument(slot == EquipmentSlot.HAND || slot == EquipmentSlot.OFF_HAND, "装备槽必须是 HAND 或 OFF_HAND");
        final FishingHook fishingHook = getHandle();
        final Player playerOwner = fishingHook.getPlayerOwner();
        Preconditions.checkState(playerOwner != null, "玩家所有者不能为 null");

        final InteractionHand hand = CraftEquipmentSlot.getHand(slot);
        final ItemStack itemInHand = playerOwner.getItemInHand(hand);
        Preconditions.checkState(itemInHand.is(Items.FISHING_ROD), "槽位中的物品不是钓鱼竿");

        return fishingHook.retrieve(itemInHand, hand);
    }
}
