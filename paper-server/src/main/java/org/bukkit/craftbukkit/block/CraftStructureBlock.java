package org.bukkit.craftbukkit.block;

import com.google.common.base.Preconditions;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Rotation;
import net.minecraft.world.level.block.entity.StructureBlockEntity;
import net.minecraft.world.level.block.state.properties.StructureMode;
import org.bukkit.Location;
import org.bukkit.World;
import org.bukkit.block.Structure;
import org.bukkit.block.structure.Mirror;
import org.bukkit.block.structure.StructureRotation;
import org.bukkit.block.structure.UsageMode;
import org.bukkit.craftbukkit.entity.CraftLivingEntity;
import org.bukkit.craftbukkit.util.CraftBlockVector;
import org.bukkit.entity.LivingEntity;
import org.bukkit.util.BlockVector;

public class CraftStructureBlock extends CraftBlockEntityState<StructureBlockEntity> implements Structure {

    private static final int MAX_SIZE = 48;

    public CraftStructureBlock(World world, StructureBlockEntity blockEntity) {
        super(world, blockEntity);
    }

    protected CraftStructureBlock(CraftStructureBlock state, Location location) {
        super(state, location);
    }

    @Override
    public String getStructureName() {
        return this.getSnapshot().getStructureName();
    }

    @Override
    public void setStructureName(String name) {
        Preconditions.checkArgument(name != null, "结构名称不能为 null");
        this.getSnapshot().setStructureName(name);
    }

    @Override
    public String getAuthor() {
        return this.getSnapshot().author;
    }

    @Override
    public void setAuthor(String author) {
        Preconditions.checkArgument(author != null, "作者名不能为 null");
        Preconditions.checkArgument(!author.isEmpty(), "作者名不能为空");
        this.getSnapshot().author = author;
    }

    @Override
    public void setAuthor(LivingEntity entity) {
        Preconditions.checkArgument(entity != null, "结构方块作者实体不能为 null");
        this.getSnapshot().createdBy(((CraftLivingEntity) entity).getHandle());
    }

    @Override
    public BlockVector getRelativePosition() {
        return CraftBlockVector.toBukkit(this.getSnapshot().getStructurePos());
    }

    @Override
    public void setRelativePosition(BlockVector vector) {
        Preconditions.checkArgument(CraftStructureBlock.isBetween(vector.getBlockX(), -CraftStructureBlock.MAX_SIZE, CraftStructureBlock.MAX_SIZE), "结构尺寸（X）必须在 -%s 到 %s 之间，但实际为 %s", CraftStructureBlock.MAX_SIZE, CraftStructureBlock.MAX_SIZE, vector.getBlockX());
        Preconditions.checkArgument(CraftStructureBlock.isBetween(vector.getBlockY(), -CraftStructureBlock.MAX_SIZE, CraftStructureBlock.MAX_SIZE), "结构尺寸（Y）必须在 -%s 到 %s 之间，但实际为 %s", CraftStructureBlock.MAX_SIZE, CraftStructureBlock.MAX_SIZE, vector.getBlockY());
        Preconditions.checkArgument(CraftStructureBlock.isBetween(vector.getBlockZ(), -CraftStructureBlock.MAX_SIZE, CraftStructureBlock.MAX_SIZE), "结构尺寸（Z）必须在 -%s 到 %s 之间，但实际为 %s", CraftStructureBlock.MAX_SIZE, CraftStructureBlock.MAX_SIZE, vector.getBlockZ());
        this.getSnapshot().setStructurePos(CraftBlockVector.toBlockPosition(vector));
    }

    @Override
    public BlockVector getStructureSize() {
        return CraftBlockVector.toBukkit(this.getSnapshot().getStructureSize());
    }

    @Override
    public void setStructureSize(BlockVector vector) {
        Preconditions.checkArgument(CraftStructureBlock.isBetween(vector.getBlockX(), 0, CraftStructureBlock.MAX_SIZE), "结构尺寸（X）必须在 %s 到 %s 之间，但实际为 %s", 0, CraftStructureBlock.MAX_SIZE, vector.getBlockX());
        Preconditions.checkArgument(CraftStructureBlock.isBetween(vector.getBlockY(), 0, CraftStructureBlock.MAX_SIZE), "结构尺寸（Y）必须在 %s 到 %s 之间，但实际为 %s", 0, CraftStructureBlock.MAX_SIZE, vector.getBlockY());
        Preconditions.checkArgument(CraftStructureBlock.isBetween(vector.getBlockZ(), 0, CraftStructureBlock.MAX_SIZE), "结构尺寸（Z）必须在 %s 到 %s 之间，但实际为 %s", 0, CraftStructureBlock.MAX_SIZE, vector.getBlockZ());
        this.getSnapshot().setStructureSize(CraftBlockVector.toBlockPosition(vector));
    }

    @Override
    public void setMirror(Mirror mirror) {
        Preconditions.checkArgument(mirror != null, "镜像不能为 null");
        this.getSnapshot().setMirror(net.minecraft.world.level.block.Mirror.valueOf(mirror.name()));
    }

    @Override
    public Mirror getMirror() {
        return Mirror.valueOf(this.getSnapshot().getMirror().name());
    }

    @Override
    public void setRotation(StructureRotation rotation) {
        Preconditions.checkArgument(rotation != null, "StructureRotation 不能为 null");
        this.getSnapshot().setRotation(Rotation.valueOf(rotation.name()));
    }

    @Override
    public StructureRotation getRotation() {
        return StructureRotation.valueOf(this.getSnapshot().getRotation().name());
    }

    @Override
    public void setUsageMode(UsageMode mode) {
        Preconditions.checkArgument(mode != null, "UsageMode 不能为 null");
        this.getSnapshot().mode = StructureMode.valueOf(mode.name());
    }

    @Override
    public UsageMode getUsageMode() {
        return UsageMode.valueOf(this.getSnapshot().getMode().name());
    }

    @Override
    public void setIgnoreEntities(boolean flag) {
        this.getSnapshot().ignoreEntities = flag;
    }

    @Override
    public boolean isIgnoreEntities() {
        return this.getSnapshot().ignoreEntities;
    }

    @Override
    public void setShowAir(boolean showAir) {
        this.getSnapshot().setShowAir(showAir);
    }

    @Override
    public boolean isShowAir() {
        return this.getSnapshot().getShowAir();
    }

    @Override
    public void setBoundingBoxVisible(boolean showBoundingBox) {
        this.getSnapshot().setShowBoundingBox(showBoundingBox);
    }

    @Override
    public boolean isBoundingBoxVisible() {
        return this.getSnapshot().getShowBoundingBox();
    }

    @Override
    public void setIntegrity(float integrity) {
        Preconditions.checkArgument(CraftStructureBlock.isBetween(integrity, 0.0f, 1.0f), "完整性必须介于 0.0f 到 1.0f 之间，但实际为 %s", integrity);
        this.getSnapshot().setIntegrity(integrity);
    }

    @Override
    public float getIntegrity() {
        return this.getSnapshot().getIntegrity();
    }

    @Override
    public void setSeed(long seed) {
        this.getSnapshot().setSeed(seed);
    }

    @Override
    public long getSeed() {
        return this.getSnapshot().getSeed();
    }

    @Override
    public void setMetadata(String metadata) {
        Preconditions.checkArgument(metadata != null, "结构元数据不能为 null");
        if (this.getUsageMode() == UsageMode.DATA) {
            this.getSnapshot().setMetaData(metadata);
        }
    }

    @Override
    public String getMetadata() {
        return this.getSnapshot().getMetaData();
    }

    @Override
    protected void applyTo(StructureBlockEntity blockEntity) {
        super.applyTo(blockEntity);
        net.minecraft.world.level.LevelAccessor access = this.getWorldHandle();

        // Ensure block type is correct
        if (access instanceof net.minecraft.world.level.Level) {
            blockEntity.setMode(blockEntity.getMode());
        } else if (access != null) {
            // Custom handle during world generation
            // From StructureBlockEntity#setMode(BlockPropertyStructureMode)
            net.minecraft.world.level.block.state.BlockState state = access.getBlockState(this.getPosition());
            if (state.is(net.minecraft.world.level.block.Blocks.STRUCTURE_BLOCK)) {
                access.setBlock(this.getPosition(), state.setValue(net.minecraft.world.level.block.StructureBlock.MODE, blockEntity.getMode()), Block.UPDATE_CLIENTS);
            }
        }
    }

    @Override
    public CraftStructureBlock copy() {
        return new CraftStructureBlock(this, null);
    }

    @Override
    public CraftStructureBlock copy(Location location) {
        return new CraftStructureBlock(this, location);
    }

    private static boolean isBetween(int num, int min, int max) {
        return num >= min && num <= max;
    }

    private static boolean isBetween(float num, float min, float max) {
        return num >= min && num <= max;
    }
}
