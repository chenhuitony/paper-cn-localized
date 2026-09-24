package org.bukkit.plugin.messaging;

/**
 * Thrown if a plugin attempts to register for a reserved channel (such as
 * "REGISTER")
 */
@SuppressWarnings("serial")
public class ReservedChannelException extends RuntimeException {
    public ReservedChannelException() {
        this("尝试注册保留的通道名称。");
    }

    public ReservedChannelException(String name) {
        super("尝试注册保留的通道名称（'" + name + "')");
    }
}
