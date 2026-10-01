package org.spigotmc;

import net.minecraft.server.MinecraftServer;

public class AsyncCatcher {

    public static void catchOp(String reason) {
        if (!ca.spottedleaf.moonrise.common.util.TickThread.isTickThread()) { // Paper - chunk system
            MinecraftServer.LOGGER.error("线程 {} 未通过主线程检查：{}", Thread.currentThread().getName(), reason, new Throwable()); // Paper
            throw new IllegalStateException("Asynchronous " + reason + "!");
        }
    }
}
