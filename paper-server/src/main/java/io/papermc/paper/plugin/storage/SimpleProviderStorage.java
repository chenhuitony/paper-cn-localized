package io.papermc.paper.plugin.storage;

import com.google.common.graph.GraphBuilder;
import com.mojang.logging.LogUtils;
import io.papermc.paper.plugin.entrypoint.dependency.MetaDependencyTree;
import io.papermc.paper.plugin.entrypoint.dependency.SimpleMetaDependencyTree;
import io.papermc.paper.plugin.entrypoint.strategy.PluginGraphCycleException;
import io.papermc.paper.plugin.entrypoint.strategy.ProviderLoadingStrategy;
import io.papermc.paper.plugin.provider.PluginProvider;
import org.slf4j.Logger;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

public abstract class SimpleProviderStorage<T> implements ProviderStorage<T> {

    private static final Logger LOGGER = LogUtils.getClassLogger();

    protected final List<PluginProvider<T>> providers = new ArrayList<>();
    protected ProviderLoadingStrategy<T> strategy;

    protected SimpleProviderStorage(ProviderLoadingStrategy<T> strategy) {
        this.strategy = strategy;
    }

    @Override
    public void register(PluginProvider<T> provider) {
        this.providers.add(provider);
    }

    @Override
    public void enter() {
        List<PluginProvider<T>> providerList = new ArrayList<>(this.providers);
        this.filterLoadingProviders(providerList);

        try {
            for (ProviderLoadingStrategy.ProviderPair<T> providerPair : this.strategy.loadProviders(providerList, this.createDependencyTree())) {
                this.processProvided(providerPair.provider(), providerPair.provided());
            }
        } catch (PluginGraphCycleException exception) {
            this.handleCycle(exception);
        }
    }

    @Override
    public MetaDependencyTree createDependencyTree() {
        return new SimpleMetaDependencyTree(GraphBuilder.directed().build());
    }

    @Override
    public Iterable<PluginProvider<T>> getRegisteredProviders() {
        return this.providers;
    }

    public void processProvided(PluginProvider<T> provider, T provided) {
    }

    // Mutable enter
    protected void filterLoadingProviders(List<PluginProvider<T>> providers) {
    }

    protected void handleCycle(PluginGraphCycleException exception) {
        List<String> logMessages = new ArrayList<>();
        for (List<String> list : exception.getCycles()) {
            logMessages.add(String.join(" -> ", list) + " -> " + list.get(0));
        }

        LOGGER.error("检测到循环加载插件！");
        LOGGER.error("循环加载顺序：");
        for (String logMessage : logMessages) {
            LOGGER.error("  {}", logMessage);
        }
        LOGGER.error("请将此问题报告给循环中第一个插件的作者，或加入 PaperMC Discord 服务器以获取进一步帮助。");
        LOGGER.error("如果你仍想加载这些插件（知晓可能出现意外的插件加载问题），请使用 -Dpaper.useLegacyPluginLoading=true 运行服务端");

        if (this.throwOnCycle()) {
            throw new IllegalStateException("插件之间存在循环加载：" + exception.getCycles().stream().map(cycle -> cycle.get(0)).collect(Collectors.joining(", ")));
        }
    }

    public boolean throwOnCycle() {
        return true;
    }

    @Override
    public String toString() {
        return "SimpleProviderStorage{" +
            "providers=" + this.providers +
            ", strategy=" + this.strategy +
            '}';
    }
}
