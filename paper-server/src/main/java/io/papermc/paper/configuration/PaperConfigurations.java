package io.papermc.paper.configuration;

import com.google.common.base.Suppliers;
import com.google.common.collect.Table;
import com.mojang.logging.LogUtils;
import io.leangen.geantyref.TypeToken;
import io.papermc.paper.configuration.legacy.RequiresSpigotInitialization;
import io.papermc.paper.configuration.mapping.Definition;
import io.papermc.paper.configuration.mapping.FieldProcessor;
import io.papermc.paper.configuration.mapping.InnerClassFieldDiscoverer;
import io.papermc.paper.configuration.mapping.MergeMap;
import io.papermc.paper.configuration.serializer.ComponentSerializer;
import io.papermc.paper.configuration.serializer.EnumValueSerializer;
import io.papermc.paper.configuration.serializer.IdentifierSerializer;
import io.papermc.paper.configuration.serializer.NbtPathSerializer;
import io.papermc.paper.configuration.serializer.ServerboundPacketClassSerializer;
import io.papermc.paper.configuration.serializer.StringRepresentableSerializer;
import io.papermc.paper.configuration.serializer.collection.TableSerializer;
import io.papermc.paper.configuration.serializer.collection.map.FastutilMapSerializer;
import io.papermc.paper.configuration.serializer.collection.map.MapSerializer;
import io.papermc.paper.configuration.serializer.registry.RegistryHolderSerializer;
import io.papermc.paper.configuration.serializer.registry.RegistryValueSerializer;
import io.papermc.paper.configuration.transformation.Transformations;
import io.papermc.paper.configuration.transformation.global.LegacyPaperConfig;
import io.papermc.paper.configuration.transformation.global.versioned.V29_LogIPs;
import io.papermc.paper.configuration.transformation.global.versioned.V30_PacketIds;
import io.papermc.paper.configuration.transformation.global.versioned.V31_AllowNetherPropertiesToConfig;
import io.papermc.paper.configuration.transformation.world.FeatureSeedsGeneration;
import io.papermc.paper.configuration.transformation.world.LegacyPaperWorldConfig;
import io.papermc.paper.configuration.transformation.world.versioned.V29_ZeroWorldHeight;
import io.papermc.paper.configuration.transformation.world.versioned.V30_RenameFilterNbtFromSpawnEgg;
import io.papermc.paper.configuration.type.BooleanOrDefault;
import io.papermc.paper.configuration.type.DespawnRange;
import io.papermc.paper.configuration.type.Duration;
import io.papermc.paper.configuration.type.DurationOrDisabled;
import io.papermc.paper.configuration.type.EngineMode;
import io.papermc.paper.configuration.type.fallback.FallbackValueSerializer;
import io.papermc.paper.configuration.type.number.DoubleOr;
import io.papermc.paper.configuration.type.number.IntOr;
import it.unimi.dsi.fastutil.objects.Reference2IntMap;
import it.unimi.dsi.fastutil.objects.Reference2IntOpenHashMap;
import it.unimi.dsi.fastutil.objects.Reference2LongMap;
import it.unimi.dsi.fastutil.objects.Reference2LongOpenHashMap;
import it.unimi.dsi.fastutil.objects.Reference2ObjectMap;
import it.unimi.dsi.fastutil.objects.Reference2ObjectOpenHashMap;
import java.io.File;
import java.io.IOException;
import java.lang.annotation.Annotation;
import java.lang.reflect.Type;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;
import java.util.List;
import java.util.Locale;
import java.util.function.Function;
import java.util.function.Supplier;
import net.kyori.adventure.key.Key;
import net.minecraft.core.RegistryAccess;
import net.minecraft.core.component.DataComponentType;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.Identifier;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.gamerules.GameRules;
import net.minecraft.world.level.levelgen.feature.ConfiguredFeature;
import org.apache.commons.lang3.RandomStringUtils;
import org.bukkit.configuration.ConfigurationSection;
import org.bukkit.configuration.file.YamlConfiguration;
import org.jetbrains.annotations.VisibleForTesting;
import org.jspecify.annotations.Nullable;
import org.slf4j.Logger;
import org.spigotmc.SpigotConfig;
import org.spigotmc.SpigotWorldConfig;
import org.spongepowered.configurate.BasicConfigurationNode;
import org.spongepowered.configurate.ConfigurateException;
import org.spongepowered.configurate.ConfigurationNode;
import org.spongepowered.configurate.ConfigurationOptions;
import org.spongepowered.configurate.NodePath;
import org.spongepowered.configurate.objectmapping.ObjectMapper;
import org.spongepowered.configurate.transformation.ConfigurationTransformation;
import org.spongepowered.configurate.transformation.TransformAction;
import org.spongepowered.configurate.yaml.YamlConfigurationLoader;

import static com.google.common.base.Preconditions.checkState;
import static io.leangen.geantyref.GenericTypeReflector.erase;

@SuppressWarnings("Convert2Diamond")
public class PaperConfigurations extends Configurations<GlobalConfiguration, WorldConfiguration> {

    private static final Logger LOGGER = LogUtils.getClassLogger();
    static final String GLOBAL_CONFIG_FILE_NAME = "paper-global.yml";
    static final String WORLD_DEFAULTS_CONFIG_FILE_NAME = "paper-world-defaults.yml";
    static final String WORLD_CONFIG_FILE_NAME = "paper-world.yml";
    public static final String CONFIG_DIR = "config";
    private static final String BACKUP_DIR ="legacy-backup";

    private static final String GLOBAL_HEADER = String.format("""
            这是 Paper 的全局配置文件。
            如你所见，有很多选项可以配置。部分选项可能影响游戏玩法，因此请谨慎使用，
            并在配置前确保你了解每个选项的作用。

            如果你在配置方面需要帮助，或有任何与 Paper 相关的问题，
            请加入我们的 Discord 或查阅文档页面。

            世界配置选项已移动到各自的世界文件夹中。
            文件名为 %s

            文件参考: https://docs.papermc.io/paper/reference/global-configuration/
            文档: https://docs.papermc.io/
            Discord: https://discord.gg/papermc
            网站: https://papermc.io/""", WORLD_CONFIG_FILE_NAME);

    private static final String WORLD_DEFAULTS_HEADER = """
            这是 Paper 的世界默认配置文件。
            如你所见，有很多选项可以配置。部分选项可能影响游戏玩法，因此请谨慎使用，
            并在配置前确保你了解每个选项的作用。

            如果你在配置方面需要帮助，或有任何与 Paper 相关的问题，
            请加入我们的 Discord 或查阅文档页面。

            此处的配置选项适用于所有世界，除非你在每个世界文件夹内的世界专属配置文件中指定覆盖。

            文件参考: https://docs.papermc.io/paper/reference/world-configuration/
            文档: https://docs.papermc.io/
            Discord: https://discord.gg/papermc
            网站: https://papermc.io/""";

    private static final Function<ContextMap, String> WORLD_HEADER = map -> String.format("""
        这是 Paper 的一个世界配置文件。
        此文件初始为空，但可以填入设置以覆盖 %s/%s 中的选项。
        
        更多信息请参见 https://docs.papermc.io/paper/reference/configuration/#per-world-configuration
        
        世界: %s""",
        PaperConfigurations.CONFIG_DIR,
        PaperConfigurations.WORLD_DEFAULTS_CONFIG_FILE_NAME,
        map.require(WORLD_KEY)
    );

    private static final String MOVED_NOTICE = """
        全局和世界默认配置文件已移动到 %s，
        世界专属配置文件已移动到对应世界文件夹内。
        
        更多信息请参见 https://docs.papermc.io/paper/configuration。
        """;

    @VisibleForTesting
    public static final Supplier<SpigotWorldConfig> SPIGOT_WORLD_DEFAULTS = Suppliers.memoize(() -> new SpigotWorldConfig(RandomStringUtils.randomAlphabetic(255), Key.key(RandomStringUtils.randomAlphabetic(255).toLowerCase(Locale.ROOT))) {
        @Override // override to ensure "verbose" is false
        public void init() {
            SpigotConfig.readConfig(SpigotWorldConfig.class, this);
        }
    });
    public static final ContextKey<Supplier<SpigotWorldConfig>> SPIGOT_WORLD_CONFIG_CONTEXT_KEY = new ContextKey<>(new TypeToken<Supplier<SpigotWorldConfig>>() {}, "spigot world config");


    public PaperConfigurations(final Path globalFolder) {
        super(globalFolder, GlobalConfiguration.class, WorldConfiguration.class, GLOBAL_CONFIG_FILE_NAME, WORLD_DEFAULTS_CONFIG_FILE_NAME, WORLD_CONFIG_FILE_NAME);
    }

    @Override
    protected int globalConfigVersion() {
        return GlobalConfiguration.CURRENT_VERSION;
    }

    @Override
    protected int worldConfigVersion() {
        return WorldConfiguration.CURRENT_VERSION;
    }

    @Override
    protected YamlConfigurationLoader.Builder createLoaderBuilder() {
        return super.createLoaderBuilder()
            .defaultOptions(PaperConfigurations::defaultOptions);
    }

    private static ConfigurationOptions defaultOptions(ConfigurationOptions options) {
        return options.serializers(builder -> builder
            .register(MapSerializer.TYPE, new MapSerializer(false))
            .register(new EnumValueSerializer())
            .register(new ComponentSerializer())
            .register(IntOr.Default.SERIALIZER)
            .register(IntOr.Disabled.SERIALIZER)
            .register(DoubleOr.Default.SERIALIZER)
            .register(DoubleOr.Disabled.SERIALIZER)
            .register(BooleanOrDefault.SERIALIZER)
            .register(Duration.SERIALIZER)
            .register(DurationOrDisabled.SERIALIZER)
            .register(NbtPathSerializer.SERIALIZER)
            .register(IdentifierSerializer.INSTANCE)
        );
    }

    @Override
    protected ObjectMapper.Factory.Builder createGlobalObjectMapperFactoryBuilder() {
        return defaultGlobalFactoryBuilder(super.createGlobalObjectMapperFactoryBuilder());
    }

    private static ObjectMapper.Factory.Builder defaultGlobalFactoryBuilder(ObjectMapper.Factory.Builder builder) {
        return builder.addDiscoverer(InnerClassFieldDiscoverer.globalConfig(defaultFieldProcessors()));
    }

    @Override
    protected YamlConfigurationLoader.Builder createGlobalLoaderBuilder(RegistryAccess registryAccess) {
        return super.createGlobalLoaderBuilder(registryAccess)
            .defaultOptions((options) -> defaultGlobalOptions(registryAccess, options));
    }

    private static ConfigurationOptions defaultGlobalOptions(RegistryAccess registryAccess, ConfigurationOptions options) {
        return options
            .header(GLOBAL_HEADER)
            .serializers(builder -> builder
                .register(new ServerboundPacketClassSerializer())
                .register(new RegistryValueSerializer<>(new TypeToken<DataComponentType<?>>() {}, registryAccess, Registries.DATA_COMPONENT_TYPE, false))
            );
    }

    @Override
    public GlobalConfiguration initializeGlobalConfiguration(final RegistryAccess registryAccess) throws ConfigurateException {
        GlobalConfiguration configuration = super.initializeGlobalConfiguration(registryAccess);
        GlobalConfiguration.set(configuration);
        return configuration;
    }

    @Override
    protected ContextMap.Builder createDefaultContextMap(final RegistryAccess registryAccess) {
        return super.createDefaultContextMap(registryAccess)
            .put(SPIGOT_WORLD_CONFIG_CONTEXT_KEY, SPIGOT_WORLD_DEFAULTS);
    }

    @Override
    protected ObjectMapper.Factory.Builder createWorldObjectMapperFactoryBuilder(final ContextMap contextMap) {
        return super.createWorldObjectMapperFactoryBuilder(contextMap)
            .addNodeResolver(new RequiresSpigotInitialization.Factory(contextMap.require(SPIGOT_WORLD_CONFIG_CONTEXT_KEY).get()))
            .addNodeResolver(new NestedSetting.Factory())
            .addDiscoverer(InnerClassFieldDiscoverer.worldConfig(createWorldConfigInstance(contextMap), defaultFieldProcessors()));
    }

    private static WorldConfiguration createWorldConfigInstance(ContextMap contextMap) {
        return new WorldConfiguration(
            contextMap.require(PaperConfigurations.SPIGOT_WORLD_CONFIG_CONTEXT_KEY).get(),
            contextMap.require(Configurations.WORLD_KEY)
        );
    }

    @Override
    protected YamlConfigurationLoader.Builder createWorldConfigLoaderBuilder(final ContextMap contextMap) {
        final RegistryAccess access = contextMap.require(REGISTRY_ACCESS);
        return super.createWorldConfigLoaderBuilder(contextMap)
            .defaultOptions(options -> options
                .header(contextMap.require(WORLD_KEY).equals(WORLD_DEFAULTS_KEY) ? WORLD_DEFAULTS_HEADER : WORLD_HEADER.apply(contextMap))
                .serializers(serializers -> serializers
                    .register(new TypeToken<Reference2IntMap<?>>() {}, new FastutilMapSerializer.SomethingToPrimitive<Reference2IntMap<?>>(Reference2IntOpenHashMap::new, Integer.TYPE))
                    .register(new TypeToken<Reference2LongMap<?>>() {}, new FastutilMapSerializer.SomethingToPrimitive<Reference2LongMap<?>>(Reference2LongOpenHashMap::new, Long.TYPE))
                    .register(new TypeToken<Reference2ObjectMap<?, ?>>() {}, new FastutilMapSerializer.SomethingToSomething<Reference2ObjectMap<?, ?>>(Reference2ObjectOpenHashMap::new))
                    .register(new TypeToken<Table<?, ?, ?>>() {}, new TableSerializer())
                    .register(DespawnRange.class, DespawnRange.SERIALIZER)
                    .register(StringRepresentableSerializer::isValidFor, new StringRepresentableSerializer())
                    .register(EngineMode.SERIALIZER)
                    .register(FallbackValueSerializer.create(contextMap.require(SPIGOT_WORLD_CONFIG_CONTEXT_KEY).get(), MinecraftServer::getServer))
                    .register(new RegistryValueSerializer<>(new TypeToken<EntityType<?>>() {}, access, Registries.ENTITY_TYPE, true))
                    .register(new RegistryValueSerializer<>(Item.class, access, Registries.ITEM, true))
                    .register(new RegistryValueSerializer<>(Block.class, access, Registries.BLOCK, true))
                    .register(new RegistryHolderSerializer<>(new TypeToken<ConfiguredFeature<?, ?>>() {}, access, Registries.CONFIGURED_FEATURE, false))
                )
            );
    }

    @Override
    protected void applyWorldConfigTransformations(final ContextMap contextMap, final ConfigurationNode node, final @Nullable ConfigurationNode defaultsNode) throws ConfigurateException {
        final ConfigurationTransformation.Builder builder = ConfigurationTransformation.builder();
        for (final NodePath path : RemovedConfigurations.REMOVED_WORLD_PATHS) {
            builder.addAction(path, TransformAction.remove());
        }
        builder.build().apply(node);

        final ConfigurationTransformation.VersionedBuilder versionedBuilder = Transformations.versionedBuilder();
        V29_ZeroWorldHeight.apply(versionedBuilder);
        V30_RenameFilterNbtFromSpawnEgg.apply(versionedBuilder);
        // ADD FUTURE VERSIONED TRANSFORMS TO versionedBuilder HERE
        versionedBuilder.build().apply(node);
    }

    @Override
    protected void applyGlobalConfigTransformations(ConfigurationNode node) throws ConfigurateException {
        ConfigurationTransformation.Builder builder = ConfigurationTransformation.builder();
        for (NodePath path : RemovedConfigurations.REMOVED_GLOBAL_PATHS) {
            builder.addAction(path, TransformAction.remove());
        }
        builder.build().apply(node);

        final ConfigurationTransformation.VersionedBuilder versionedBuilder = Transformations.versionedBuilder();
        V29_LogIPs.apply(versionedBuilder);
        V30_PacketIds.apply(versionedBuilder);
        V31_AllowNetherPropertiesToConfig.apply(versionedBuilder);
        // ADD FUTURE VERSIONED TRANSFORMS TO versionedBuilder HERE
        versionedBuilder.build().apply(node);
    }

    private static final List<Transformations.DefaultsAware> DEFAULT_AWARE_TRANSFORMATIONS = List.of(
        FeatureSeedsGeneration::apply
    );

    @Override
    protected void applyDefaultsAwareWorldConfigTransformations(final ContextMap contextMap, final ConfigurationNode worldNode, final ConfigurationNode defaultsNode) throws ConfigurateException {
        final ConfigurationTransformation.Builder builder = ConfigurationTransformation.builder();
        // ADD FUTURE TRANSFORMS HERE (these transforms run after the defaults have been merged into the node)
        DEFAULT_AWARE_TRANSFORMATIONS.forEach(transform -> transform.apply(builder, contextMap, defaultsNode));
        builder.build().apply(worldNode);
    }

    @Override
    public WorldConfiguration createWorldConfig(final ContextMap contextMap) {
        final String levelKey = contextMap.require(WORLD_KEY).toString();
        try {
            return super.createWorldConfig(contextMap);
        } catch (IOException exception) {
            throw new RuntimeException("无法为以下内容创建世界配置：" + levelKey, exception);
        }
    }

    @Override
    protected boolean isConfigType(final Type type) {
        return ConfigurationPart.class.isAssignableFrom(erase(type));
    }

    public void reloadConfigs(MinecraftServer server) {
        try {
            this.initializeGlobalConfiguration(server.registryAccess(), reloader(this.globalConfigClass, GlobalConfiguration.get()));
            this.initializeWorldDefaultsConfiguration(server.registryAccess());
            for (ServerLevel level : server.getAllLevels()) {
                this.createWorldConfig(createWorldContextMap(level), reloader(this.worldConfigClass, level.paperConfig()));
            }
        } catch (Exception ex) {
            throw new RuntimeException("无法重载 Paper 配置文件", ex);
        }
    }

    private static List<Definition<? extends Annotation, ?, ? extends FieldProcessor.Factory<?, ?>>> defaultFieldProcessors() {
        return List.of(
            MergeMap.DEFINITION
        );
    }

    private static ContextMap createWorldContextMap(ServerLevel level) {
        return createWorldContextMap(level.getServer().storageSource.getDimensionPath(level.dimension()), level.dimension().identifier(), level.spigotConfig, level.registryAccess(), level.getGameRules());
    }

    public static ContextMap createWorldContextMap(final Path dir, final Identifier worldKey, final SpigotWorldConfig spigotConfig, final RegistryAccess registryAccess, final GameRules gameRules) {
        return ContextMap.builder()
            .put(WORLD_DIRECTORY, dir)
            .put(WORLD_KEY, worldKey)
            .put(SPIGOT_WORLD_CONFIG_CONTEXT_KEY, Suppliers.ofInstance(spigotConfig))
            .put(REGISTRY_ACCESS, registryAccess)
            .put(GAME_RULES, gameRules)
            .build();
    }

    public static PaperConfigurations setup(final Path legacyConfig, final Path configDir, final Path worldFolder, final File spigotConfig) throws Exception {
        final Path legacy = Files.isSymbolicLink(legacyConfig) ? Files.readSymbolicLink(legacyConfig) : legacyConfig;
        if (needsConverting(legacyConfig)) {
            final String legacyFileName = legacyConfig.getFileName().toString();
            try {
                if (Files.exists(configDir) && !Files.isDirectory(configDir)) {
                    throw new RuntimeException("Paper 需要创建一个 '" + configDir.toAbsolutePath() + "' 文件夹。但已存在一个名为 '" + configDir.toAbsolutePath() + "'。请将其删除并重启服务端。");
                }
                final Path backupDir = configDir.resolve(BACKUP_DIR);
                if (Files.exists(backupDir) && !Files.isDirectory(backupDir)) {
                    throw new RuntimeException("Paper 需要创建一个 '" + BACKUP_DIR + "' 目录，位于 '" + configDir.toAbsolutePath() + "' 文件夹。但已存在一个名为 '" + BACKUP_DIR + "'。请将其删除并重启服务端。");
                }
                createDirectoriesSymlinkAware(backupDir);
                final String backupFileName = legacyFileName + ".old";
                final Path legacyConfigBackup = backupDir.resolve(backupFileName);
                if (Files.exists(legacyConfigBackup) && !Files.isRegularFile(legacyConfigBackup)) {
                    throw new RuntimeException("Paper 需要创建一个 '" + backupFileName + "' 文件，位于 '" + backupDir.toAbsolutePath() + "' 文件夹。但已存在一个名为 '" + backupFileName + "'。请将其删除并重启服务端。");
                }
                Files.move(legacyConfig.toRealPath(), legacyConfigBackup, StandardCopyOption.REPLACE_EXISTING); // make backup
                if (Files.isSymbolicLink(legacyConfig)) {
                    Files.delete(legacyConfig);
                }
                final Path replacementFile = legacy.resolveSibling(legacyFileName + "-README.txt");
                if (Files.notExists(replacementFile)) {
                    Files.createFile(replacementFile);
                    Files.writeString(replacementFile, String.format(MOVED_NOTICE, configDir.toAbsolutePath()));
                }
                convert(legacyConfigBackup, configDir, worldFolder, spigotConfig);
            } catch (final IOException ex) {
                throw new RuntimeException("无法转换 '" + legacyFileName + "' 转换为新的配置格式", ex);
            }
        }
        try {
            createDirectoriesSymlinkAware(configDir);
            return new PaperConfigurations(configDir);
        } catch (final IOException ex) {
            throw new RuntimeException("无法设置 PaperConfigurations", ex);
        }
    }

    private static void convert(final Path legacyConfig, final Path configDir, final Path worldFolder, final File spigotConfig) throws Exception {
        createDirectoriesSymlinkAware(configDir);

        final YamlConfigurationLoader legacyLoader = ConfigurationLoaders.naturallySortedWithoutHeader(legacyConfig);
        final YamlConfigurationLoader globalLoader = ConfigurationLoaders.naturallySortedWithoutHeader(configDir.resolve(GLOBAL_CONFIG_FILE_NAME));
        final YamlConfigurationLoader worldDefaultsLoader = ConfigurationLoaders.naturallySortedWithoutHeader(configDir.resolve(WORLD_DEFAULTS_CONFIG_FILE_NAME));

        final ConfigurationNode legacy = legacyLoader.load();
        checkState(!legacy.virtual(), "不能为虚拟");
        final int version = legacy.node(Configuration.LEGACY_CONFIG_VERSION_FIELD).getInt();

        final ConfigurationNode legacyWorldSettings = legacy.node("world-settings").copy();
        checkState(!legacyWorldSettings.virtual(), "不能为虚拟");
        legacy.removeChild("world-settings");

        // Apply legacy transformations before settings flatten
        final YamlConfiguration spigotConfiguration = loadLegacyConfigFile(spigotConfig); // needs to change spigot config values in this transformation
        LegacyPaperConfig.transformation(spigotConfiguration).apply(legacy);
        spigotConfiguration.save(spigotConfig);
        legacy.mergeFrom(legacy.node("settings")); // flatten "settings" to root
        legacy.removeChild("settings");
        LegacyPaperConfig.toNewFormat().apply(legacy);
        globalLoader.save(legacy); // save converted node to new global location

        final ConfigurationNode worldDefaults = legacyWorldSettings.node("default").copy();
        checkState(!worldDefaults.virtual());
        worldDefaults.node(Configuration.LEGACY_CONFIG_VERSION_FIELD).raw(version);
        legacyWorldSettings.removeChild("default");
        LegacyPaperWorldConfig.transformation().apply(worldDefaults);
        LegacyPaperWorldConfig.toNewFormat().apply(worldDefaults);
        worldDefaultsLoader.save(worldDefaults);

        legacyWorldSettings.childrenMap().forEach((world, legacyWorldNode) -> {
            try {
                legacyWorldNode.node(Configuration.LEGACY_CONFIG_VERSION_FIELD).raw(version);
                LegacyPaperWorldConfig.transformation().apply(legacyWorldNode);
                LegacyPaperWorldConfig.toNewFormat().apply(legacyWorldNode);
                ConfigurationLoaders.naturallySortedWithoutHeader(worldFolder.resolve(world.toString()).resolve(WORLD_CONFIG_FILE_NAME)).save(legacyWorldNode); // save converted node to new location
            } catch (final ConfigurateException ex) {
                ex.printStackTrace();
            }
        });
    }

    private static boolean needsConverting(final Path legacyConfig) {
        return Files.exists(legacyConfig) && Files.isRegularFile(legacyConfig);
    }

    @Deprecated
    public YamlConfiguration createLegacyObject(final MinecraftServer server) {
        YamlConfiguration global = YamlConfiguration.loadConfiguration(this.globalFolder.resolve(this.globalConfigFileName).toFile());
        ConfigurationSection worlds = global.createSection("__________WORLDS__________");
        worlds.set("__defaults__", YamlConfiguration.loadConfiguration(this.globalFolder.resolve(this.defaultWorldConfigFileName).toFile()));
        for (ServerLevel level : server.getAllLevels()) {
            worlds.set(level.getWorld().getName(), YamlConfiguration.loadConfiguration(getWorldConfigFile(level).toFile()));
        }
        return global;
    }

    @Deprecated
    public static YamlConfiguration loadLegacyConfigFile(File configFile) throws Exception {
        YamlConfiguration config = new YamlConfiguration();
        if (configFile.exists()) {
            try {
                config.load(configFile);
            } catch (Exception ex) {
                throw new Exception("加载配置文件失败：" + configFile.getName(), ex);
            }
        }
        return config;
    }

    @VisibleForTesting
    static ConfigurationNode createForTesting(RegistryAccess registryAccess) {
        ObjectMapper.Factory factory = defaultGlobalFactoryBuilder(ObjectMapper.factoryBuilder()).build();
        ConfigurationOptions options = defaultGlobalOptions(registryAccess, defaultOptions(ConfigurationOptions.defaults()))
            .serializers(builder -> builder.register(type -> ConfigurationPart.class.isAssignableFrom(erase(type)), factory.asTypeSerializer()));
        return BasicConfigurationNode.root(options);
    }

    // Symlinks are not correctly checked in createDirectories
    static void createDirectoriesSymlinkAware(Path path) throws IOException {
        if (!Files.isDirectory(path)) {
            Files.createDirectories(path);
        }
    }
}
