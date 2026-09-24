package io.papermc.paper.configuration;

import com.google.common.base.Preconditions;
import com.mojang.logging.LogUtils;
import io.leangen.geantyref.TypeToken;
import io.papermc.paper.configuration.constraint.Constraint;
import io.papermc.paper.configuration.constraint.Constraints;
import java.io.IOException;
import java.lang.reflect.Type;
import java.nio.file.AccessDeniedException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.Map;
import java.util.NoSuchElementException;
import java.util.Objects;
import java.util.function.UnaryOperator;
import net.minecraft.core.RegistryAccess;
import net.minecraft.resources.Identifier;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.level.gamerules.GameRules;
import org.jetbrains.annotations.MustBeInvokedByOverriders;
import org.jspecify.annotations.Nullable;
import org.slf4j.Logger;
import org.spongepowered.configurate.CommentedConfigurationNode;
import org.spongepowered.configurate.ConfigurateException;
import org.spongepowered.configurate.ConfigurationNode;
import org.spongepowered.configurate.ConfigurationOptions;
import org.spongepowered.configurate.objectmapping.ObjectMapper;
import org.spongepowered.configurate.serialize.SerializationException;
import org.spongepowered.configurate.util.CheckedFunction;
import org.spongepowered.configurate.yaml.YamlConfigurationLoader;

public abstract class Configurations<G, W> {

    private static final Logger LOGGER = LogUtils.getClassLogger();
    public static final Identifier WORLD_DEFAULTS_KEY = Identifier.fromNamespaceAndPath("configurations", "__world_defaults__");
    protected final Path globalFolder;
    protected final Class<G> globalConfigClass;
    protected final Class<W> worldConfigClass;
    protected final String globalConfigFileName;
    protected final String defaultWorldConfigFileName;
    protected final String worldConfigFileName;

    public Configurations(
        final Path globalFolder,
        final Class<G> globalConfigType,
        final Class<W> worldConfigClass,
        final String globalConfigFileName,
        final String defaultWorldConfigFileName,
        final String worldConfigFileName
    ) {
        this.globalFolder = globalFolder;
        this.globalConfigClass = globalConfigType;
        this.worldConfigClass = worldConfigClass;
        this.globalConfigFileName = globalConfigFileName;
        this.defaultWorldConfigFileName = defaultWorldConfigFileName;
        this.worldConfigFileName = worldConfigFileName;
    }

    protected ObjectMapper.Factory.Builder createObjectMapper() {
        return ObjectMapper.factoryBuilder()
            .addConstraint(Constraint.class, new Constraint.Factory())
            .addConstraint(Constraints.Min.class, Number.class, new Constraints.Min.Factory())
            .addConstraint(Constraints.Max.class, Number.class, new Constraints.Max.Factory());
    }

    protected YamlConfigurationLoader.Builder createLoaderBuilder() {
        return ConfigurationLoaders.naturallySorted();
    }

    protected abstract boolean isConfigType(final Type type);

    protected abstract int globalConfigVersion();

    protected abstract int worldConfigVersion();

    protected ObjectMapper.Factory.Builder createGlobalObjectMapperFactoryBuilder() {
        return this.createObjectMapper();
    }

    @MustBeInvokedByOverriders
    protected YamlConfigurationLoader.Builder createGlobalLoaderBuilder(RegistryAccess registryAccess) {
        return this.createLoaderBuilder();
    }

    static <T> CheckedFunction<ConfigurationNode, T, SerializationException> creator(final Class<? extends T> type, final boolean refreshNode) {
        return node -> {
            final T instance = node.require(type);
            if (refreshNode) {
                node.set(type, instance);
            }
            return instance;
        };
    }

    static <T> CheckedFunction<ConfigurationNode, T, SerializationException> reloader(Class<T> type, T instance) {
        return node -> {
            ObjectMapper.Factory factory = (ObjectMapper.Factory) Objects.requireNonNull(node.options().serializers().get(type));
            ObjectMapper.Mutable<T> mutable = (ObjectMapper.Mutable<T>) factory.get(type);
            mutable.load(instance, node);
            return instance;
        };
    }

    public G initializeGlobalConfiguration(final RegistryAccess registryAccess) throws ConfigurateException {
        return this.initializeGlobalConfiguration(registryAccess, creator(this.globalConfigClass, true));
    }

    private void trySaveFileNode(YamlConfigurationLoader loader, ConfigurationNode node, String filename) throws ConfigurateException {
        try {
            loader.save(node);
        } catch (ConfigurateException ex) {
            if (ex.getCause() instanceof AccessDeniedException) {
                LOGGER.warn("无法保存 {}：Paper 无法将所有配置设置持久化到配置文件中。配置文件中缺失的设置将在内存中使用默认值。管理员应查阅 https://docs.papermc.io/paper/configuration 上的配置文档以获取更多详细信息。", filename, ex);
            } else throw ex;
        }
    }

    protected G initializeGlobalConfiguration(final RegistryAccess registryAccess, final CheckedFunction<ConfigurationNode, G, SerializationException> creator) throws ConfigurateException {
        final Path configFile = this.globalFolder.resolve(this.globalConfigFileName);
        final YamlConfigurationLoader loader = this.createGlobalLoaderBuilder(registryAccess)
            .defaultOptions(this.applyObjectMapperFactory(this.createGlobalObjectMapperFactoryBuilder().build()))
            .path(configFile)
            .build();
        final ConfigurationNode node;
        if (Files.notExists(configFile)) {
            node = CommentedConfigurationNode.root(loader.defaultOptions());
            node.node(Configuration.VERSION_FIELD).raw(this.globalConfigVersion());
            GlobalConfiguration.isFirstStart = true;
        } else {
            node = loader.load();
            this.verifyGlobalConfigVersion(node);
        }
        this.applyGlobalConfigTransformations(node);
        final G instance = creator.apply(node);
        trySaveFileNode(loader, node, configFile.toString());
        return instance;
    }

    protected void verifyGlobalConfigVersion(final ConfigurationNode globalNode) {
        final ConfigurationNode version = globalNode.node(Configuration.VERSION_FIELD);
        if (version.virtual()) {
            LOGGER.warn("全局配置文件未设置版本号，假设为最新版本");
            version.raw(this.globalConfigVersion());
        } else if (version.getInt() > this.globalConfigVersion()) {
            LOGGER.error("正在加载比所支持的版本更新的配置（{} > {}）！你可能需要备份并删除全局配置文件才能启动服务器。", version.getInt(), this.globalConfigVersion());
        }
    }

    protected void applyGlobalConfigTransformations(final ConfigurationNode node) throws ConfigurateException {
    }

    @MustBeInvokedByOverriders
    protected ContextMap.Builder createDefaultContextMap(final RegistryAccess registryAccess) {
        return ContextMap.builder()
            .put(WORLD_KEY, WORLD_DEFAULTS_KEY)
            .put(REGISTRY_ACCESS, registryAccess);
    }

    public void initializeWorldDefaultsConfiguration(final RegistryAccess registryAccess) throws ConfigurateException {
        final ContextMap contextMap = this.createDefaultContextMap(registryAccess)
            .put(FIRST_DEFAULT)
            .build();
        final Path configFile = this.globalFolder.resolve(this.defaultWorldConfigFileName);
        final DefaultWorldLoader result = this.createDefaultWorldLoader(false, contextMap, configFile);
        final YamlConfigurationLoader loader = result.loader();
        final ConfigurationNode node = loader.load();
        if (result.isNewFile()) { // add version to new files
            node.node(Configuration.VERSION_FIELD).raw(this.worldConfigVersion());
        } else {
            this.verifyWorldConfigVersion(contextMap, node);
        }
        this.applyWorldConfigTransformations(contextMap, node, null);
        final W instance = node.require(this.worldConfigClass);
        node.set(this.worldConfigClass, instance);
        this.trySaveFileNode(loader, node, configFile.toString());
    }

    private DefaultWorldLoader createDefaultWorldLoader(final boolean requireFile, final ContextMap contextMap, final Path configFile) {
        boolean willCreate = Files.notExists(configFile);
        if (requireFile && willCreate) {
            throw new IllegalStateException("World defaults configuration file '" + configFile + "' doesn't exist");
        }
        return new DefaultWorldLoader(
            this.createWorldConfigLoaderBuilder(contextMap)
                .defaultOptions(this.applyObjectMapperFactory(this.createWorldObjectMapperFactoryBuilder(contextMap).build()))
                .path(configFile)
                .build(),
            willCreate
        );
    }

    private record DefaultWorldLoader(YamlConfigurationLoader loader, boolean isNewFile) {
    }

    protected ObjectMapper.Factory.Builder createWorldObjectMapperFactoryBuilder(final ContextMap contextMap) {
        return this.createObjectMapper();
    }

    @MustBeInvokedByOverriders
    protected YamlConfigurationLoader.Builder createWorldConfigLoaderBuilder(final ContextMap contextMap) {
        return this.createLoaderBuilder();
    }

    // Make sure to run version transforms on the default world config first via #setupWorldDefaultsConfig
    public W createWorldConfig(final ContextMap contextMap) throws IOException {
        return this.createWorldConfig(contextMap, creator(this.worldConfigClass, false));
    }

    protected W createWorldConfig(final ContextMap contextMap, final CheckedFunction<ConfigurationNode, W, SerializationException> creator) throws IOException {
        Preconditions.checkArgument(!contextMap.isDefaultWorldContext(), "cannot create world map with default world context");
        final Path defaultsConfigFile = this.globalFolder.resolve(this.defaultWorldConfigFileName);
        final YamlConfigurationLoader defaultsLoader = this.createDefaultWorldLoader(true, this.createDefaultContextMap(contextMap.require(REGISTRY_ACCESS)).build(), defaultsConfigFile).loader();
        final ConfigurationNode defaultsNode = defaultsLoader.load();

        boolean newFile = false;
        final Path dir = contextMap.require(WORLD_DIRECTORY);
        final Path worldConfigFile = dir.resolve(this.worldConfigFileName);
        if (Files.notExists(worldConfigFile)) {
            PaperConfigurations.createDirectoriesSymlinkAware(dir);
            Files.createFile(worldConfigFile); // create empty file as template
            newFile = true;
        }

        final YamlConfigurationLoader worldLoader = this.createWorldConfigLoaderBuilder(contextMap)
            .defaultOptions(this.applyObjectMapperFactory(this.createWorldObjectMapperFactoryBuilder(contextMap).build()))
            .path(worldConfigFile)
            .build();
        final ConfigurationNode worldNode = worldLoader.load();
        if (newFile) { // set the version field if new file
            worldNode.node(Configuration.VERSION_FIELD).set(this.worldConfigVersion());
        } else {
            this.verifyWorldConfigVersion(contextMap, worldNode);
        }
        this.applyWorldConfigTransformations(contextMap, worldNode, defaultsNode);
        this.applyDefaultsAwareWorldConfigTransformations(contextMap, worldNode, defaultsNode);
        this.trySaveFileNode(worldLoader, worldNode, worldConfigFile.toString()); // save before loading node NOTE: don't save the backing node after loading it, or you'll fill up the world-specific config
        worldNode.mergeFrom(defaultsNode);
        return creator.apply(worldNode);
    }

    protected void verifyWorldConfigVersion(final ContextMap contextMap, final ConfigurationNode worldNode) {
        final ConfigurationNode version = worldNode.node(Configuration.VERSION_FIELD);
        final Identifier worldKey = contextMap.require(WORLD_KEY);
        if (version.virtual()) {
            if (worldKey.equals(WORLD_DEFAULTS_KEY)) {
                LOGGER.warn("世界默认配置文件未设置版本号，假设为最新版本");
            } else {
                LOGGER.warn("世界 " + worldKey + " 的配置文件未设置版本号，假设为最新版本");
            }
            version.raw(this.worldConfigVersion());
        } else if (version.getInt() > this.worldConfigVersion()) {
            String msg = "正在加载比所支持的版本更新的配置（{} > {}）！";
            if (worldKey.equals(WORLD_DEFAULTS_KEY)) {
                msg += "你可能需要备份并删除世界默认配置文件才能启动服务器。";
            } else {
                msg += "你可能需要备份并删除 " + worldKey + " 的配置文件才能启动服务器。";
            }
            LOGGER.error(msg, version.getInt(), this.worldConfigVersion());
        }
    }

    protected void applyWorldConfigTransformations(final ContextMap contextMap, final ConfigurationNode node, final @Nullable ConfigurationNode defaultsNode) throws ConfigurateException {
    }

    protected void applyDefaultsAwareWorldConfigTransformations(final ContextMap contextMap, final ConfigurationNode worldNode, final ConfigurationNode defaultsNode) throws ConfigurateException {
    }

    private UnaryOperator<ConfigurationOptions> applyObjectMapperFactory(final ObjectMapper.Factory factory) {
        return options -> options.serializers(builder -> builder
            .register(this::isConfigType, factory.asTypeSerializer())
            .registerAnnotatedObjects(factory));
    }

    public Path getWorldConfigFile(ServerLevel level) {
        return level.getServer().storageSource.getDimensionPath(level.dimension()).resolve(this.worldConfigFileName);
    }

    public static class ContextMap {
        private static final Object VOID = new Object();

        public static Builder builder() {
            return new Builder();
        }

        private final Map<ContextKey<?>, Object> backingMap;

        private ContextMap(Map<ContextKey<?>, Object> map) {
            this.backingMap = Map.copyOf(map);
        }

        @SuppressWarnings("unchecked")
        public <T> T require(ContextKey<T> key) {
            final @Nullable Object value = this.backingMap.get(key);
            if (value == null) {
                throw new NoSuchElementException("No element found for " + key + " with type " + key.type());
            } else if (value == VOID) {
                throw new IllegalArgumentException("Cannot get the value of a Void key");
            }
            return (T) value;
        }

        @SuppressWarnings("unchecked")
        public <T> @Nullable T get(ContextKey<T> key) {
            return (T) this.backingMap.get(key);
        }

        public boolean has(ContextKey<?> key) {
            return this.backingMap.containsKey(key);
        }

        public boolean isDefaultWorldContext() {
            return this.require(WORLD_KEY).equals(WORLD_DEFAULTS_KEY);
        }

        public static class Builder {

            private Builder() {
            }

            private final Map<ContextKey<?>, Object> buildingMap = new HashMap<>();

            public <T> Builder put(ContextKey<T> key, T value) {
                this.buildingMap.put(key, value);
                return this;
            }

            public Builder put(ContextKey<Void> key) {
                this.buildingMap.put(key, VOID);
                return this;
            }

            public ContextMap build() {
                return new ContextMap(this.buildingMap);
            }
        }
    }

    public static final ContextKey<Path> WORLD_DIRECTORY = new ContextKey<>(Path.class, "world directory");
    public static final ContextKey<Identifier> WORLD_KEY = new ContextKey<>(Identifier.class, "world key");
    public static final ContextKey<Void> FIRST_DEFAULT = new ContextKey<>(Void.class, "first default");
    public static final ContextKey<RegistryAccess> REGISTRY_ACCESS = new ContextKey<>(RegistryAccess.class, "registry access");
    public static final ContextKey<GameRules> GAME_RULES = new ContextKey<>(GameRules.class, "game rules");

    public record ContextKey<T>(TypeToken<T> type, String name) {

        public ContextKey(Class<T> type, String name) {
            this(TypeToken.get(type), name);
        }

        @Override
        public String toString() {
            return "ContextKey{" + this.name + "}";
        }
    }
}
