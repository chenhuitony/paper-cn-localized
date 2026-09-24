package ca.spottedleaf.moonrise.common.util;

import ca.spottedleaf.concurrentutil.executor.thread.BalancedPrioritisedThreadPool;
import ca.spottedleaf.concurrentutil.numa.OSNuma;
import ca.spottedleaf.moonrise.common.PlatformHooks;
import com.mojang.logging.LogUtils;
import org.slf4j.Logger;
import java.util.concurrent.ThreadFactory;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.function.Consumer;

public final class MoonriseCommon {

    private static final Logger LOGGER = LogUtils.getClassLogger();

    public static final long WORKER_QUEUE_HOLD_TIME = (long)(20.0e6); // 20ms
    public static final BalancedPrioritisedThreadPool WORKER_POOL = new BalancedPrioritisedThreadPool(
        WORKER_QUEUE_HOLD_TIME,
        new ThreadFactory() {
            private final AtomicInteger idGenerator = new AtomicInteger();

            @Override
            public Thread newThread(final Runnable run) {
                final Thread thread = new Thread(run, PlatformHooks.get().getBrand() + " Common Worker #" + this.idGenerator.getAndIncrement());

                thread.setDaemon(true);
                thread.setUncaughtExceptionHandler(new Thread.UncaughtExceptionHandler() {
                    @Override
                    public void uncaughtException(final Thread thread, final Throwable throwable) {
                        LOGGER.error("线程 " + thread.getName() + " 中发生未捕获的异常", throwable);
                    }
                });

                return thread;
            }
        }
    );
    public static final BalancedPrioritisedThreadPool.OrderedStreamGroup CLIENT_GROUP = MoonriseCommon.WORKER_POOL.createOrderedStreamGroup();
    public static final BalancedPrioritisedThreadPool.OrderedStreamGroup SERVER_GROUP = MoonriseCommon.WORKER_POOL.createOrderedStreamGroup();

    public static void adjustWorkerThreads(final int configWorkerThreads, final int configIoThreads) {
        int defaultWorkerThreads = OSNuma.getNativeInstance().getTotalCores()  / 2;
        if (defaultWorkerThreads <= 4) {
            defaultWorkerThreads = defaultWorkerThreads <= 3 ? 1 : 2;
        } else {
            defaultWorkerThreads = defaultWorkerThreads / 2;
        }
        defaultWorkerThreads = Integer.getInteger(PlatformHooks.get().getBrand() + ".WorkerThreadCount", Integer.valueOf(defaultWorkerThreads));

        int workerThreads = configWorkerThreads;

        if (workerThreads <= 0) {
            workerThreads = defaultWorkerThreads;
        }

        final int ioThreads = Math.max(1, configIoThreads);

        WORKER_POOL.adjustThreadCount(workerThreads);
        IO_POOL.adjustThreadCount(ioThreads);

        LOGGER.info(PlatformHooks.get().getBrand() + " 正在使用 " + workerThreads + " 个工作线程、" + ioThreads + " 个输入输出线程");
    }

    public static final long IO_QUEUE_HOLD_TIME = (long)(25.0e6); // 25ms
    public static final BalancedPrioritisedThreadPool IO_POOL = new BalancedPrioritisedThreadPool(
        IO_QUEUE_HOLD_TIME,
        new ThreadFactory() {
                private final AtomicInteger idGenerator = new AtomicInteger();

                @Override
                public Thread newThread(final Runnable run) {
                    final Thread thread = new Thread(run, PlatformHooks.get().getBrand() + " I/O Worker #" + this.idGenerator.getAndIncrement());

                    thread.setDaemon(true);
                    thread.setUncaughtExceptionHandler(new Thread.UncaughtExceptionHandler() {
                        @Override
                        public void uncaughtException(final Thread thread, final Throwable throwable) {
                            LOGGER.error("线程 " + thread.getName() + " 中发生未捕获的异常", throwable);
                        }
                    });

                    return thread;
                }
            }
    );
    public static final BalancedPrioritisedThreadPool.OrderedStreamGroup CLIENT_IO_GROUP = IO_POOL.createOrderedStreamGroup();
    public static final BalancedPrioritisedThreadPool.OrderedStreamGroup SERVER_IO_GROUP = IO_POOL.createOrderedStreamGroup();

    public static void haltExecutors() {
        MoonriseCommon.WORKER_POOL.shutdown(false);
        LOGGER.info("正在等待工作线程池终止，最多等待 60 秒...");
        if (!MoonriseCommon.WORKER_POOL.join(TimeUnit.SECONDS.toMillis(60L))) {
            LOGGER.error("工作线程池未能在规定时间内关闭！");
            MoonriseCommon.WORKER_POOL.halt(false);
        }

        MoonriseCommon.IO_POOL.shutdown(false);
        LOGGER.info("正在等待输入输出线程池终止，最多等待 60 秒...");
        if (!MoonriseCommon.IO_POOL.join(TimeUnit.SECONDS.toMillis(60L))) {
            LOGGER.error("输入输出线程池未能在规定时间内关闭！");
            MoonriseCommon.IO_POOL.halt(false);
        }
    }

    private MoonriseCommon() {}
}
