package io.papermc.paper.world.migration;

import com.mojang.logging.LogUtils;
import com.mojang.serialization.Dynamic;
import io.papermc.paper.world.saveddata.PaperWorldPDC;
import java.io.DataInputStream;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;
import java.util.List;
import java.util.UUID;
import net.minecraft.core.HolderLookup;
import net.minecraft.nbt.NbtException;
import net.minecraft.nbt.NbtOps;
import net.minecraft.nbt.ReportedNbtException;
import net.minecraft.resources.Identifier;
import net.minecraft.util.datafix.DataFixers;
import net.minecraft.util.worldupdate.UpgradeProgress;
import net.minecraft.world.level.saveddata.SavedDataType;
import net.minecraft.world.level.storage.LevelStorageSource;
import net.minecraft.world.level.storage.LevelSummary;
import org.jspecify.annotations.NullMarked;
import org.jspecify.annotations.Nullable;
import org.slf4j.Logger;

@NullMarked
final class WorldMigrationSupport {
    private static final Logger LOGGER = LogUtils.getClassLogger();
    static final List<String> DIMENSION_DIRECTORIES = List.of("region", "entities", "poi");
    static final String PAPER_WORLD_CONFIG = "paper-world.yml";
    static final String LEGACY_UID_FILE_NAME = "uid.dat";

    private WorldMigrationSupport() {
    }

    static @Nullable PaperWorldPDC readLegacyPdc(final @Nullable Dynamic<?> levelData, final HolderLookup.Provider registryAccess) {
        if (levelData == null) {
            return null;
        }

        return levelData.get("BukkitValues")
            .result()
            .flatMap(dynamic -> PaperWorldPDC.CODEC.parse(registryAccess.createSerializationContext(NbtOps.INSTANCE), dynamic.convert(NbtOps.INSTANCE).getValue()).result())
            .orElse(null);
    }

    static void clearLegacyPdc(final Dynamic<?> levelData) {
        levelData.remove("BukkitValues");
    }

    static @Nullable UUID readLegacyUuid(final Path sourceRoot) {
        final Path fileId = sourceRoot.resolve(LEGACY_UID_FILE_NAME);
        if (!Files.isRegularFile(fileId)) {
            return null;
        }

        try (DataInputStream inputStream = new DataInputStream(Files.newInputStream(fileId))) {
            return new UUID(inputStream.readLong(), inputStream.readLong());
        } catch (final IOException ex) {
            LOGGER.warn("读取 {} 失败", fileId, ex);
            return null;
        }
    }

    static Path getStorageFolder(final Identifier dimension, final Path baseFolder) {
        return dimension.resolveAgainst(baseFolder.resolve("dimensions"));
    }

    static void migratePaperWorldConfig(final Path sourceRoot, final Path targetDimensionPath) throws IOException {
        final Path source = sourceRoot.resolve(PAPER_WORLD_CONFIG);
        if (!Files.isRegularFile(source)) {
            return;
        }

        final Path target = targetDimensionPath.resolve(PAPER_WORLD_CONFIG);
        if (Files.exists(target)) {
            return;
        }

        Files.createDirectories(target.getParent());
        LOGGER.info("正在将 Paper 世界配置从 {} 迁移到 {}", source, target);
        Files.move(source, target);
    }

    static void migrateDimensionDirectories(final Path sourceDimensionRoot, final Path targetDimensionPath) throws IOException {
        if (sourceDimensionRoot.equals(targetDimensionPath)) {
            return;
        }

        for (final String directory : DIMENSION_DIRECTORIES) {
            final Path source = sourceDimensionRoot.resolve(directory);
            if (!Files.exists(source)) {
                continue;
            }

            final Path target = targetDimensionPath.resolve(directory);
            LOGGER.info("正在将世界目录从 {} 迁移到 {}", source, target);
            mergeMove(source, target);
        }
    }

    private static void mergeMove(final Path source, final Path target) throws IOException {
        if (Files.isDirectory(source)) {
            Files.createDirectories(target);
            try (final var entries = Files.list(source)) {
                for (final Path child : entries.toList()) {
                    mergeMove(child, target.resolve(child.getFileName().toString()));
                }
            }
            tryDeleteIfEmpty(source);
            return;
        }

        if (Files.exists(target)) {
            throw new IOException("迁移文件 " + source + " 时，拒绝覆盖已存在的 " + target);
        }

        Files.createDirectories(target.getParent());
        Files.move(source, target);
    }

    private static void tryDeleteIfEmpty(final Path path) throws IOException {
        try (final var entries = Files.list(path)) {
            if (entries.findAny().isPresent()) {
                return;
            }
        }
        Files.deleteIfExists(path);
    }

    record LevelDataResult(@Nullable Dynamic<?> dataTag, boolean fatalError) {}

    static LevelDataResult readFixedLevelData(final LevelStorageSource.LevelStorageAccess access) {
        if (!access.hasWorldData()) {
            return new LevelDataResult(null, false);
        }

        final Dynamic<?> levelDataUnfixed;
        try {
            levelDataUnfixed = access.getUnfixedDataTagWithFallback();
        } catch (final NbtException | ReportedNbtException | IOException ex) {
            LOGGER.error("加载世界数据失败。世界文件可能已损坏。正在关闭服务器。", ex);
            return new LevelDataResult(null, true);
        }

        final LevelSummary summary = access.fixAndGetSummaryFromTag(levelDataUnfixed);
        if (summary.requiresManualConversion()) {
            LOGGER.info("此世界必须在更旧版本（如 1.6.4）中打开，才能安全转换");
            return new LevelDataResult(null, true);
        }

        if (!summary.isCompatible()) {
            LOGGER.info("此世界由不兼容的版本创建。");
            return new LevelDataResult(null, true);
        }

        return new LevelDataResult(DataFixers.getFileFixer().fix(access, levelDataUnfixed, new UpgradeProgress()), false);
    }

    static Path savedDataPath(final Path dataRoot, final SavedDataType<?> type) {
        return type.id().withSuffix(".dat").resolveAgainst(dataRoot);
    }

    static boolean copySavedDataIfPresent(
        final List<Path> sourceDataRoots,
        final Path targetDataRoot,
        final SavedDataType<?> type,
        final boolean overwrite
    ) throws IOException {
        return copySavedDataFileIfPresent(targetDataRoot, findSavedDataFile(sourceDataRoots, type), type, overwrite);
    }

    static boolean copySavedDataFileIfPresent(
        final Path targetDataRoot,
        final @Nullable Path source,
        final SavedDataType<?> type,
        final boolean overwrite
    ) throws IOException {
        if (source == null) {
            return false;
        }

        final Path target = savedDataPath(targetDataRoot, type);
        if (!overwrite && Files.isRegularFile(target)) {
            return true;
        }

        Files.createDirectories(target.getParent());
        Files.copy(source, target, StandardCopyOption.REPLACE_EXISTING, StandardCopyOption.COPY_ATTRIBUTES);
        return true;
    }

    static @Nullable Path findSavedDataFile(final List<Path> dataRoots, final SavedDataType<?> type) {
        for (final Path dataRoot : dataRoots) {
            final Path source = savedDataPath(dataRoot, type);
            if (Files.isRegularFile(source)) {
                return source;
            }
        }
        return null;
    }

}
