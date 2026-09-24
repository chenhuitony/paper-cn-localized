package org.bukkit.craftbukkit.damage;

import com.google.common.base.Preconditions;
import net.kyori.adventure.pointer.Pointers;
import org.bukkit.Location;
import org.bukkit.damage.DamageSource;
import org.bukkit.damage.DamageType;
import org.bukkit.entity.Entity;
import java.util.function.Consumer;

public class CraftDamageSourceBuilder implements DamageSource.Builder {

    private final DamageType damageType;
    private Entity causingEntity;
    private Entity directEntity;
    private Location damageLocation;
    private Pointers.Builder damageContext;

    public CraftDamageSourceBuilder(DamageType damageType) {
        Preconditions.checkArgument(damageType != null, "DamageType 不能为 null");
        this.damageType = damageType;
        this.damageContext = Pointers.builder();
    }

    @Override
    public DamageSource.Builder withCausingEntity(Entity entity) {
        Preconditions.checkArgument(entity != null, "实体不能为 null");
        this.causingEntity = entity;
        return this;
    }

    @Override
    public DamageSource.Builder withDirectEntity(Entity entity) {
        Preconditions.checkArgument(entity != null, "实体不能为 null");
        this.directEntity = entity;
        return this;
    }

    @Override
    public DamageSource.Builder withDamageLocation(Location location) {
        Preconditions.checkArgument(location != null, "位置不能为 null");
        this.damageLocation = location.clone();
        return this;
    }

    @Override
    public DamageSource.Builder withDamageContext(Consumer<Pointers.Builder> consumer) {
        Preconditions.checkArgument(consumer != null, "Consumer 不能为 null");
        consumer.accept(damageContext);
        return this;
    }

    @Override
    public DamageSource build() {
        if (this.causingEntity != null && this.directEntity == null) {
            throw new IllegalArgumentException("如果设置了引发实体，则必须设置直接实体");
        }

        return CraftDamageSource.buildFromBukkit(this.damageType, this.causingEntity, this.directEntity, this.damageLocation, this.damageContext.build());
    }
}
