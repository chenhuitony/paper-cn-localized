package org.spigotmc;

import java.io.File;
import net.kyori.adventure.text.format.NamedTextColor;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import org.bukkit.command.Command;
import org.bukkit.command.CommandSender;

import static net.kyori.adventure.text.Component.text;

public class SpigotCommand extends Command {

    public SpigotCommand(String name) {
        super(name);
        this.description = "Spigot 相关命令";
        this.usageMessage = "/spigot reload";
        this.setPermission("bukkit.command.spigot");
    }

    @Override
    public boolean execute(CommandSender sender, String commandLabel, String[] args) {
        if (!this.testPermission(sender)) return true;

        if (args.length != 1 || !args[0].equals("reload")) {
            sender.sendMessage(text("用法：" + this.usageMessage, NamedTextColor.RED));
        }


        Command.broadcastCommandMessage(sender, text().color(NamedTextColor.RED)
            .append(text("请注意，此命令不受支持，可能引发问题。"))
            .appendNewline()
            .append(text("如遇任何问题，请使用 /stop 命令重启服务器。"))
            .build()
        );

        MinecraftServer console = MinecraftServer.getServer();
        org.spigotmc.SpigotConfig.init((File) console.options.valueOf("spigot-settings"));
        for (ServerLevel world : console.getAllLevels()) {
            world.spigotConfig.init();
        }
        console.server.reloadCount++;

        Command.broadcastCommandMessage(sender, text("重载完成。", NamedTextColor.GREEN));
        

        return true;
    }
}
