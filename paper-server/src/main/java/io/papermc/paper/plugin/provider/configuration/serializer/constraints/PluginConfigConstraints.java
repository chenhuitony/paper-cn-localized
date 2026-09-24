package io.papermc.paper.plugin.provider.configuration.serializer.constraints;

import io.papermc.paper.plugin.util.NamespaceChecker;
import org.spongepowered.configurate.objectmapping.meta.Constraint;
import org.spongepowered.configurate.serialize.SerializationException;

import java.lang.annotation.Documented;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;
import java.lang.reflect.Type;
import java.util.Locale;
import java.util.Set;
import java.util.regex.Pattern;

public final class PluginConfigConstraints {

    public static final Set<String> RESERVED_KEYS = Set.of("bukkit", "minecraft", "mojang", "spigot", "paper");

    @Documented
    @Retention(RetentionPolicy.RUNTIME)
    @Target(ElementType.FIELD)
    public @interface PluginName {

        final class Factory implements Constraint.Factory<PluginName, String> {

            private static final Pattern VALID_NAME = Pattern.compile("^[A-Za-z\\d _.-]+$");

            @Override
            public Constraint<String> make(PluginName data, Type type) {
                return value -> {
                    if (value != null) {
                        if (RESERVED_KEYS.contains(value.toLowerCase(Locale.ROOT))) {
                            throw new SerializationException("名称受限，不能将 '%s' 用作插件名称。".formatted(data));
                        } else if (value.indexOf(' ') != -1) {
                            // For legacy reasons, the space condition has a separate exception message.
                            throw new SerializationException("名称受限，插件名称中不能使用 0x20（空格字符）。");
                        }

                        if (!VALID_NAME.matcher(value).matches()) {
                            throw new SerializationException("名称 '" + value + "' 包含非法字符。");
                        }
                    }
                };
            }
        }
    }

    @Documented
    @Retention(RetentionPolicy.RUNTIME)
    @Target(ElementType.FIELD)
    public @interface PluginNameSpace {

        final class Factory implements Constraint.Factory<PluginNameSpace, String> {

            @Override
            public Constraint<String> make(PluginNameSpace data, Type type) {
                return value -> {
                    if (value != null && !NamespaceChecker.isValidNameSpace(value)) {
                        throw new SerializationException("提供的类 '%s' 位于无效的命名空间中。".formatted(value));
                    }
                };
            }
        }
    }
}
