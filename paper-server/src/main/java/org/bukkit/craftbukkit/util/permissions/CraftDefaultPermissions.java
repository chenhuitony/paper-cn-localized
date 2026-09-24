package org.bukkit.craftbukkit.util.permissions;

import org.bukkit.permissions.Permission;
import org.bukkit.util.permissions.DefaultPermissions;

public final class CraftDefaultPermissions {
    private static final String ROOT = "minecraft";

    private CraftDefaultPermissions() {}

    public static void registerCorePermissions() {
        Permission parent = DefaultPermissions.registerPermission(CraftDefaultPermissions.ROOT, "允许用户使用所有原版实用功能和命令");
        CommandPermissions.registerPermissions(parent);
        DefaultPermissions.registerPermission(CraftDefaultPermissions.ROOT + ".nbt.place", "允许用户在创造模式下放置带有 NBT 的受限方块", org.bukkit.permissions.PermissionDefault.OP, parent);
        DefaultPermissions.registerPermission(CraftDefaultPermissions.ROOT + ".nbt.copy", "允许用户在创造模式下复制 NBT", org.bukkit.permissions.PermissionDefault.TRUE, parent);
        DefaultPermissions.registerPermission(CraftDefaultPermissions.ROOT + ".debugstick", "允许用户在创造模式下使用调试棒", org.bukkit.permissions.PermissionDefault.OP, parent);
        DefaultPermissions.registerPermission(CraftDefaultPermissions.ROOT + ".debugstick.always", "允许用户在所有游戏模式下使用调试棒", org.bukkit.permissions.PermissionDefault.FALSE/* , parent */); // Paper - should not have this parent, as it's not a "vanilla" utility
        DefaultPermissions.registerPermission(CraftDefaultPermissions.ROOT + ".commandblock", "允许用户使用命令方块。", org.bukkit.permissions.PermissionDefault.OP, parent); // Paper
        parent.recalculatePermissibles();
    }
}
