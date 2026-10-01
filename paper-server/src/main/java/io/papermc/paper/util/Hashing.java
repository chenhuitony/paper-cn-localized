package io.papermc.paper.util;

import com.google.common.hash.HashCode;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Locale;
import org.apache.commons.io.IOUtils;
import org.checkerframework.checker.nullness.qual.NonNull;
import org.checkerframework.framework.qual.DefaultQualifier;

@DefaultQualifier(NonNull.class)
public final class Hashing {
    private Hashing() {
    }

    /**
     * Hash the provided {@link InputStream} using SHA-256. Stream will be closed.
     *
     * @param stream input stream
     * @return SHA-256 hash string
     */
    public static String sha256(final InputStream stream) {
        try (stream) {
            return com.google.common.hash.Hashing.sha256().hashBytes(IOUtils.toByteArray(stream)).toString().toUpperCase(Locale.ROOT);
        } catch (final IOException ex) {
            throw new RuntimeException("计算 InputStream 的哈希失败", ex);
        }
    }

    /**
     * Hash the provided file using SHA-256.
     *
     * @param file file
     * @return SHA-256 hash string
     */
    public static String sha256(final Path file) {
        if (!Files.isRegularFile(file)) {
            throw new IllegalArgumentException("'" + file + "' 不是一个常规文件！");
        }
        final HashCode hash;
        try {
            hash = com.google.common.io.Files.asByteSource(file.toFile()).hash(com.google.common.hash.Hashing.sha256());
        } catch (final IOException ex) {
            throw new RuntimeException("计算文件的哈希失败：'" + file + "'", ex);
        }
        return hash.toString().toUpperCase(Locale.ROOT);
    }
}
