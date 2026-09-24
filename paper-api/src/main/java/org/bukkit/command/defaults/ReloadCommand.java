package org.bukkit.command.defaults;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.command.Command;
import org.bukkit.command.CommandSender;
import org.jetbrains.annotations.NotNull;

import static net.kyori.adventure.text.Component.text;

public class ReloadCommand extends BukkitCommand {
    public ReloadCommand(@NotNull String name) {
        super(name);
        this.description = "重载服务端配置和插件";
        this.usageMessage = "/reload [permissions|commands|confirm]"; // Paper
        this.setPermission("bukkit.command.reload");
        this.setAliases(Arrays.asList("rl"));
    }

    @org.jetbrains.annotations.ApiStatus.Internal // Paper
    public static final String RELOADING_DISABLED_MESSAGE = "已注册生命周期事件处理器，导致无法重载插件"; // Paper

    @Override
    public boolean execute(@NotNull CommandSender sender, @NotNull String currentAlias, @NotNull String[] args) { // Paper
        if (!testPermission(sender)) return true;

        boolean confirmed = System.getProperty("LetMeReload") != null;
        if (args.length == 1) {
            if (args[0].equalsIgnoreCase("permissions")) {
                Bukkit.getServer().reloadPermissions();
                Command.broadcastCommandMessage(sender, text("权限已成功重载。", net.kyori.adventure.text.format.NamedTextColor.GREEN));
                return true;
            } else if ("commands".equalsIgnoreCase(args[0])) {
                if (Bukkit.getServer().reloadCommandAliases()) {
                    Command.broadcastCommandMessage(sender, text("命令别名已成功重载。", net.kyori.adventure.text.format.NamedTextColor.GREEN));
                } else {
                    Command.broadcastCommandMessage(sender, text("重载命令别名时出错。", net.kyori.adventure.text.format.NamedTextColor.RED));
                }
                return true;
            } else if ("confirm".equalsIgnoreCase(args[0])) {
                confirmed = true;
            } else {
                Command.broadcastCommandMessage(sender, text("Usage: " + usageMessage, net.kyori.adventure.text.format.NamedTextColor.RED));
                return true;
            }
        }
        if (!confirmed) {
            Command.broadcastCommandMessage(sender, text("你确定要重载服务端吗？此命令即将被移除。这样做可能导致 Bug 和内存泄漏。建议重启而不是使用 /bukkit:reload。要确认，请输入 ", net.kyori.adventure.text.format.NamedTextColor.RED).append(text("/bukkit:reload confirm", net.kyori.adventure.text.format.NamedTextColor.YELLOW)));
            return true;
        }

        Command.broadcastCommandMessage(sender, ChatColor.RED + "请注意，此命令不受支持，在使用某些插件时可能导致问题，并且将在不久后移除。");
        Command.broadcastCommandMessage(sender, ChatColor.RED + "如果你遇到任何问题，请使用 /stop 命令重启服务端。");
        // Paper start - lifecycle events
        try {
            Bukkit.reload();
        } catch (final IllegalStateException ex) {
            if (ex.getMessage().equals(RELOADING_DISABLED_MESSAGE)) {
                Command.broadcastCommandMessage(sender, ChatColor.RED + RELOADING_DISABLED_MESSAGE);
                return true;
            }
        }
        // Paper end - lifecycle events
        Command.broadcastCommandMessage(sender, ChatColor.GREEN + "重载完成。");

        return true;
    }

    @NotNull
    @Override
    public List<String> tabComplete(@NotNull CommandSender sender, @NotNull String alias, @NotNull String[] args) throws IllegalArgumentException {
        return com.google.common.collect.Lists.newArrayList("permissions", "commands"); // Paper
    }
}
