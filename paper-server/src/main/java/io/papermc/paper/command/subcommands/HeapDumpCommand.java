package io.papermc.paper.command.subcommands;

import io.papermc.paper.command.PaperSubcommand;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import org.bukkit.command.Command;
import org.bukkit.command.CommandSender;
import org.bukkit.craftbukkit.CraftServer;
import org.checkerframework.checker.nullness.qual.NonNull;
import org.checkerframework.framework.qual.DefaultQualifier;

import static net.kyori.adventure.text.Component.text;
import static net.kyori.adventure.text.format.NamedTextColor.GREEN;
import static net.kyori.adventure.text.format.NamedTextColor.RED;
import static net.kyori.adventure.text.format.NamedTextColor.YELLOW;

@DefaultQualifier(NonNull.class)
public final class HeapDumpCommand implements PaperSubcommand {
    @Override
    public boolean execute(final CommandSender sender, final String subCommand, final String[] args) {
        this.dumpHeap(sender);
        return true;
    }

    private void dumpHeap(final CommandSender sender) {
        java.nio.file.Path dir = java.nio.file.Paths.get("./dumps");
        String name = "heap-dump-" + DateTimeFormatter.ofPattern("yyyy-MM-dd_HH.mm.ss").format(LocalDateTime.now());

        Command.broadcastCommandMessage(sender, text("正在写入 JVM 堆数据...", YELLOW));

        java.nio.file.Path file = CraftServer.dumpHeap(dir, name);
        if (file != null) {
            Command.broadcastCommandMessage(sender, text("堆转储已保存至 " + file, GREEN));
        } else {
            Command.broadcastCommandMessage(sender, text("写入堆转储失败，详情请查看服务器日志", RED));
        }
    }
}
