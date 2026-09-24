package org.bukkit.plugin;

import com.google.common.base.Preconditions;
import io.papermc.paper.event.executor.EventExecutorFactory;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import org.bukkit.event.Event;
import org.bukkit.event.EventException;
import org.bukkit.event.Listener;
import org.bukkit.plugin.java.JavaPlugin;
import org.jetbrains.annotations.NotNull;

/**
 * Interface which defines the class for event call backs to plugins
 */
public interface EventExecutor {
    public void execute(@NotNull Listener listener, @NotNull Event event) throws EventException;

    // Paper start
    @NotNull
    static EventExecutor create(@NotNull Method m, @NotNull Class<? extends Event> eventClass) {
        Preconditions.checkNotNull(m, "方法为 null");
        Preconditions.checkArgument(m.getParameterCount() != 0, "参数数量不正确：%s", m.getParameterCount());
        Preconditions.checkArgument(m.getParameterTypes()[0] == eventClass, "第一个参数 %s 与事件类 %s 不匹配", m.getParameterTypes()[0], eventClass);
        if (m.getReturnType() != Void.TYPE) {
            final JavaPlugin plugin = JavaPlugin.getProvidingPlugin(m.getDeclaringClass());
            org.bukkit.Bukkit.getLogger().warning("@EventHandler 方法 " + m.getDeclaringClass().getName() + (Modifier.isStatic(m.getModifiers()) ? '.' : '#') + m.getName()
                + " 返回非 void 类型 " + m.getReturnType().getName() + "。这是不受支持的行为，并将在未来版本的 Paper 中失效。"
                + " 此问题应报告给以下插件的开发者: " + plugin.getPluginMeta().getDisplayName() + " (" + String.join(",", plugin.getPluginMeta().getAuthors()) + ')');
        }
        if (!m.trySetAccessible()) {
            final JavaPlugin plugin = JavaPlugin.getProvidingPlugin(m.getDeclaringClass());
            throw new AssertionError(
                "@EventHandler 方法 " + m.getDeclaringClass().getName() + (Modifier.isStatic(m.getModifiers()) ? '.' : '#') + m.getName() + " 不可访问。"
                    + " 此问题应报告给以下插件的开发者: " + plugin.getDescription().getName() + " (" + String.join(",", plugin.getDescription().getAuthors()) + ')'
            );
        }
        return EventExecutorFactory.create(m, eventClass);
    }
    // Paper end
}
