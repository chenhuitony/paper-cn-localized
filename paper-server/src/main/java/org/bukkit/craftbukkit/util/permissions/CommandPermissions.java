package org.bukkit.craftbukkit.util.permissions;

import org.bukkit.permissions.Permission;
import org.bukkit.permissions.PermissionDefault;
import org.bukkit.util.permissions.DefaultPermissions;

public final class CommandPermissions {
    private static final String ROOT = "minecraft.command";
    private static final String PREFIX = CommandPermissions.ROOT + ".";

    private CommandPermissions() {}

    public static Permission registerPermissions(Permission parent) {
        Permission commands = DefaultPermissions.registerPermission(CommandPermissions.ROOT, "允许用户使用所有原版 Minecraft 命令", parent);

        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "kill", "允许用户自杀", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "me", "允许用户执行聊天动作", PermissionDefault.TRUE, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "msg", "允许用户私下向其他玩家发消息", PermissionDefault.TRUE, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "help", "允许用户查看原版命令帮助", PermissionDefault.TRUE, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "say", "允许用户以控制台身份发言", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "give", "允许用户给予玩家物品", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "teleport", "允许用户传送玩家", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "kick", "允许用户踢出玩家", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "stop", "允许用户停止服务端", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "list", "允许用户列出所有在线玩家", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "gamemode", "允许用户更改其他玩家的游戏模式", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "experience", "允许用户给自己或他人任意数量的经验", PermissionDefault.OP, commands); // Paper - wrong permission; redirects are de-redirected and the root literal name is used, so xp -> experience
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "defaultgamemode", "允许用户更改服务端的默认游戏模式", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "seed", "允许用户查看世界种子", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "effect", "允许给玩家添加/移除效果", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "selector", "允许使用选择器", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "trigger", "允许使用 trigger 命令", PermissionDefault.TRUE, commands);
        // Paper start
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "advancement", "允许用户给予、移除或查看玩家进度", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "attribute", "允许用户查询、添加、移除或设置实体属性", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "ban", "允许用户将玩家加入封禁列表", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "ban-ip", "允许用户将 IP 地址加入封禁列表", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "banlist", "允许用户显示封禁列表", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "bossbar", "允许用户创建和修改 Boss 血条", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "clear", "允许用户清空玩家物品栏中的物品", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "clone", "允许用户将方块从一处复制到另一处", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "damage", "允许用户使用 damage 命令伤害实体", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "data", "允许用户获取、合并、修改和移除方块实体及实体的 NBT 数据", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "datapack", "允许用户控制已加载的数据包", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "debug", "允许用户开启或关闭调试会话", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "deop", "允许用户撤销玩家的管理员权限", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "dialog", "允许用户显示对话框", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "difficulty", "允许用户设置难度等级", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "enchant", "允许用户为玩家物品附魔", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "execute", "允许用户执行另一条命令", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "fetchprofile", "允许用户通过名称或 id 获取玩家档案", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "fill", "允许用户用指定方块填充区域", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "fillbiome", "允许用户用指定生物群系填充区域", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "forceload", "允许用户强制区块持续加载或不加载", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "function", "允许用户运行函数", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "gamerule", "允许用户设置或查询游戏规则值", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "item", "允许用户替换物品栏中的物品", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "jfr", "允许用户使用原版 Java FlightRecorder 性能分析系统", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "locate", "允许用户定位最近的结构", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "loot", "允许用户将物品从物品栏槽位丢到地面", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "op", "允许用户给予玩家管理员权限", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "pardon", "允许用户从玩家封禁列表中移除条目", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "pardon-ip", "允许用户从 IP 封禁列表中移除条目", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "particle", "允许用户创建粒子", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "perf", "允许用户开启/关闭原版性能指标采集", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "place", "允许用户放置地物和结构", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "playsound", "允许用户播放音效", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "random", "允许用户生成随机数", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "recipe", "允许用户给予或移除配方", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "reload", "允许用户从磁盘重载战利品表、进度和函数", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "return", "允许用户使用 /return 命令", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "ride", "允许用户使用 /ride 命令控制骑乘者", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "rotate", "允许用户更改实体的朝向", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "save-all", "允许用户将服务端数据保存到磁盘", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "save-off", "允许用户关闭服务端自动保存", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "save-on", "允许用户开启服务端自动保存", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "schedule", "允许用户延迟执行函数", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "scoreboard", "允许用户管理记分板目标和玩家", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "setblock", "允许用户将一个方块替换为另一个方块", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "setidletimeout", "允许用户设置空闲玩家被踢出的时间", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "setworldspawn", "允许用户设置世界出生点", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "spawnpoint", "允许用户设置玩家的出生点", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "spectate", "允许用户让旁观者模式的玩家旁观某个实体", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "spreadplayers", "允许用户将实体传送到随机位置", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "stopsound", "允许用户停止音效", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "summon", "允许用户召唤实体", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "swing", "允许用户摆动实体的手臂", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "tag", "允许用户控制实体标签", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "team", "允许用户控制队伍", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "teammsg", "允许用户指定发送给队伍的消息", PermissionDefault.TRUE, commands); // defaults to all players
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "tellraw", "允许向玩家显示 JSON 消息", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "test", "允许用户管理和执行 GameTest", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "tick", "允许用户控制服务端的 tick 速率", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "time", "允许用户更改或查询世界的游戏时间", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "title", "允许用户管理屏幕标题", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "transfer", "允许用户 transfer 到另一个服务端", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "version", "显示与服务端版本相关的信息", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "waypoint", "允许管理服务端/定位栏中的路径点", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "weather", "允许用户设置天气", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "whitelist", "允许用户管理服务端白名单", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "worldborder", "允许用户管理世界边界", PermissionDefault.OP, commands);
        DefaultPermissions.registerPermission(CommandPermissions.PREFIX + "stopwatch", "允许用户使用 /stopwatch 命令", PermissionDefault.OP, commands);
        // Paper end

        DefaultPermissions.registerPermission("minecraft.admin.command_feedback", "当 sendCommandFeedback 为 true 时接收命令广播", PermissionDefault.OP, commands);

        commands.recalculatePermissibles();
        return commands;
    }
}
