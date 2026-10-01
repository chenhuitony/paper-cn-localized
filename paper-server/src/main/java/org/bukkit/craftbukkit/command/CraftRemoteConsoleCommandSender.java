package org.bukkit.craftbukkit.command;

import java.net.SocketAddress;
import net.minecraft.network.chat.Component;
import net.minecraft.server.rcon.RconConsoleSource;
import org.bukkit.command.RemoteConsoleCommandSender;

public class CraftRemoteConsoleCommandSender extends ServerCommandSender implements RemoteConsoleCommandSender {

    private final RconConsoleSource listener;

    public CraftRemoteConsoleCommandSender(RconConsoleSource listener) {
        this.listener = listener;
    }

    public RconConsoleSource getListener() {
        return this.listener;
    }

    @Override
    public SocketAddress getAddress() {
       return this.listener.socketAddress;
    }

    @Override
    public void sendMessage(String message) {
        this.listener.sendSystemMessage(Component.literal(message + "\n")); // Send a newline after each message, to preserve formatting.
    }

    @Override
    public void sendMessage(String... messages) {
        for (String message : messages) {
            this.sendMessage(message);
        }
    }

    @Override
    public String getName() {
        return "Rcon";
    }

    @Override
    public net.kyori.adventure.text.Component name() {
        return net.kyori.adventure.text.Component.text(this.getName());
    }

    @Override
    public boolean isOp() {
        return true;
    }

    @Override
    public void setOp(boolean value) {
        throw new UnsupportedOperationException("无法更改远程控制器的操作员状态。");
    }

    @Override
    public boolean hasPermission(String name) {
        return io.papermc.paper.configuration.GlobalConfiguration.get().console.hasAllPermissions || super.hasPermission(name);
    }

    @Override
    public boolean hasPermission(org.bukkit.permissions.Permission perm) {
        return io.papermc.paper.configuration.GlobalConfiguration.get().console.hasAllPermissions || super.hasPermission(perm);
    }
}
