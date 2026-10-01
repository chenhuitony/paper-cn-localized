package io.papermc.paper.plugin;

import com.mojang.logging.LogUtils;
import io.papermc.paper.configuration.PaperConfigurations;
import io.papermc.paper.plugin.entrypoint.Entrypoint;
import io.papermc.paper.plugin.entrypoint.LaunchEntryPointHandler;
import io.papermc.paper.plugin.provider.PluginProvider;
import io.papermc.paper.plugin.provider.type.paper.PaperPluginParent;
import io.papermc.paper.plugin.provider.type.spigot.SpigotPluginProvider;
import java.util.Set;
import java.util.TreeSet;
import joptsimple.OptionSet;
import net.minecraft.server.dedicated.DedicatedServer;
import org.bukkit.configuration.file.YamlConfiguration;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;
import org.slf4j.Logger;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class PluginInitializerManager {

    private static final Logger LOGGER = LogUtils.getClassLogger();
    private static PluginInitializerManager impl;
    private final Path pluginDirectory;
    private final Path updateDirectory;

    PluginInitializerManager(final Path pluginDirectory, final Path updateDirectory) {
        this.pluginDirectory = pluginDirectory;
        this.updateDirectory = updateDirectory;
    }

    private static PluginInitializerManager parse(@NotNull final OptionSet minecraftOptionSet) throws Exception {
        // We have to load the bukkit configuration inorder to get the update folder location.
        final File configFileLocationBukkit = (File) minecraftOptionSet.valueOf("bukkit-settings");

        final Path pluginDirectory = ((File) minecraftOptionSet.valueOf("plugins")).toPath();

        final YamlConfiguration configuration = PaperConfigurations.loadLegacyConfigFile(configFileLocationBukkit);

        final String updateDirectoryName = configuration.getString("settings.update-folder", "update");
        if (updateDirectoryName.isBlank()) {
            return new PluginInitializerManager(pluginDirectory, null);
        }

        final Path resolvedUpdateDirectory = pluginDirectory.resolve(updateDirectoryName);
        if (!Files.isDirectory(resolvedUpdateDirectory)) {
            if (Files.exists(resolvedUpdateDirectory)) {
                LOGGER.error("更新目录配置有误！");
                LOGGER.error("你在 bukkit.yml 中配置的更新目录（{}）指向了一个非目录路径。 " +
                    "自动更新功能将无法工作。", resolvedUpdateDirectory);
            }
            return new PluginInitializerManager(pluginDirectory, null);
        }

        boolean isSameFile;
        try {
            isSameFile = Files.isSameFile(resolvedUpdateDirectory, pluginDirectory);
        } catch (final IOException e) {
            LOGGER.error("更新目录配置有误！");
            LOGGER.error("比较更新目录与插件目录失败", e);
            return new PluginInitializerManager(pluginDirectory, null);
        }

        if (isSameFile) {
            LOGGER.error("更新目录配置有误！");
            LOGGER.error(("你在 bukkit.yml 中配置的更新目录（%s）指向了与插件目录（%s）相同的位置。 " +
                "自动更新功能将被禁用。").formatted(resolvedUpdateDirectory, pluginDirectory));

            return new PluginInitializerManager(pluginDirectory, null);
        }

        return new PluginInitializerManager(pluginDirectory, resolvedUpdateDirectory);
    }

    public static PluginInitializerManager init(final OptionSet optionSet) throws Exception {
        impl = parse(optionSet);
        return impl;
    }

    public static PluginInitializerManager instance() {
        return impl;
    }

    @NotNull
    public Path pluginDirectoryPath() {
        return pluginDirectory;
    }

    @Nullable
    public Path pluginUpdatePath() {
        return updateDirectory;
    }

    public static void load(OptionSet optionSet) throws Exception {
        LOGGER.info("正在初始化插件...");
        // We have to load the bukkit configuration inorder to get the update folder location.
        io.papermc.paper.plugin.PluginInitializerManager pluginSystem = io.papermc.paper.plugin.PluginInitializerManager.init(optionSet);

        // Register the default plugin directory
        io.papermc.paper.plugin.util.EntrypointUtil.registerProvidersFromSource(io.papermc.paper.plugin.provider.source.DirectoryProviderSource.INSTANCE, pluginSystem.pluginDirectoryPath());

        // Register plugins from the flag
        @SuppressWarnings("unchecked")
        java.util.List<Path> files = ((java.util.List<File>) optionSet.valuesOf("add-plugin")).stream().map(File::toPath).toList();
        io.papermc.paper.plugin.util.EntrypointUtil.registerProvidersFromSource(io.papermc.paper.plugin.provider.source.PluginFlagProviderSource.INSTANCE, files);

        @SuppressWarnings("unchecked")
        java.util.List<Path> dirs = ((java.util.List<File>) optionSet.valuesOf("add-plugin-dir")).stream().map(File::toPath).toList();
        dirs.forEach(pluginDir -> io.papermc.paper.plugin.util.EntrypointUtil.registerProvidersFromSource(io.papermc.paper.plugin.provider.source.DirectoryProviderSource.INSTANCE_NO_CREATE, pluginDir));

        final Set<String> paperPluginNames = new TreeSet<>();
        final Set<String> legacyPluginNames = new TreeSet<>();
        LaunchEntryPointHandler.INSTANCE.getStorage().forEach((entrypoint, providerStorage) -> {
            providerStorage.getRegisteredProviders().forEach(provider -> {
                if (provider instanceof final SpigotPluginProvider legacy) {
                    legacyPluginNames.add(String.format("%s (%s)", legacy.getMeta().getName(), legacy.getMeta().getVersion()));
                } else if (provider instanceof final PaperPluginParent.PaperServerPluginProvider paper) {
                    paperPluginNames.add(String.format("%s (%s)", provider.getMeta().getName(), provider.getMeta().getVersion()));
                }
            });
        });
        final int total = paperPluginNames.size() + legacyPluginNames.size();
        LOGGER.info("已初始化 {} 个插件", total);
        if (!paperPluginNames.isEmpty()) {
            if (LOGGER.isDebugEnabled()) {
                LOGGER.info("Paper 插件（{}）：\n - {}", paperPluginNames.size(), String.join("\n - ", paperPluginNames));
            } else {
                LOGGER.info("Paper 插件（{}）：\n - {}", paperPluginNames.size(), String.join(", ", paperPluginNames));
            }
        }
        if (!legacyPluginNames.isEmpty()) {
            if (LOGGER.isDebugEnabled()) {
                LOGGER.info("Bukkit 插件（{}）：\n - {}", legacyPluginNames.size(), String.join("\n - ", legacyPluginNames));
            } else {
                LOGGER.info("Bukkit 插件（{}）：\n - {}", legacyPluginNames.size(), String.join(", ", legacyPluginNames));
            }
        }
    }

    // This will be the end of me...
    public static void reload(DedicatedServer dedicatedServer) {
        // Wipe the provider storage
        LaunchEntryPointHandler.INSTANCE.populateProviderStorage();
        try {
            load(dedicatedServer.options);
        } catch (Exception e) {
            throw new RuntimeException("重载失败！", e);
        }

        boolean hasPaperPlugin = false;
        for (PluginProvider<?> provider : LaunchEntryPointHandler.INSTANCE.getStorage().get(Entrypoint.PLUGIN).getRegisteredProviders()) {
            if (provider instanceof PaperPluginParent.PaperServerPluginProvider) {
                hasPaperPlugin = true;
                break;
            }
        }

        if (hasPaperPlugin) {
            LOGGER.warn("======== 警告 ========");
            LOGGER.warn("你的服务器上安装了 Paper 插件，而你正在执行重载。");
            LOGGER.warn("Paper 插件不支持被重载。这会导致一些意外问题。");
            LOGGER.warn("=========================");
        }
    }
}
