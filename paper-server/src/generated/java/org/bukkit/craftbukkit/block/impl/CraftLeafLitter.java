package org.bukkit.craftbukkit.block.impl;

import com.google.common.base.Preconditions;
import io.papermc.paper.annotation.GeneratedClass;
import java.util.Set;
import net.minecraft.core.Direction;
import net.minecraft.world.level.block.LeafLitterBlock;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.properties.EnumProperty;
import net.minecraft.world.level.block.state.properties.IntegerProperty;
import org.bukkit.block.BlockFace;
import org.bukkit.block.data.type.LeafLitter;
import org.bukkit.craftbukkit.block.data.CraftBlockData;
import org.jspecify.annotations.NullMarked;

@NullMarked
@GeneratedClass
public class CraftLeafLitter extends CraftBlockData implements LeafLitter {
    private static final EnumProperty<Direction> FACING = LeafLitterBlock.FACING;

    private static final IntegerProperty AMOUNT = LeafLitterBlock.AMOUNT;

    public CraftLeafLitter(BlockState state) {
        super(state);
    }

    @Override
    public BlockFace getFacing() {
        return this.get(FACING, BlockFace.class);
    }

    @Override
    public void setFacing(final BlockFace blockFace) {
        Preconditions.checkArgument(blockFace != null, "blockFace 不能为 null！");
        Preconditions.checkArgument(blockFace.isCartesian() && blockFace.getModY() == 0, "面无效，此属性只允许笛卡尔水平面！");
        this.set(FACING, blockFace);
    }

    @Override
    public Set<BlockFace> getFaces() {
        return this.getValues(FACING, BlockFace.class);
    }

    @Override
    public int getSegmentAmount() {
        return this.get(AMOUNT);
    }

    @Override
    public void setSegmentAmount(final int segmentAmount) {
        this.set(AMOUNT, segmentAmount);
    }

    @Override
    public int getMinimumSegmentAmount() {
        return AMOUNT.min;
    }

    @Override
    public int getMaximumSegmentAmount() {
        return AMOUNT.max;
    }
}
