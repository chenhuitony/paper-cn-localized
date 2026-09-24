package io.papermc.paper.command.subcommands;

import com.destroystokyo.paper.util.SneakyThrow;
import io.papermc.paper.command.PaperSubcommand;
import java.io.IOException;
import java.io.PrintWriter;
import java.lang.invoke.MethodHandle;
import java.lang.invoke.MethodHandles;
import java.lang.reflect.Field;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Locale;
import java.util.Set;
import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.event.ClickEvent;
import net.minecraft.server.MinecraftServer;
import org.bukkit.Bukkit;
import org.bukkit.command.CommandSender;
import org.bukkit.event.HandlerList;
import org.bukkit.plugin.Plugin;
import org.bukkit.plugin.RegisteredListener;
import org.checkerframework.checker.nullness.qual.NonNull;
import org.checkerframework.checker.nullness.qual.Nullable;
import org.checkerframework.framework.qual.DefaultQualifier;

import static net.kyori.adventure.text.Component.newline;
import static net.kyori.adventure.text.Component.space;
import static net.kyori.adventure.text.Component.text;
import static net.kyori.adventure.text.format.NamedTextColor.GRAY;
import static net.kyori.adventure.text.format.NamedTextColor.GREEN;
import static net.kyori.adventure.text.format.NamedTextColor.RED;
import static net.kyori.adventure.text.format.NamedTextColor.WHITE;

@DefaultQualifier(NonNull.class)
public final class DumpListenersCommand implements PaperSubcommand {
    private static final DateTimeFormatter FORMATTER = DateTimeFormatter.ofPattern("yyyy-MM-dd_HH.mm.ss");
    private static final String COMMAND_ARGUMENT_TO_FILE = "tofile";
    private static final MethodHandle EVENT_TYPES_HANDLE;

    static {
        try {
            final Field eventTypesField = HandlerList.class.getDeclaredField("EVENT_TYPES");
            eventTypesField.setAccessible(true);
            EVENT_TYPES_HANDLE = MethodHandles.lookup().unreflectGetter(eventTypesField);
        } catch (final ReflectiveOperationException e) {
            throw new RuntimeException(e);
        }
    }

    @Override
    public boolean execute(final CommandSender sender, final String subCommand, final String[] args) {
        if (args.length >= 1 && args[0].equals(COMMAND_ARGUMENT_TO_FILE)) {
            this.dumpToFile(sender);
            return true;
        }
        this.doDumpListeners(sender, args);
        return true;
    }

    private void dumpToFile(final CommandSender sender) {
        Path parent = Path.of("debug");
        Path path = parent.resolve("listeners-" + FORMATTER.format(LocalDateTime.now()) + ".txt");
        sender.sendMessage(
            text("正在将监听器写入目录", GREEN)
                .appendSpace()
                .append(
                    text(parent.toString(), WHITE)
                        .hoverEvent(text("点击复制调试目录的完整路径", WHITE))
                        .clickEvent(ClickEvent.copyToClipboard(parent.toAbsolutePath().toString()))
                )
        );
        try {
            Files.createDirectories(parent);
            Files.createFile(path);
            try (final PrintWriter writer = new PrintWriter(path.toFile())) {
                for (final String eventClass : eventClassNames()) {
                    final HandlerList handlers;
                    try {
                        handlers = (HandlerList) findClass(eventClass).getMethod("getHandlerList").invoke(null);
                    } catch (final ReflectiveOperationException e) {
                        continue;
                    }
                    if (handlers.getRegisteredListeners().length != 0) {
                        writer.println(eventClass);
                    }
                    for (final RegisteredListener registeredListener : handlers.getRegisteredListeners()) {
                        writer.println(" - " + registeredListener);
                    }
                }
            }
        } catch (final IOException ex) {
            sender.sendMessage(text("写入监听器转储失败！详情请查看控制台。", RED));
            MinecraftServer.LOGGER.warn("Error occurred while dumping listeners", ex);
            return;
        }
        sender.sendMessage(
            text("监听器已成功写入", GREEN)
                .appendSpace()
                .append(
                    text(path.toString(), WHITE)
                        .hoverEvent(text("点击复制该文件的完整路径", WHITE))
                        .clickEvent(ClickEvent.copyToClipboard(path.toAbsolutePath().toString()))
                )
        );
    }

    private void doDumpListeners(final CommandSender sender, final String[] args) {
        if (args.length == 0) {
            sender.sendMessage(text("用法：/paper dumplisteners " + COMMAND_ARGUMENT_TO_FILE + "|<类名>", RED));
            return;
        }

        final String className = args[0];

        try {
            final HandlerList handlers = (HandlerList) findClass(className).getMethod("getHandlerList").invoke(null);

            if (handlers.getRegisteredListeners().length == 0) {
                sender.sendMessage(text(className + " 未注册任何监听器。"));
                return;
            }

            sender.sendMessage(text(className + " 的监听器："));

            for (final RegisteredListener listener : handlers.getRegisteredListeners()) {
                final Component hoverText = text("优先级：" + listener.getPriority().name() + "（" + listener.getPriority().getSlot() + "）", WHITE)
                    .append(newline())
                    .append(text("监听器：" + listener.getListener()))
                    .append(newline())
                    .append(text("执行器：" + listener.getExecutor()))
                    .append(newline())
                    .append(text("忽略已取消事件：" + listener.isIgnoringCancelled()));

                sender.sendMessage(text(listener.getPlugin().getName(), GREEN)
                    .append(space())
                    .append(text("(" + listener.getListener().getClass().getName() + ")", GRAY).hoverEvent(hoverText)));
            }

            sender.sendMessage(text("监听器总数：" + handlers.getRegisteredListeners().length));

        } catch (final ClassNotFoundException e) {
            sender.sendMessage(text("找不到名为 '" + className + "' 的类。请确保使用完全限定名。", RED));
        } catch (final NoSuchMethodException e) {
            sender.sendMessage(text("类 '" + className + "' 没有有效的 getHandlerList 方法。", RED));
        } catch (final ReflectiveOperationException e) {
            sender.sendMessage(text("发生错误，详情请查看控制台。", RED));
            MinecraftServer.LOGGER.warn("Error occurred while dumping listeners for class {}", className, e);
        }
    }

    @Override
    public List<String> tabComplete(final CommandSender sender, final String subCommand, final String[] args) {
        return switch (args.length) {
            case 0 -> suggestions();
            case 1 -> suggestions().stream()
                .filter(clazz -> clazz.toLowerCase(Locale.ROOT).contains(args[0].toLowerCase(Locale.ROOT)))
                .toList();
            default -> Collections.emptyList();
        };
    }

    private static List<String> suggestions() {
        final List<String> ret = new ArrayList<>();
        ret.add(COMMAND_ARGUMENT_TO_FILE);
        ret.addAll(eventClassNames());
        return ret;
    }

    @SuppressWarnings("unchecked")
    private static Set<String> eventClassNames() {
        try {
            return (Set<String>) EVENT_TYPES_HANDLE.invokeExact();
        } catch (final Throwable e) {
            SneakyThrow.sneaky(e);
            return Collections.emptySet(); // Unreachable
        }
    }

    private static Class<?> findClass(final String className) throws ClassNotFoundException {
        try {
            return Class.forName(className);
        } catch (final ClassNotFoundException ignore) {
            for (final Plugin plugin : Bukkit.getServer().getPluginManager().getPlugins()) {
                if (!plugin.isEnabled()) {
                    continue;
                }

                try {
                    return Class.forName(className, false, plugin.getClass().getClassLoader());
                } catch (final ClassNotFoundException ignore0) {
                }
            }
        }
        throw new ClassNotFoundException(className);
    }
}
