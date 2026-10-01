package org.bukkit.craftbukkit.entity;

import com.google.common.base.Preconditions;
import org.bukkit.DyeColor;
import org.bukkit.block.BlockFace;
import org.bukkit.craftbukkit.CraftServer;
import org.bukkit.craftbukkit.block.CraftBlock;
import org.bukkit.entity.Shulker;

public class CraftShulker extends CraftGolem implements Shulker, CraftEnemy {

    public CraftShulker(CraftServer server, net.minecraft.world.entity.monster.Shulker entity) {
        super(server, entity);
    }

    @Override
    public net.minecraft.world.entity.monster.Shulker getHandle() {
        return (net.minecraft.world.entity.monster.Shulker) this.entity;
    }

    @Override
    public DyeColor getColor() {
        return DyeColor.getByWoolData(this.getHandle().getEntityData().get(net.minecraft.world.entity.monster.Shulker.DATA_COLOR_ID));
    }

    @Override
    public void setColor(DyeColor color) {
        this.getHandle().getEntityData().set(net.minecraft.world.entity.monster.Shulker.DATA_COLOR_ID, (color == null) ? 16 : color.getWoolData());
    }

    @Override
    public float getPeek() {
        return (float) this.getHandle().getRawPeekAmount() / 100;
    }

    @Override
    public void setPeek(float value) {
        Preconditions.checkArgument(value >= 0 && value <= 1, "value 必须在 0 到 1 之间（含边界）");
        this.getHandle().setRawPeekAmount((int) (value * 100));
    }

    @Override
    public BlockFace getAttachedFace() {
        return CraftBlock.notchToBlockFace(this.getHandle().getAttachFace());
    }

    @Override
    public void setAttachedFace(BlockFace face) {
        Preconditions.checkNotNull(face, "face 不能为 null");
        Preconditions.checkArgument(face.isCartesian(), "%s 不是合法的潜影盒附着方块面，需要笛卡尔方向面", face);
        this.getHandle().setAttachFace(CraftBlock.blockFaceToNotch(face));
    }
}
