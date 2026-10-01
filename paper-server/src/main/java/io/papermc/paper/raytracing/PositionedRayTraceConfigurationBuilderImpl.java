package io.papermc.paper.raytracing;

import com.google.common.base.Preconditions;
import java.util.EnumSet;
import java.util.OptionalDouble;
import java.util.function.Predicate;
import org.bukkit.FluidCollisionMode;
import org.bukkit.Location;
import org.bukkit.block.Block;
import org.bukkit.entity.Entity;
import org.bukkit.util.Vector;
import org.jspecify.annotations.NullMarked;
import org.jspecify.annotations.Nullable;

@NullMarked
public class PositionedRayTraceConfigurationBuilderImpl implements PositionedRayTraceConfigurationBuilder {

    public @Nullable Location start;
    public @Nullable Vector direction;
    public OptionalDouble maxDistance = OptionalDouble.empty();
    public FluidCollisionMode fluidCollisionMode = FluidCollisionMode.NEVER;
    public BlockCollisionMode blockCollisionMode = BlockCollisionMode.OUTLINE;
    public double raySize = 0.0;
    public @Nullable Predicate<? super Entity> entityFilter;
    public @Nullable Predicate<? super Block> blockFilter;
    public EnumSet<RayTraceTarget> targets = EnumSet.noneOf(RayTraceTarget.class);

    @Override
    public PositionedRayTraceConfigurationBuilder start(final Location start) {
        Preconditions.checkArgument(start != null, "start 不能为 null");
        this.start = start.clone();
        return this;
    }

    @Override
    public PositionedRayTraceConfigurationBuilder direction(final Vector direction) {
        Preconditions.checkArgument(direction != null, "direction 不能为 null");
        this.direction = direction.clone();
        return this;
    }

    @Override
    public PositionedRayTraceConfigurationBuilder maxDistance(final double maxDistance) {
        Preconditions.checkArgument(maxDistance >= 0, "maxDistance 不能为负数");
        this.maxDistance = OptionalDouble.of(maxDistance);
        return this;
    }

    @Override
    public PositionedRayTraceConfigurationBuilder fluidCollisionMode(final FluidCollisionMode fluidCollisionMode) {
        Preconditions.checkArgument(fluidCollisionMode != null, "fluidCollisionMode 不能为 null");
        this.fluidCollisionMode = fluidCollisionMode;
        return this;
    }

    @Override
    public PositionedRayTraceConfigurationBuilder blockCollisionMode(final BlockCollisionMode blockCollisionMode) {
        Preconditions.checkArgument(blockCollisionMode != null, "blockCollisionMode 不能为 null");
        this.blockCollisionMode = blockCollisionMode;
        return this;
    }

    @Override
    public PositionedRayTraceConfigurationBuilder ignorePassableBlocks(final boolean ignorePassableBlocks) {
        this.blockCollisionMode = ignorePassableBlocks ? BlockCollisionMode.COLLIDER : BlockCollisionMode.OUTLINE;
        return this;
    }

    @Override
    public PositionedRayTraceConfigurationBuilder raySize(final double raySize) {
        Preconditions.checkArgument(raySize >= 0, "raySize 必须为非负数");
        this.raySize = raySize;
        return this;
    }

    @Override
    public PositionedRayTraceConfigurationBuilder entityFilter(final Predicate<? super Entity> entityFilter) {
        Preconditions.checkArgument(entityFilter != null, "entityFilter 不能为 null");
        this.entityFilter = entityFilter;
        return this;
    }

    @Override
    public PositionedRayTraceConfigurationBuilder blockFilter(final Predicate<? super Block> blockFilter) {
        Preconditions.checkArgument(blockFilter != null, "blockFilter 不能为 null");
        this.blockFilter = blockFilter;
        return this;
    }

    @Override
    public PositionedRayTraceConfigurationBuilder targets(final RayTraceTarget first, final RayTraceTarget... others) {
        Preconditions.checkArgument(first != null, "first 不能为 null");
        Preconditions.checkArgument(others != null, "others 不能为 null");
        this.targets = EnumSet.of(first, others);
        return this;
    }
}
