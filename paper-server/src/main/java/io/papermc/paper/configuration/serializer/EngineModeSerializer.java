package io.papermc.paper.configuration.serializer;

import io.papermc.paper.configuration.type.EngineMode;
import java.lang.reflect.Type;
import java.util.function.Predicate;
import org.spongepowered.configurate.serialize.ScalarSerializer;
import org.spongepowered.configurate.serialize.SerializationException;

public final class EngineModeSerializer extends ScalarSerializer<EngineMode> {

    public EngineModeSerializer() {
        super(EngineMode.class);
    }

    @Override
    public EngineMode deserialize(final Type type, final Object obj) throws SerializationException {
        if (obj instanceof final Integer id) {
            try {
                return EngineMode.valueOf(id);
            } catch (final IllegalArgumentException e) {
                throw new SerializationException(id + " 不是以下类型的有效 id：" + type + "（此节点）");
            }
        }

        throw new SerializationException(obj + " 不是有效的类型 " + type + "（此节点）");
    }

    @Override
    protected Object serialize(final EngineMode item, final Predicate<Class<?>> typeSupported) {
        return item.getId();
    }
}
