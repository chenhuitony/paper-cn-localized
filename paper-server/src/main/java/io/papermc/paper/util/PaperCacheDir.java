package io.papermc.paper.util;

import com.mojang.logging.LogUtils;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import org.slf4j.Logger;

public final class PaperCacheDir {

    private static final Path PATH = Path.of(".paper");
    private static final Logger LOGGER = LogUtils.getLogger();

    public static Path get() {
        if (!Files.exists(PATH)) {
            try {
                Files.createDirectories(PATH);
            } catch (final IOException e) {
                throw new RuntimeException("创建 .paper 缓存目录时出错", e);
            }
        }
        if (!Files.isDirectory(PATH)) {
            throw new RuntimeException(".paper 缓存目录不是一个目录");
        }
        return PATH;
    }

    public static Path get(final String child) {
        return get().resolve(child);
    }

    public static Path moveFromServerRootAndGet(final String child, final String newName) {
        // Keep this for individual use until a more unified migration place is made for larger config migrations
        final Path path = Path.of(child);
        final Path target = get(newName);
        if (!Files.isRegularFile(path)) {
            return target;
        }

        if (Files.exists(target)) {
            // Delete the one in the server root
            try {
                Files.deleteIfExists(path);
            } catch (final IOException e) {
                LOGGER.error("删除文件时出错：{}", child, e);
            }
        } else {
            // Move into .paper
            try {
                Files.move(path, target);
            } catch (final IOException e) {
                LOGGER.error("移动文件时出错：{}", child, e);
            }
        }
        return target;
    }
}
