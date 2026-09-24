package org.bukkit.craftbukkit.block.impl;

import com.google.common.base.Preconditions;
import io.papermc.paper.annotation.GeneratedClass;
import net.minecraft.world.level.block.StandingSignBlock;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.properties.BooleanProperty;
import net.minecraft.world.level.block.state.properties.IntegerProperty;
import net.minecraft.world.level.block.state.properties.RotationSegment;
import org.bukkit.block.BlockFace;
import org.bukkit.block.data.type.Sign;
import org.bukkit.craftbukkit.block.data.CraftBlockData;
import org.bukkit.util.Vector;
import org.jspecify.annotations.NullMarked;

@NullMarked
@GeneratedClass
public class CraftStandingSign extends CraftBlockData implements Sign {
    private static final IntegerProperty ROTATION = StandingSignBlock.ROTATION;

    private static final BooleanProperty WATERLOGGED = StandingSignBlock.WATERLOGGED;

    public CraftStandingSign(BlockState state) {
        super(state);
    }

    @Override
    public BlockFace getRotation() {
        return CraftBlockData.ROTATION_CYCLE[this.get(ROTATION)];
    }

    @Override
    public void setRotation(final BlockFace blockFace) {
        Preconditions.checkArgument(blockFace != null, "blockFace 不能为 null！");
        Preconditions.checkArgument(blockFace != BlockFace.SELF && blockFace.getModY() == 0, "面无效，此属性只允许水平面！");
        Vector dir = blockFace.getDirection();
        float angle = (float) -Math.toDegrees(Math.atan2(dir.getX(), dir.getZ()));
        this.set(ROTATION, RotationSegment.convertToSegment(angle));
    }

    @Override
    public boolean isWaterlogged() {
        return this.get(WATERLOGGED);
    }

    @Override
    public void setWaterlogged(final boolean waterlogged) {
        this.set(WATERLOGGED, waterlogged);
    }
}
