package io.papermc.paper.datacomponent;

import java.util.function.Function;
import net.minecraft.core.Holder;
import net.minecraft.core.component.DataComponentType;
import net.minecraft.util.NullOps;
import net.minecraft.util.Unit;
import org.bukkit.craftbukkit.CraftRegistry;

public record DataComponentAdapter<NMS, API>(
    Function<API, NMS> apiToVanilla,
    Function<NMS, API> vanillaToApi,
    boolean codecValidation
) {
    static final Function<Void, Unit> API_TO_UNIT_CONVERTER = _ -> Unit.INSTANCE;

    static final Function API_TO_UNIMPLEMENTED_CONVERTER = _ -> {
        throw new UnsupportedOperationException("无法将 API 值转换为未实现的类型");
    };

    public boolean isValued() {
        return this.apiToVanilla != API_TO_UNIT_CONVERTER;
    }

    public boolean isUnimplemented() {
        return this.apiToVanilla == API_TO_UNIMPLEMENTED_CONVERTER;
    }

    public NMS toVanilla(final API value, final Holder<? extends DataComponentType<NMS>> type) {
        final NMS nms = this.apiToVanilla.apply(value);
        if (this.codecValidation && !type.value().isTransient()) {
            type.value().codecOrThrow().encodeStart(CraftRegistry.getMinecraftRegistry().createSerializationContext(NullOps.INSTANCE), nms).ifError(error -> {
                throw new IllegalArgumentException("编码数据组件 %s (%s) 失败".formatted(type.unwrapKey().orElseThrow(), error.message()));
            });
        }

        return nms;
    }

    public API fromVanilla(final NMS value) {
        return this.vanillaToApi.apply(value);
    }
}
