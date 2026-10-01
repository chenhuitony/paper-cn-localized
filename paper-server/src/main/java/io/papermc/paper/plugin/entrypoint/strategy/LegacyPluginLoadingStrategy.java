package io.papermc.paper.plugin.entrypoint.strategy;

import com.google.common.graph.GraphBuilder;
import com.google.common.graph.MutableGraph;
import io.papermc.paper.plugin.configuration.PluginMeta;
import io.papermc.paper.plugin.entrypoint.dependency.GraphDependencyContext;
import io.papermc.paper.plugin.entrypoint.dependency.MetaDependencyTree;
import io.papermc.paper.plugin.provider.PluginProvider;
import io.papermc.paper.plugin.provider.type.paper.PaperPluginParent;
import org.bukkit.plugin.UnknownDependencyException;

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.logging.Level;
import java.util.logging.Logger;

@SuppressWarnings("UnstableApiUsage")
public class LegacyPluginLoadingStrategy<T> implements ProviderLoadingStrategy<T> {

    private static final Logger LOGGER = Logger.getLogger("LegacyPluginLoadingStrategy");
    private final ProviderConfiguration<T> configuration;

    public LegacyPluginLoadingStrategy(ProviderConfiguration<T> onLoad) {
        this.configuration = onLoad;
    }

    @Override
    public List<ProviderPair<T>> loadProviders(List<PluginProvider<T>> providers, MetaDependencyTree dependencyTree) {
        List<ProviderPair<T>> javapluginsLoaded = new ArrayList<>();
        MutableGraph<String> dependencyGraph = dependencyTree.getGraph();

        Map<String, PluginProvider<T>> providersToLoad = new HashMap<>();
        Set<String> loadedPlugins = new HashSet<>();
        Map<String, String> pluginsProvided = new HashMap<>();
        Map<String, Collection<String>> dependencies = new HashMap<>();
        Map<String, Collection<String>> softDependencies = new HashMap<>();

        for (PluginProvider<T> provider : providers) {
            PluginMeta configuration = provider.getMeta();

            PluginProvider<T> replacedProvider = providersToLoad.put(configuration.getName(), provider);
            dependencyTree.addDirectDependency(configuration.getName()); // add to dependency tree
            if (replacedProvider != null) {
                LOGGER.severe(String.format(
                    "插件名称 `%s' 在 `%s' 中的文件 `%s' 和 `%s' 之间存在歧义",
                    configuration.getName(),
                    provider.getSource(),
                    replacedProvider.getSource(),
                    replacedProvider.getParentSource()
                ));
            }

            String removedProvided = pluginsProvided.remove(configuration.getName());
            if (removedProvided != null) {
                LOGGER.warning(String.format(
                    "插件名称 `%s' 存在歧义。它同时也由 `%s' 提供",
                    configuration.getName(),
                    removedProvided
                ));
            }

            for (String provided : configuration.getProvidedPlugins()) {
                PluginProvider<T> pluginProvider = providersToLoad.get(provided);

                if (pluginProvider != null) {
                    LOGGER.warning(String.format(
                        "`%s 提供了 `%s'，而这也是 `%s' 中 `%s' 的名称",
                        provider.getSource(),
                        provided,
                        pluginProvider.getSource(),
                        provider.getParentSource()
                    ));
                } else {
                    String replacedPlugin = pluginsProvided.put(provided, configuration.getName());
                    dependencyTree.addDirectDependency(provided); // add to dependency tree
                    if (replacedPlugin != null) {
                        LOGGER.warning(String.format(
                            "`%s' 同时被 `%s' 和 `%s' 提供",
                            provided,
                            configuration.getName(),
                            replacedPlugin
                        ));
                    }
                }
            }

            Collection<String> softDependencySet = provider.getMeta().getPluginSoftDependencies();
            if (softDependencySet != null && !softDependencySet.isEmpty()) {
                if (softDependencies.containsKey(configuration.getName())) {
                    // Duplicates do not matter, they will be removed together if applicable
                    softDependencies.get(configuration.getName()).addAll(softDependencySet);
                } else {
                    softDependencies.put(configuration.getName(), new LinkedList<String>(softDependencySet));
                }

                for (String depend : softDependencySet) {
                    dependencyGraph.putEdge(configuration.getName(), depend);
                }
            }

            Collection<String> dependencySet = provider.getMeta().getPluginDependencies();
            if (dependencySet != null && !dependencySet.isEmpty()) {
                dependencies.put(configuration.getName(), new LinkedList<String>(dependencySet));

                for (String depend : dependencySet) {
                    dependencyGraph.putEdge(configuration.getName(), depend);
                }
            }

            Collection<String> loadBeforeSet = provider.getMeta().getLoadBeforePlugins();
            if (loadBeforeSet != null && !loadBeforeSet.isEmpty()) {
                for (String loadBeforeTarget : loadBeforeSet) {
                    if (softDependencies.containsKey(loadBeforeTarget)) {
                        softDependencies.get(loadBeforeTarget).add(configuration.getName());
                    } else {
                        // softDependencies is never iterated, so 'ghost' plugins aren't an issue
                        Collection<String> shortSoftDependency = new LinkedList<String>();
                        shortSoftDependency.add(configuration.getName());
                        softDependencies.put(loadBeforeTarget, shortSoftDependency);
                    }

                    dependencyGraph.putEdge(loadBeforeTarget, configuration.getName());
                }
            }
        }

        while (!providersToLoad.isEmpty()) {
            boolean missingDependency = true;
            Iterator<Map.Entry<String, PluginProvider<T>>> providerIterator = providersToLoad.entrySet().iterator();

            while (providerIterator.hasNext()) {
                Map.Entry<String, PluginProvider<T>> entry = providerIterator.next();
                String providerIdentifier = entry.getKey();

                if (dependencies.containsKey(providerIdentifier)) {
                    Iterator<String> dependencyIterator = dependencies.get(providerIdentifier).iterator();
                    final Set<String> missingHardDependencies = new HashSet<>(dependencies.get(providerIdentifier).size()); // Paper - list all missing hard depends

                    while (dependencyIterator.hasNext()) {
                        String dependency = dependencyIterator.next();

                        // Dependency loaded
                        if (loadedPlugins.contains(dependency)) {
                            dependencyIterator.remove();

                            // We have a dependency not found
                        } else if (!providersToLoad.containsKey(dependency) && !pluginsProvided.containsKey(dependency)) {
                            // Paper start
                            missingHardDependencies.add(dependency);
                        }
                    }
                    if (!missingHardDependencies.isEmpty()) {
                        // Paper end
                        missingDependency = false;
                        providerIterator.remove();
                        pluginsProvided.values().removeIf(s -> s.equals(providerIdentifier)); // Paper - remove provided plugins
                        softDependencies.remove(providerIdentifier);
                        dependencies.remove(providerIdentifier);

                        LOGGER.log(
                            Level.SEVERE,
                            "无法在文件夹 '" + entry.getValue().getParentSource() + "' 中加载 '" + entry.getValue().getSource() + "'", // Paper
                            new UnknownDependencyException(missingHardDependencies, providerIdentifier)); // Paper
                    }

                    if (dependencies.containsKey(providerIdentifier) && dependencies.get(providerIdentifier).isEmpty()) {
                        dependencies.remove(providerIdentifier);
                    }
                }
                if (softDependencies.containsKey(providerIdentifier)) {
                    Iterator<String> softDependencyIterator = softDependencies.get(providerIdentifier).iterator();

                    while (softDependencyIterator.hasNext()) {
                        String softDependency = softDependencyIterator.next();

                        // Soft depend is no longer around
                        if (!providersToLoad.containsKey(softDependency) && !pluginsProvided.containsKey(softDependency)) {
                            softDependencyIterator.remove();
                        }
                    }

                    if (softDependencies.get(providerIdentifier).isEmpty()) {
                        softDependencies.remove(providerIdentifier);
                    }
                }
                if (!(dependencies.containsKey(providerIdentifier) || softDependencies.containsKey(providerIdentifier)) && providersToLoad.containsKey(providerIdentifier)) {
                    // We're clear to load, no more soft or hard dependencies left
                    PluginProvider<T> file = providersToLoad.get(providerIdentifier);
                    providerIterator.remove();
                    pluginsProvided.values().removeIf(s -> s.equals(providerIdentifier)); // Paper - remove provided plugins
                    missingDependency = false;

                    try {
                        this.configuration.applyContext(file, dependencyTree);
                        T loadedPlugin = file.createInstance();
                        this.warnIfPaperPlugin(file);

                        if (this.configuration.load(file, loadedPlugin)) {
                            loadedPlugins.add(file.getMeta().getName());
                            loadedPlugins.addAll(file.getMeta().getProvidedPlugins());
                            javapluginsLoaded.add(new ProviderPair<>(file, loadedPlugin));
                        }

                    } catch (Throwable ex) {
                        LOGGER.log(Level.SEVERE, "无法在文件夹 '" + file.getParentSource() + "' 中加载 '" + file.getSource() + "'", ex); // Paper
                    }
                }
            }

            if (missingDependency) {
                // We now iterate over plugins until something loads
                // This loop will ignore soft dependencies
                providerIterator = providersToLoad.entrySet().iterator();

                while (providerIterator.hasNext()) {
                    Map.Entry<String, PluginProvider<T>> entry = providerIterator.next();
                    String plugin = entry.getKey();

                    if (!dependencies.containsKey(plugin)) {
                        softDependencies.remove(plugin);
                        missingDependency = false;
                        PluginProvider<T> file = entry.getValue();
                        providerIterator.remove();

                        try {
                            this.configuration.applyContext(file, dependencyTree);
                            T loadedPlugin = file.createInstance();
                            this.warnIfPaperPlugin(file);

                            if (this.configuration.load(file, loadedPlugin)) {
                                loadedPlugins.add(file.getMeta().getName());
                                loadedPlugins.addAll(file.getMeta().getProvidedPlugins());
                                javapluginsLoaded.add(new ProviderPair<>(file, loadedPlugin));
                            }
                            break;
                        } catch (Throwable ex) {
                            LOGGER.log(Level.SEVERE, "无法在文件夹 '" + file.getParentSource() + "' 中加载 '" + file.getSource() + "'", ex); // Paper
                        }
                    }
                }
                // We have no plugins left without a depend
                if (missingDependency) {
                    softDependencies.clear();
                    dependencies.clear();
                    Iterator<PluginProvider<T>> failedPluginIterator = providersToLoad.values().iterator();

                    while (failedPluginIterator.hasNext()) {
                        PluginProvider<T> file = failedPluginIterator.next();
                        failedPluginIterator.remove();
                        LOGGER.log(Level.SEVERE, "无法在文件夹 '" + file.getParentSource() + "' 中加载 '" + file.getSource() + "'：检测到循环依赖"); // Paper
                    }
                }
            }
        }

        return javapluginsLoaded;
    }

    private void warnIfPaperPlugin(PluginProvider<T> provider) {
        if (provider instanceof PaperPluginParent.PaperServerPluginProvider) {
            provider.getLogger().warn("正在使用旧版插件加载逻辑加载 Paper 插件。这并不推荐，可能会导致加载顺序出现一些差异。如果你希望使用 Paper 插件，强烈建议你摆脱这种加载方式。");
        }
    }
}
