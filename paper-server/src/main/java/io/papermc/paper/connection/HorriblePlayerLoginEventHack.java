package io.papermc.paper.connection;

import com.mojang.authlib.GameProfile;
import com.mojang.logging.LogUtils;
import io.papermc.paper.adventure.PaperAdventure;
import io.papermc.paper.util.StackWalkerUtil;
import java.util.HashSet;
import java.util.Optional;
import java.util.Set;
import net.minecraft.network.Connection;
import net.minecraft.network.chat.Component;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ClientInformation;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.server.players.PlayerList;
import org.bukkit.craftbukkit.entity.CraftPlayer;
import org.bukkit.event.player.PlayerLoginEvent;
import org.bukkit.plugin.RegisteredListener;
import org.jspecify.annotations.NullMarked;
import org.jspecify.annotations.Nullable;
import org.slf4j.Logger;

// TODO: DO we even need this? Who mutates the player here? it does nothing anyways.
// TODO: Make sure player settings are migrated too
@NullMarked
@Deprecated
public class HorriblePlayerLoginEventHack {

    private static final Logger LOGGER = LogUtils.getClassLogger();
    private static boolean nagged = false;

    public static boolean warnReenterConfiguration(final Connection connection) {
        if (!connection.handledLegacyLoginEvent) {
            return false;
        }
        LOGGER.warn("""
                
                ============================================================
                警告: {} 尝试调用 PlayerGameConnection#reenterConfiguration()
                
                该方法目前要求服务端上安装的所有插件
                都没有监听 PlayerLoginEvent 事件。
                
                请在日志中查找监听此事件的插件。
                ============================================================""", StackWalkerUtil.getFirstPluginCaller().getName());
        return true;
    }

    public static @Nullable Component execute(final Connection connection, MinecraftServer server, GameProfile profile, PlayerList.LoginResult result) {
        if (PlayerLoginEvent.getHandlerList().getRegisteredListeners().length == 0) {
            return result.message();
        }

        if (!nagged) {
            Set<String> plugins = new HashSet<>();
            for (final RegisteredListener listener : PlayerLoginEvent.getHandlerList().getRegisteredListeners()) {
                plugins.add(listener.getPlugin().getName());
            }
            if (true) {
                LOGGER.info("有插件监听了 PlayerLoginEvent，这将导致重新配置 API 不可用：{}", plugins);
            } else {
                LOGGER.warn("""
                    
                    ============================================================
                    警告: 检测到已废弃的 PlayerLoginEvent 用法！
                    
                    该事件会强制走一条已废弃的玩家加载路径，
                    并将在未来版本中被移除。
                    更多信息请参见: https://go.papermc.io/announcement/1.21.7
                    
                    请通知以下插件开发者: {}
                    ============================================================""", plugins);
            }
            nagged = true;
        }
        // We need to account for the fact that during the config stage we now call this event to mimic the old behavior.
        // However, we want to make sure that we still properly hold the same player reference
        ServerPlayer player;
        if (connection.savedPlayerForLegacyEvents != null) {
            player = connection.savedPlayerForLegacyEvents;
        } else {
            ServerPlayer serverPlayer = new ServerPlayer(server, server.overworld(), profile, ClientInformation.createDefault());
            connection.savedPlayerForLegacyEvents = serverPlayer;
            player = serverPlayer;
        }
        connection.handledLegacyLoginEvent = true;

        CraftPlayer horribleBukkitPlayer = player.getBukkitEntity();
        PlayerLoginEvent event = new PlayerLoginEvent(horribleBukkitPlayer, connection.hostname, ((java.net.InetSocketAddress) connection.getRemoteAddress()).getAddress(), ((java.net.InetSocketAddress) connection.channel.remoteAddress()).getAddress());
        event.disallow(result.result(), PaperAdventure.asAdventure(result.message()));
        event.callEvent();

        Component finalResult;
        if (event.getResult() == PlayerLoginEvent.Result.ALLOWED) {
            finalResult = null;
        } else {
            finalResult = PaperAdventure.asVanilla(event.kickMessage());
        }

        // If the event changed the result, save this result. We need to save this for config
        if (event.getResult() != result.result()) {
            connection.legacySavedLoginEventResultOverride = Optional.ofNullable(finalResult);
        }

        return finalResult;
    }
}
