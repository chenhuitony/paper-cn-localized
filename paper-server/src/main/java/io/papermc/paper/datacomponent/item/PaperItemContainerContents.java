package io.papermc.paper.datacomponent.item;

import com.google.common.base.Preconditions;
import io.papermc.paper.util.MCUtil;
import it.unimi.dsi.fastutil.objects.ObjectArrayList;
import java.util.List;
import org.bukkit.craftbukkit.inventory.CraftItemStack;
import org.bukkit.craftbukkit.util.Handleable;
import org.bukkit.inventory.ItemStack;

public record PaperItemContainerContents(
    net.minecraft.world.item.component.ItemContainerContents impl
) implements ItemContainerContents, Handleable<net.minecraft.world.item.component.ItemContainerContents> {

    @Override
    public net.minecraft.world.item.component.ItemContainerContents getHandle() {
        return this.impl;
    }

    @Override
    public List<ItemStack> contents() {
        return MCUtil.transformUnmodifiable(this.impl.items, optional -> optional.map(CraftItemStack::asBukkitCopy).orElse(ItemStack.empty()));
    }

    static final class BuilderImpl implements ItemContainerContents.Builder {

        private final List<net.minecraft.world.item.ItemStack> items = new ObjectArrayList<>();

        @Override
        public ItemContainerContents.Builder add(final ItemStack item) {
            Preconditions.checkArgument(item != null, "item 不能为 null");
            Preconditions.checkArgument(
                this.items.size() + 1 <= net.minecraft.world.item.component.ItemContainerContents.MAX_SIZE,
                "物品数量不能超过 %s，当前为 %s",
                net.minecraft.world.item.component.ItemContainerContents.MAX_SIZE,
                this.items.size() + 1
            );
            this.items.add(CraftItemStack.asNMSCopy(item));
            return this;
        }

        @Override
        public ItemContainerContents.Builder addAll(final List<ItemStack> items) {
            Preconditions.checkArgument(
                this.items.size() + items.size() <= net.minecraft.world.item.component.ItemContainerContents.MAX_SIZE,
                "物品数量不能超过 %s，当前为 %s",
                net.minecraft.world.item.component.ItemContainerContents.MAX_SIZE,
                this.items.size() + items.size()
            );
            MCUtil.addAndConvert(this.items, items, item -> {
                Preconditions.checkArgument(item != null, "不能传入 null 物品！");
                return CraftItemStack.asNMSCopy(item);
            });
            return this;
        }

        @Override
        public ItemContainerContents build() {
            if (this.items.isEmpty()) {
                return new PaperItemContainerContents(net.minecraft.world.item.component.ItemContainerContents.EMPTY);
            }
            return new PaperItemContainerContents(net.minecraft.world.item.component.ItemContainerContents.fromItems(this.items));
        }
    }
}
