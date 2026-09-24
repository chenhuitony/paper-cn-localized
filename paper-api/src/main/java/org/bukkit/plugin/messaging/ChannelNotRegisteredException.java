package org.bukkit.plugin.messaging;

/**
 * Thrown if a Plugin attempts to send a message on an unregistered channel.
 */
@SuppressWarnings("serial")
public class ChannelNotRegisteredException extends RuntimeException {
    public ChannelNotRegisteredException() {
        this("尝试通过未注册的通道发送插件消息。");
    }

    public ChannelNotRegisteredException(String channel) {
        super("尝试通过未注册的通道 ` 发送插件消息" + channel + "'.");
    }
}
