package org.bukkit.plugin.messaging;

/**
 * Thrown if a Plugin Channel is too long.
 */
@SuppressWarnings("serial")
public class ChannelNameTooLongException extends RuntimeException {
    public ChannelNameTooLongException() {
        super("尝试向过大的通道发送插件消息。通道的最大长度为 " + Messenger.MAX_CHANNEL_SIZE + " chars.");
    }

    // Paper start
    public ChannelNameTooLongException(int length, String shortenedChannel) {
        super("尝试向过大的通道发送插件消息。通道的最大长度为 " + Messenger.MAX_CHANNEL_SIZE + " 个字符（尝试了 " + length + " - '" + shortenedChannel + ".");
        // Paper end
    }
}
