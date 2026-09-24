package org.bukkit.util.permissions;

import org.bukkit.permissions.Permission;
import org.bukkit.permissions.PermissionDefault;
import org.jetbrains.annotations.NotNull;

public final class CommandPermissions {
    private static final String ROOT = "bukkit.command";
    private static final String PREFIX = ROOT + ".";

    private CommandPermissions() {}

    @NotNull
    public static Permission registerPermissions(@NotNull Permission parent) {
        Permission commands = DefaultPermissions.registerPermission(ROOT, "允许用户使用所有 CraftBukkit 命令", parent);

        DefaultPermissions.registerPermission(PREFIX + "help", "允许用户查看原版帮助菜单", PermissionDefault.TRUE, commands);
        DefaultPermissions.registerPermission(PREFIX + "plugins", "允许用户查看此服务端上运行的插件列表", PermissionDefault.TRUE, commands);
        DefaultPermissions.registerPermission(PREFIX + "reload", "允许用户重载服务端设置", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(PREFIX + "version", "允许用户查看服务端版本", PermissionDefault.TRUE, commands);

        commands.recalculatePermissibles();
        return commands;
    }
}
