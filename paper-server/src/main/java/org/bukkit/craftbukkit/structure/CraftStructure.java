package org.bukkit.craftbukkit.structure;

import com.google.common.base.Preconditions;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.List;
import java.util.Random;
import java.util.stream.Collectors;
import com.mojang.logging.LogUtils;
import net.minecraft.core.BlockPos;
import net.minecraft.core.RegistryAccess;
import net.minecraft.util.ProblemReporter;
import net.minecraft.util.RandomSource;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.EntitySpawnRequest;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.level.ChunkPos;
import net.minecraft.world.level.WorldGenLevel;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.Rotation;
import net.minecraft.world.level.levelgen.structure.templatesystem.BlockRotProcessor;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructurePlaceSettings;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructureTemplate;
import net.minecraft.world.level.storage.TagValueInput;
import org.bukkit.Bukkit;
import org.bukkit.Location;
import org.bukkit.RegionAccessor;
import org.bukkit.World;
import org.bukkit.block.structure.Mirror;
import org.bukkit.block.structure.StructureRotation;
import org.bukkit.craftbukkit.CraftRegionAccessor;
import org.bukkit.craftbukkit.CraftWorld;
import org.bukkit.craftbukkit.util.CraftBlockVector;
import org.bukkit.craftbukkit.util.CraftLocation;
import org.bukkit.craftbukkit.util.CraftStructureTransformer;
import org.bukkit.craftbukkit.util.RandomSourceWrapper;
import org.bukkit.craftbukkit.util.TransformerLevelAccessor;
import org.bukkit.entity.Entity;
import org.bukkit.persistence.PersistentDataContainer;
import org.bukkit.structure.Palette;
import org.bukkit.structure.Structure;
import org.bukkit.util.BlockTransformer;
import org.bukkit.util.BlockVector;
import org.bukkit.util.EntityTransformer;
import org.slf4j.Logger;

public class CraftStructure implements Structure {

    private static final Logger LOGGER = LogUtils.getLogger();

    private final StructureTemplate structure;
    private final RegistryAccess registry;

    public CraftStructure(StructureTemplate structure, RegistryAccess registry) {
        this.structure = structure;
        this.registry = registry;
    }

    @Override
    public void place(Location location, boolean includeEntities, StructureRotation structureRotation, Mirror mirror, int palette, float integrity, Random random) {
        this.place(location, includeEntities, structureRotation, mirror, palette, integrity, random, Collections.emptyList(), Collections.emptyList());
    }

    @Override
    public void place(Location location, boolean includeEntities, StructureRotation structureRotation, Mirror mirror, int palette, float integrity, Random random, Collection<BlockTransformer> blockTransformers, Collection<EntityTransformer> entityTransformers) {
        Preconditions.checkArgument(location != null, "位置不能为 null");
        location.checkFinite();
        World world = location.getWorld();
        Preconditions.checkArgument(world != null, "位置的世界不能为 null");

        BlockVector blockVector = new BlockVector(location.getBlockX(), location.getBlockY(), location.getBlockZ());
        this.place(world, blockVector, includeEntities, structureRotation, mirror, palette, integrity, random, blockTransformers, entityTransformers);
    }

    @Override
    public void place(RegionAccessor regionAccessor, BlockVector location, boolean includeEntities, StructureRotation structureRotation, Mirror mirror, int palette, float integrity, Random random) {
       this.place(regionAccessor, location, includeEntities, structureRotation, mirror, palette, integrity, random, Collections.emptyList(), Collections.emptyList());
    }

    @Override
    public void place(RegionAccessor regionAccessor, BlockVector location, boolean includeEntities, StructureRotation structureRotation, Mirror mirror, int palette, float integrity, Random random, Collection<BlockTransformer> blockTransformers, Collection<EntityTransformer> entityTransformers) {
        Preconditions.checkArgument(location != null, "位置不能为 null");
        Preconditions.checkArgument(regionAccessor != null, "RegionAccessor 不能为 null");
        Preconditions.checkArgument(blockTransformers != null, "BlockTransformers 不能为 null");
        Preconditions.checkArgument(entityTransformers != null, "EntityTransformers 不能为 null");
        location.checkFinite();

        Preconditions.checkArgument(integrity >= 0F && integrity <= 1F, "完整性值 (%S) 必须介于 0 到 1 之间（含边界）", integrity);

        RandomSource randomSource = new RandomSourceWrapper(random);
        StructurePlaceSettings definedstructureinfo = new StructurePlaceSettings()
                .setMirror(net.minecraft.world.level.block.Mirror.valueOf(mirror.name()))
                .setRotation(Rotation.valueOf(structureRotation.name()))
                .setIgnoreEntities(!includeEntities)
                .addProcessor(new BlockRotProcessor(integrity))
                .setRandom(randomSource);
        definedstructureinfo.palette = palette;

        BlockPos pos = CraftBlockVector.toBlockPosition(location);
        WorldGenLevel handle = ((CraftRegionAccessor) regionAccessor).getHandle();

        TransformerLevelAccessor accessor = new TransformerLevelAccessor();
        accessor.setDelegate(handle);
        accessor.setStructureTransformer(new CraftStructureTransformer(handle, ChunkPos.containing(pos), blockTransformers, entityTransformers));

        this.structure.placeInWorld(accessor, pos, pos, definedstructureinfo, randomSource, Block.UPDATE_CLIENTS);
        accessor.getStructureTransformer().discard();
    }

    @Override
    public void fill(Location corner1, Location corner2, boolean includeEntities) {
        Preconditions.checkArgument(corner1 != null, "位置 corner1 不能为 null");
        Preconditions.checkArgument(corner2 != null, "位置 corner2 不能为 null");
        World world = corner1.getWorld();
        Preconditions.checkArgument(world != null, "corner1 Location 的世界不能为 null");

        Location origin = new Location(world, Math.min(corner1.getBlockX(), corner2.getBlockX()), Math.min(corner1.getBlockY(), corner2.getBlockY()), Math.min(corner1.getBlockZ(), corner2.getBlockZ()));
        BlockVector size = new BlockVector(Math.abs(corner1.getBlockX() - corner2.getBlockX()), Math.abs(corner1.getBlockY() - corner2.getBlockY()), Math.abs(corner1.getBlockZ() - corner2.getBlockZ()));
        this.fill(origin, size, includeEntities);
    }

    @Override
    public void fill(Location origin, BlockVector size, boolean includeEntities) {
        Preconditions.checkArgument(origin != null, "位置原点不能为 null");
        World world = origin.getWorld();
        Preconditions.checkArgument(world != null, "Location 原点的世界不能为 null");
        Preconditions.checkArgument(size != null, "BlockVector 的大小不能为 null");
        Preconditions.checkArgument(size.getBlockX() >= 1 && size.getBlockY() >= 1 && size.getBlockZ() >= 1, "尺寸至少为 1x1x1，但实际为 %sx%sx%s", size.getBlockX(), size.getBlockY(), size.getBlockZ());

        this.structure.fillFromWorld(((CraftWorld) world).getHandle(), CraftLocation.toBlockPos(origin), CraftBlockVector.toBlockPosition(size), includeEntities, List.of(Blocks.STRUCTURE_VOID));
    }

    @Override
    public BlockVector getSize() {
        return CraftBlockVector.toBukkit(this.structure.getSize());
    }

    @Override
    public List<Entity> getEntities() {
        List<Entity> entities = new ArrayList<>();
        for (StructureTemplate.StructureEntityInfo entity : this.structure.entityInfoList) {
            try (final ProblemReporter.ScopedCollector problemReporter = new ProblemReporter.ScopedCollector(
                () -> "entity@" + entity.pos, LOGGER
            )) {
                EntityType.create(
                    TagValueInput.createGlobal(problemReporter, entity.nbt),
                    ((CraftWorld) Bukkit.getServer().getWorlds().get(0)).getHandle(),
                    new EntitySpawnRequest(EntitySpawnReason.STRUCTURE, false)
                ).ifPresent(dummyEntity -> {
                    dummyEntity.setPos(entity.pos.x, entity.pos.y, entity.pos.z);
                    entities.add(dummyEntity.getBukkitEntity());
                });
            }
        }
        return Collections.unmodifiableList(entities);
    }

    @Override
    public int getEntityCount() {
        return this.structure.entityInfoList.size();
    }

    @Override
    public List<Palette> getPalettes() {
        return this.structure.palettes.stream().map((palette) -> new CraftPalette(palette, this.registry)).collect(Collectors.toList());
    }

    @Override
    public int getPaletteCount() {
        return this.structure.palettes.size();
    }

    @Override
    public PersistentDataContainer getPersistentDataContainer() {
        return this.getHandle().persistentDataContainer;
    }

    public StructureTemplate getHandle() {
        return this.structure;
    }
}
