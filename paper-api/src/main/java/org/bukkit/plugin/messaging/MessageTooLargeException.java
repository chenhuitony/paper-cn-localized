package org.bukkit.plugin.messaging;

/**
 * Thrown if a Plugin Message is sent that is too large to be sent.
 */
@SuppressWarnings("serial")
public class MessageTooLargeException extends RuntimeException {
    public MessageTooLargeException() {
        this("尝试发送过大的插件消息。插件消息的最大长度为 " + Messenger.MAX_MESSAGE_SIZE + " bytes.");
    }

    public MessageTooLargeException(byte[] message) {
        this(message.length);
    }

    public MessageTooLargeException(int length) {
        this("尝试发送过大的插件消息。插件消息的最大长度为 " + Messenger.MAX_MESSAGE_SIZE + " 字节（尝试发送的消息大小为 " + length + " 字节）。");
    }

    public MessageTooLargeException(String msg) {
        super(msg);
    }
}
