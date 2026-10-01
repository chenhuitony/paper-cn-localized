package org.bukkit.craftbukkit;

import java.io.File;
import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;
import joptsimple.OptionParser;
import joptsimple.OptionSet;
import joptsimple.util.PathConverter;

import static java.util.Arrays.asList;

public class Main {
    public static final java.time.Instant BOOT_TIME = java.time.Instant.now(); // Paper - track initial start time
    public static boolean useJline = true;
    public static boolean useConsole = true;

    // Paper start - Reset loggers after shutdown
    static {
        System.setProperty("java.util.logging.manager", "io.papermc.paper.log.CustomLogManager");
    }
    // Paper end - Reset loggers after shutdown

    public static void main(String[] args) {
        if (System.getProperty("jdk.nio.maxCachedBufferSize") == null) System.setProperty("jdk.nio.maxCachedBufferSize", "262144"); // Paper - cap per-thread NIO cache size; https://www.evanjones.ca/java-bytebuffer-leak.html
        OptionParser parser = new OptionParser() {
            {
                this.acceptsAll(asList("?", "help"), "显示帮助");

                this.acceptsAll(asList("c", "config"), "要使用的属性文件")
                        .withRequiredArg()
                        .ofType(File.class)
                        .defaultsTo(new File("server.properties"))
                        .describedAs("属性文件");

                this.acceptsAll(asList("P", "plugins"), "要使用的插件目录")
                        .withRequiredArg()
                        .ofType(File.class)
                        .defaultsTo(new File("plugins"))
                        .describedAs("插件目录");

                this.acceptsAll(asList("h", "host", "server-ip"), "监听的主机地址")
                        .withRequiredArg()
                        .ofType(String.class)
                        .describedAs("主机名或 IP");

                this.acceptsAll(asList("W", "world-dir", "universe", "world-container"), "世界容器")
                        .withRequiredArg()
                        .ofType(File.class)
                        .defaultsTo(new File("."))
                        .describedAs("存放世界的目录");

                this.acceptsAll(asList("w", "world", "level-name"), "世界名称")
                        .withRequiredArg()
                        .ofType(String.class)
                        .describedAs("世界名称");

                this.acceptsAll(asList("p", "port", "server-port"), "监听端口")
                        .withRequiredArg()
                        .ofType(Integer.class)
                        .describedAs("Port");

                this.accepts("serverId", "服务端 ID")
                        .withRequiredArg();

                this.accepts("jfrProfile", "启用 JFR 性能分析");

                this.accepts("pidFile", "PID 文件")
                        .withRequiredArg()
                        .withValuesConvertedBy(new PathConverter());

                this.acceptsAll(asList("o", "online-mode"), "是否使用在线验证")
                        .withRequiredArg()
                        .ofType(Boolean.class)
                        .describedAs("Authentication");

                this.acceptsAll(asList("s", "size", "max-players"), "最大玩家数量")
                        .withRequiredArg()
                        .ofType(Integer.class)
                        .describedAs("服务端大小");

                this.acceptsAll(asList("b", "bukkit-settings"), "bukkit 配置文件")
                        .withRequiredArg()
                        .ofType(File.class)
                        .defaultsTo(new File("bukkit.yml"))
                        .describedAs("Yml 文件");

                this.acceptsAll(asList("C", "commands-settings"), "命令配置文件")
                        .withRequiredArg()
                        .ofType(File.class)
                        .defaultsTo(new File("commands.yml"))
                        .describedAs("Yml 文件");

                this.accepts("forceUpgrade", "是否强制升级世界");
                this.accepts("eraseCache", "是否在世界升级期间强制清除缓存");
                this.accepts("recreateRegionFiles", "是否在世界升级期间重新创建区域文件");
                this.accepts("safeMode", "仅使用原版数据包加载世界"); // Paper
                this.accepts("nogui", "禁用图形化控制台");

                this.accepts("nojline", "禁用 jline 并模拟原版控制台");

                this.accepts("noconsole", "禁用控制台");

                this.acceptsAll(asList("v", "version"), "显示 CraftBukkit 版本");

                this.accepts("demo", "演示模式");

                this.accepts("bonusChest", "启用奖励箱子");

                this.accepts("initSettings", "仅生成配置文件后退出"); // SPIGOT-5761: Add initSettings option

                this.acceptsAll(asList("S", "spigot-settings"), "spigot 配置文件")
                        .withRequiredArg()
                        .ofType(File.class)
                        .defaultsTo(new File("spigot.yml"))
                        .describedAs("Yml 文件");

                this.acceptsAll(asList("paper-dir", "paper-settings-directory"), "Paper 配置文件目录")
                        .withRequiredArg()
                        .ofType(File.class)
                        .defaultsTo(new File(io.papermc.paper.configuration.PaperConfigurations.CONFIG_DIR))
                        .describedAs("配置目录");

                this.acceptsAll(asList("paper", "paper-settings"), "Paper 配置文件")
                        .withRequiredArg()
                        .ofType(File.class)
                        .defaultsTo(new File("paper.yml"))
                        .describedAs("Yml 文件");

                this.acceptsAll(asList("add-plugin", "add-extra-plugin-jar"), "指定除 plugins 文件夹外还要加载的额外插件 Jar 路径。此参数可多次指定，每次指定一个额外插件 Jar 路径。")
                        .withRequiredArg()
                        .ofType(File.class)
                        .defaultsTo(new File[] {})
                        .describedAs("Jar 文件");

                this.acceptsAll(asList("add-plugin-dir", "add-extra-plugin-dir"), "指定除 plugins 文件夹外还要加载的额外插件目录路径。此参数可多次指定，每次指定一个额外插件目录路径。")
                        .withRequiredArg()
                        .ofType(File.class)
                        .defaultsTo(new File[] {})
                        .describedAs("插件目录");

                this.accepts("server-name", "服务端名称")
                        .withRequiredArg()
                        .ofType(String.class)
                        .defaultsTo("未知服务器")
                        .describedAs("Name");
            }
        };

        OptionSet options = null;

        try {
            options = parser.parse(args);
        } catch (joptsimple.OptionException ex) {
            Logger.getLogger(Main.class.getName()).log(Level.SEVERE, ex.getLocalizedMessage());
        }

        if ((options == null) || (options.has("?"))) {
            try {
                parser.printHelpOn(System.out);
            } catch (IOException ex) {
                Logger.getLogger(Main.class.getName()).log(Level.SEVERE, null, ex);
            }
        } else if (options.has("v")) {
            System.out.println(CraftServer.class.getPackage().getImplementationVersion());
        } else {
            // Do you love Java using + and ! as string based identifiers? I sure do!
            String path = new File(".").getAbsolutePath();
            if (path.contains("!") || path.contains("+")) {
                System.err.println("无法在路径名中包含 ! 或 + 的目录下运行服务端。请重命名受影响的文件夹后重试。");
                return;
            }

            // Paper start - Improve java version check
            boolean skip = Boolean.getBoolean("Paper.IgnoreJavaVersion");
            String javaVersionName = System.getProperty("java.version");
            // J2SE SDK/JRE Version String Naming Convention
            boolean isPreRelease = javaVersionName.contains("-");
            if (isPreRelease) {
                if (!skip) {
                    System.err.println("检测到不支持的 Java 版本（" + javaVersionName + "）。你正在运行一个不受支持的非官方版本。仅支持正式发布版（GA）的 Java。请升级你的 Java 版本。更多信息请参见 https://docs.papermc.io/paper/faq#unsupported-java-detected-what-do-i-do");
                    return;
                }

                System.err.println("检测到不支持的 Java 版本（"+ javaVersionName + "），但已跳过检查。请谨慎继续！ ");
            }
            // Paper end - Improve java version check

            try {
                if (options.has("nojline")) {
                    System.setProperty(net.minecrell.terminalconsole.TerminalConsoleAppender.JLINE_OVERRIDE_PROPERTY, "false");
                    useJline = false;
                }

                if (options.has("noconsole")) {
                    Main.useConsole = false;
                    useJline = false; // Paper
                    System.setProperty(net.minecrell.terminalconsole.TerminalConsoleAppender.JLINE_OVERRIDE_PROPERTY, "false"); // Paper
                }

                System.setProperty("library.jansi.version", "Paper"); // Paper - set meaningless jansi version to prevent git builds from crashing on Windows
                System.setProperty("jdk.console", "java.base"); // Paper - revert default console provider back to java.base so we can have our own jline

                io.papermc.paper.PaperBootstrap.boot(options);
            } catch (Throwable t) {
                t.printStackTrace();
            }
        }
    }
}
