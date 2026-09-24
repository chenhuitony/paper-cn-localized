package io.papermc.paper.plugin;

import io.papermc.paper.plugin.configuration.PluginMeta;
import org.bukkit.Server;
import org.bukkit.command.Command;
import org.bukkit.command.CommandSender;
import org.bukkit.configuration.file.FileConfiguration;
import org.bukkit.generator.BiomeProvider;
import org.bukkit.generator.ChunkGenerator;
import org.bukkit.plugin.PluginBase;
import org.bukkit.plugin.PluginDescriptionFile;
import org.bukkit.plugin.PluginLoader;
import org.bukkit.plugin.PluginLogger;

import java.io.File;
import java.io.InputStream;
import java.util.List;

public class PaperTestPlugin extends PluginBase {
    private final String pluginName;
    private boolean enabled = true;
    private final PluginMeta configuration;

    public PaperTestPlugin(String pluginName) {
        this.pluginName = pluginName;
        this.configuration = new TestPluginMeta(pluginName);
    }

    public PaperTestPlugin(PluginMeta configuration) {
        this.configuration = configuration;
        this.pluginName = configuration.getName();
    }

    @Override
    public File getDataFolder() {
        throw new UnsupportedOperationException("不支持。");
    }

    @Override
    public PluginDescriptionFile getDescription() {
        throw new UnsupportedOperationException("不支持。");
    }

    @Override
    public PluginMeta getPluginMeta() {
        return this.configuration;
    }

    @Override
    public FileConfiguration getConfig() {
        throw new UnsupportedOperationException("不支持。");
    }

    @Override
    public InputStream getResource(String filename) {
        throw new UnsupportedOperationException("不支持。");
    }

    @Override
    public void saveConfig() {
        throw new UnsupportedOperationException("不支持。");
    }

    @Override
    public void saveDefaultConfig() {
        throw new UnsupportedOperationException("不支持。");
    }

    @Override
    public void saveResource(String resourcePath, boolean replace) {
        throw new UnsupportedOperationException("不支持。");
    }

    @Override
    public void reloadConfig() {
        throw new UnsupportedOperationException("不支持。");
    }

    @Override
    public PluginLogger getLogger() {
        throw new UnsupportedOperationException("不支持。");
    }

    @Override
    public PluginLoader getPluginLoader() {
        throw new UnsupportedOperationException("不支持。");
    }

    @Override
    public Server getServer() {
        throw new UnsupportedOperationException("不支持。");
    }

    @Override
    public boolean isEnabled() {
        return enabled;
    }

    public void setEnabled(boolean enabled) {
        this.enabled = enabled;
    }

    @Override
    public void onDisable() {
        throw new UnsupportedOperationException("不支持。");
    }

    @Override
    public void onLoad() {
    }

    @Override
    public void onEnable() {
        throw new UnsupportedOperationException("不支持。");
    }

    @Override
    public boolean isNaggable() {
        throw new UnsupportedOperationException("不支持。");
    }

    @Override
    public void setNaggable(boolean canNag) {
        throw new UnsupportedOperationException("不支持。");
    }

    @Override
    public ChunkGenerator getDefaultWorldGenerator(String worldName, String id) {
        throw new UnsupportedOperationException("不支持。");
    }

    @Override
    public BiomeProvider getDefaultBiomeProvider(String worldName, String id) {
        throw new UnsupportedOperationException("不支持。");
    }

    @Override
    public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {
        throw new UnsupportedOperationException("不支持。");
    }

    @Override
    public List<String> onTabComplete(CommandSender sender, Command command, String alias, String[] args) {
        throw new UnsupportedOperationException("不支持。");
    }

    // Paper start - lifecycle events
    @Override
    public io.papermc.paper.plugin.lifecycle.event.LifecycleEventManager<org.bukkit.plugin.Plugin> getLifecycleManager() {
        throw new UnsupportedOperationException("不支持。");
    }
    // Paper end - lifecycle events
}
