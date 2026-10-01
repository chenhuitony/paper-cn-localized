package io.papermc.paper.command.subcommands;

import io.papermc.paper.command.PaperSubcommand;
import net.minecraft.server.MinecraftServer;
import org.bukkit.command.Command;
import org.bukkit.command.CommandSender;
import org.bukkit.craftbukkit.CraftServer;
import org.checkerframework.checker.nullness.qual.NonNull;
import org.checkerframework.framework.qual.DefaultQualifier;

import static net.kyori.adventure.text.Component.text;
import static net.kyori.adventure.text.format.NamedTextColor.GREEN;
import static net.kyori.adventure.text.format.NamedTextColor.RED;

@DefaultQualifier(NonNull.class)
public final class ReloadCommand implements PaperSubcommand {
    @Override
    public boolean execute(final CommandSender sender, final String subCommand, final String[] args) {
        this.doReload(sender);
        return true;
    }

    private void doReload(final CommandSender sender) {
        Command.broadcastCommandMessage(sender, text("请注意，此命令不受支持，可能引发问题。", RED));
        Command.broadcastCommandMessage(sender, text("如遇任何问题，请使用 /stop 命令重启服务器。", RED));

        MinecraftServer server = ((CraftServer) sender.getServer()).getServer();
        server.paperConfigurations.reloadConfigs(server);
        server.server.reloadCount++;

        Command.broadcastCommandMessage(sender, text("Paper 配置重载完成。", GREEN));
    }
}
