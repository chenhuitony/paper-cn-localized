package ca.spottedleaf.moonrise.common.util;

import ca.spottedleaf.concurrentutil.numa.OSNuma;
import ca.spottedleaf.moonrise.common.PlatformHooks;
import com.mojang.logging.LogUtils;
import org.slf4j.Logger;

public final class MoonriseConstants {

    private static final Logger LOGGER = LogUtils.getLogger();

    public static final int MAX_VIEW_DISTANCE = Integer.getInteger(PlatformHooks.get().getBrand() + ".MaxViewDistance", 32);
    public static final boolean NUMA_ENABLE;
    static {
        final boolean numaScheduling = Boolean.getBoolean(PlatformHooks.get().getBrand() + ".NumaScheduling");
        if (!numaScheduling) {
            NUMA_ENABLE = false;
            if (OSNuma.getNativeInstance().isAvailable()) {
                LOGGER.info("未设置 NUMA 启用标志，但当前操作系统支持 NUMA 交互。");
                LOGGER.info("检测到 " + OSNuma.getNativeInstance().getTotalNumaNodes() + " 个 NUMA 节点。");
            }
        } else {
            final OSNuma numa = OSNuma.getNativeInstance();
            if (!numa.isAvailable()) {
                NUMA_ENABLE = false;
                LOGGER.info("已设置 NUMA 启用标志，但当前操作系统不支持 NUMA 交互。");
            } else {
                NUMA_ENABLE = true;

                final int totalNodes = numa.getTotalNumaNodes();
                LOGGER.info("已设置 NUMA 启用标志。检测到 " + totalNodes + " 个 NUMA 节点、" + numa.getTotalCores() + " 个虚拟核心。");
            }
        }
    }

    private MoonriseConstants() {}
}
