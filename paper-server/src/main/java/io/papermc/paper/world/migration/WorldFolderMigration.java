package io.papermc.paper.world.migration;

import com.mojang.logging.LogUtils;
import io.papermc.paper.world.saveddata.PaperLevelOverrides;
import io.papermc.paper.world.saveddata.PaperWorldMetadata;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import net.minecraft.core.HolderLookup;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.NbtAccounter;
import net.minecraft.nbt.NbtIo;
import net.minecraft.nbt.NbtUtils;
import net.minecraft.resources.ResourceKey;
import net.minecraft.util.filefix.FileFixerUpper;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.dimension.LevelStem;
import net.minecraft.world.level.levelgen.WorldGenSettings;
import net.minecraft.world.level.storage.LevelResource;
import net.minecraft.world.level.storage.LevelStorageSource;
import org.jspecify.annotations.NullMarked;
import org.slf4j.Logger;

@NullMarked
public final class WorldFolderMigration {
    private static final Logger LOGGER = LogUtils.getClassLogger();
    private static final boolean DISABLE_MIGRATION_DELAY = Boolean.getBoolean("paper.disableMigrationDelay");
    public static boolean didInitialLoad;
    private static boolean startupMigrationWarningShown;

    private WorldFolderMigration() {
    }

    private enum MigrationMode {
        LEGACY_CRAFTBUKKIT_MIGRATION,
        VANILLA_MIGRATION,
        NO_OP
    }

    public static void migrateStartupWorld(
        final LevelStorageSource.LevelStorageAccess rootAccess,
        final HolderLookup.Provider registryAccess,
        final String worldName,
        final ResourceKey<LevelStem> stemKey,
        final ResourceKey<Level> dimensionKey
    ) throws IOException {
        final WorldMigrationContext context = new WorldMigrationContext(rootAccess, registryAccess, worldName, stemKey, dimensionKey);
        final MigrationMode mode = classifyStartupMigration(context);
        if (mode != MigrationMode.NO_OP) {
            warnAndDelayStartupMigration();
        }
        switch (mode) {
            case LEGACY_CRAFTBUKKIT_MIGRATION -> LegacyCraftBukkitWorldMigration.migrate(context);
            case VANILLA_MIGRATION -> VanillaWorldMigration.migrate(context);
            case NO_OP -> {}
        }
    }

    public static void migrateApiWorld(
        final LevelStorageSource.LevelStorageAccess rootAccess,
        final HolderLookup.Provider registryAccess,
        final String worldName,
        final ResourceKey<LevelStem> stemKey,
        final ResourceKey<Level> dimensionKey
    ) throws IOException {
        LegacyCraftBukkitWorldMigration.migrateApiWorld(new WorldMigrationContext(rootAccess, registryAccess, worldName, stemKey, dimensionKey));
    }

    public static synchronized void warnAndDelayStartupMigration() {
        if (startupMigrationWarningShown) {
            return;
        }
        startupMigrationWarningShown = true;
        LOGGER.warn("===================== ! 警告 ! =====================");
        LOGGER.warn("启动期间需要进行世界存储迁移。");
        LOGGER.warn("如果你没有备份：请立即中断服务器。使用 Ctrl+C、面板的终止功能等。");
        LOGGER.warn("=====================================================");
        LOGGER.warn("将在 30 秒后继续...");
        if (DISABLE_MIGRATION_DELAY) {
            LOGGER.warn("迁移延迟已被系统属性禁用。");
        } else {
            try {
                Thread.sleep(30_000L);
            } catch (final InterruptedException ex) {
                Thread.currentThread().interrupt();
                throw new RuntimeException("启动世界迁移前的等待被中断", ex);
            }
        }
        LOGGER.info("继续执行启动世界迁移。");
    }

    private static MigrationMode classifyStartupMigration(final WorldMigrationContext context) {
        if (!context.rootAccess().hasWorldData()) {
            return MigrationMode.NO_OP;
        }
        if (!context.rootAccess().getLevelId().equals(context.worldName()) && Files.isDirectory(context.rootAccess().parent().getLevelPath(context.worldName()))) {
            return MigrationMode.LEGACY_CRAFTBUKKIT_MIGRATION;
        }
        if (hasCurrentPaperData(context.rootAccess(), context.dimensionKey())) {
            return MigrationMode.NO_OP;
        }
        // the dimension was deleted
        if (!Files.isDirectory(context.rootAccess().getDimensionPath(context.dimensionKey()))) {
            try {
                final CompoundTag rawLevelData = NbtIo.readCompressed(
                    context.rootAccess().getLevelDirectory().dataFile(), NbtAccounter.uncompressedQuota()
                );
                final int dataVersion = NbtUtils.getDataVersion(rawLevelData.getCompoundOrEmpty("Data"));
                if (dataVersion >= FileFixerUpper.FILE_FIXER_INTRODUCTION_VERSION) {
                    return MigrationMode.NO_OP;
                }
            } catch (final IOException ex) {
                throw new RuntimeException("读取世界迁移分类所需的 level data 失败", ex);
            }
        }
        return MigrationMode.VANILLA_MIGRATION;
    }

    static boolean hasCurrentPaperData(final LevelStorageSource.LevelStorageAccess rootAccess, final ResourceKey<Level> dimensionKey) {
        final Path targetDataRoot = rootAccess.getDimensionPath(dimensionKey).resolve(LevelResource.DATA.id());
        return Files.isRegularFile(WorldMigrationSupport.savedDataPath(targetDataRoot, PaperWorldMetadata.TYPE))
            && Files.isRegularFile(WorldMigrationSupport.savedDataPath(targetDataRoot, PaperLevelOverrides.TYPE))
            && Files.isRegularFile(WorldMigrationSupport.savedDataPath(targetDataRoot, WorldGenSettings.TYPE));
    }
}
