package io.papermc.paper.adventure;

import com.google.common.base.Suppliers;
import com.mojang.datafixers.util.Pair;
import com.mojang.serialization.JavaOps;
import java.util.function.Supplier;
import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.serializer.ComponentSerializer;
import net.minecraft.network.chat.ComponentSerialization;
import net.minecraft.resources.RegistryOps;
import org.bukkit.craftbukkit.CraftRegistry;

public final class WrapperAwareSerializer implements ComponentSerializer<Component, Component, net.minecraft.network.chat.Component> {

    private final Supplier<RegistryOps<Object>> javaOps;

    public WrapperAwareSerializer(final Supplier<RegistryOps<Object>> javaOps) {
        this.javaOps = Suppliers.memoize(javaOps::get);
    }

    @Override
    public Component deserialize(final net.minecraft.network.chat.Component input) {
        if (input instanceof AdventureComponent) {
            return ((AdventureComponent) input).adventure;
        }
        final RegistryOps<Object> ops = this.javaOps.get();
        final Object obj = ComponentSerialization.CODEC.encodeStart(ops, input)
            .getOrThrow(s -> new RuntimeException("编码 Minecraft Component 失败：" + input + "; " + s));
        final Pair<Component, Object> converted = AdventureCodecs.COMPONENT_CODEC.decode(ops, obj)
            .getOrThrow(s -> new RuntimeException("解码为 adventure Component 失败：" + obj + "; " + s));
        return converted.getFirst();
    }

    @Override
    public net.minecraft.network.chat.Component serialize(final Component component) {
        final RegistryOps<Object> ops = this.javaOps.get();
        final Object obj = AdventureCodecs.COMPONENT_CODEC.encodeStart(ops, component)
            .getOrThrow(s -> new RuntimeException("编码 adventure Component 失败：" + component + "; " + s));
        final Pair<net.minecraft.network.chat.Component, Object> converted = ComponentSerialization.CODEC.decode(ops, obj)
            .getOrThrow(s -> new RuntimeException("解码为 Minecraft Component 失败：" + obj + "; " + s));
        return converted.getFirst();
    }
}
