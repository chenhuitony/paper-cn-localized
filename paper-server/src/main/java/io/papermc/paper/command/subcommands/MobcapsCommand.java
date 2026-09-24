package io.papermc.paper.command.subcommands;

import com.google.common.collect.ImmutableMap;
import io.papermc.paper.command.CommandUtil;
import io.papermc.paper.command.PaperSubcommand;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.function.ToIntFunction;
import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.ComponentLike;
import net.kyori.adventure.text.JoinConfiguration;
import net.kyori.adventure.text.TextComponent;
import net.kyori.adventure.text.format.NamedTextColor;
import net.kyori.adventure.text.format.TextColor;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.MobCategory;
import net.minecraft.world.level.NaturalSpawner;
import org.bukkit.Bukkit;
import org.bukkit.NamespacedKey;
import org.bukkit.World;
import org.bukkit.command.CommandSender;
import org.bukkit.craftbukkit.CraftWorld;
import org.bukkit.craftbukkit.entity.CraftPlayer;
import org.bukkit.entity.Player;
import org.checkerframework.checker.nullness.qual.NonNull;
import org.checkerframework.checker.nullness.qual.Nullable;
import org.checkerframework.framework.qual.DefaultQualifier;

@DefaultQualifier(NonNull.class)
public final class MobcapsCommand implements PaperSubcommand {
    static final Map<MobCategory, TextColor> MOB_CATEGORY_COLORS = ImmutableMap.<MobCategory, TextColor>builder()
        .put(MobCategory.MONSTER, NamedTextColor.RED)
        .put(MobCategory.CREATURE, NamedTextColor.GREEN)
        .put(MobCategory.AMBIENT, NamedTextColor.GRAY)
        .put(MobCategory.AXOLOTLS, TextColor.color(0x7324FF))
        .put(MobCategory.UNDERGROUND_WATER_CREATURE, TextColor.color(0x3541E6))
        .put(MobCategory.WATER_CREATURE, TextColor.color(0x006EFF))
        .put(MobCategory.WATER_AMBIENT, TextColor.color(0x00B3FF))
        .put(MobCategory.MISC, TextColor.color(0x636363))
        .build();

    @Override
    public boolean execute(final CommandSender sender, final String subCommand, final String[] args) {
        switch (subCommand) {
            case "mobcaps" -> this.printMobcaps(sender, args);
            case "playermobcaps" -> this.printPlayerMobcaps(sender, args);
        }
        return true;
    }

    @Override
    public List<String> tabComplete(final CommandSender sender, final String subCommand, final String[] args) {
        return switch (subCommand) {
            case "mobcaps" -> CommandUtil.getListMatchingLast(sender, args, this.suggestMobcaps(sender, args));
            case "playermobcaps" -> CommandUtil.getListMatchingLast(sender, args, this.suggestPlayerMobcaps(sender, args));
            default -> throw new IllegalArgumentException();
        };
    }

    private List<String> suggestMobcaps(final CommandSender sender, String[] args) {
        if (args.length == 1) {
            return CommandUtil.getWorldSuggestions(sender.getServer(), true);
        }

        return Collections.emptyList();
    }

    private List<String> suggestPlayerMobcaps(final CommandSender sender, final String[] args) {
        if (args.length == 1) {
            final List<String> list = new ArrayList<>();
            for (final Player player : Bukkit.getOnlinePlayers()) {
                if (!(sender instanceof Player senderPlayer) || senderPlayer.canSee(player)) {
                    list.add(player.getName());
                }
            }
            return list;
        }

        return Collections.emptyList();
    }

    private void printMobcaps(final CommandSender sender, final String[] args) {
        final List<World> worlds;
        if (args.length == 0) {
            if (sender instanceof Player player) {
                worlds = List.of(player.getWorld());
            } else {
                sender.sendMessage(Component.text("必须指定世界！示例：'/paper mobcaps minecraft:overworld'", NamedTextColor.RED));
                return;
            }
        } else if (args.length == 1) {
            final String input = args[0];
            if (input.equals("*")) {
                worlds = Bukkit.getServer().getWorlds();
            } else {
                final @Nullable NamespacedKey worldKey = NamespacedKey.fromString(input);
                final @Nullable World world = worldKey == null ? null : sender.getServer().getWorld(worldKey);
                if (world == null) {
                    sender.sendMessage(Component.text("'" + input + "' 不是有效世界！", NamedTextColor.RED));
                    return;
                } else {
                    worlds = List.of(world);
                }
            }
        } else {
            sender.sendMessage(Component.text("参数过多！", NamedTextColor.RED));
            return;
        }

        for (final World world : worlds) {
            final ServerLevel level = ((CraftWorld) world).getHandle();
            final NaturalSpawner.@Nullable SpawnState state = level.getChunkSource().getLastSpawnState();

            final int chunks;
            if (state == null) {
                chunks = 0;
            } else {
                chunks = state.getSpawnableChunkCount();
            }
            sender.sendMessage(Component.join(JoinConfiguration.noSeparators(),
                Component.text("世界生物上限："),
                Component.text(world.key().asString(), NamedTextColor.AQUA),
                Component.text("（" + chunks + " 个可生成区块）")
            ));

            sender.sendMessage(createMobcapsComponent(
                category -> {
                    if (state == null) {
                        return 0;
                    } else {
                        return state.getMobCategoryCounts().getOrDefault(category, 0);
                    }
                },
                category -> NaturalSpawner.globalLimitForCategory(level, category, chunks)
            ));
        }
    }

    private void printPlayerMobcaps(final CommandSender sender, final String[] args) {
        final @Nullable Player player;
        if (args.length == 0) {
            if (sender instanceof Player pl) {
                player = pl;
            } else {
                sender.sendMessage(Component.text("必须指定玩家！示例：'/paper playermobcount 玩家名'", NamedTextColor.RED));
                return;
            }
        } else if (args.length == 1) {
            final String input = args[0];
            player = Bukkit.getPlayerExact(input);
            if (player == null) {
                sender.sendMessage(Component.text("找不到名为 '" + input + "' 的玩家", NamedTextColor.RED));
                return;
            }
        } else {
            sender.sendMessage(Component.text("参数过多！", NamedTextColor.RED));
            return;
        }

        final ServerPlayer serverPlayer = ((CraftPlayer) player).getHandle();
        final ServerLevel level = serverPlayer.level();

        if (!level.paperConfig().entities.spawning.perPlayerMobSpawns) {
            sender.sendMessage(Component.text("在禁用按玩家生物生成的世界中，请使用 '/paper mobcaps'。", NamedTextColor.RED));
            return;
        }

        sender.sendMessage(Component.join(JoinConfiguration.noSeparators(), Component.text("玩家生物上限："), Component.text(player.getName(), NamedTextColor.GREEN)));
        sender.sendMessage(createMobcapsComponent(
            category -> level.getChunkSource().chunkMap.getMobCountNear(serverPlayer, category),
            category -> level.getWorld().getSpawnLimitUnsafe(org.bukkit.craftbukkit.util.CraftSpawnCategory.toBukkit(category))
        ));
    }

    private static Component createMobcapsComponent(final ToIntFunction<MobCategory> countGetter, final ToIntFunction<MobCategory> limitGetter) {
        return MOB_CATEGORY_COLORS.entrySet().stream()
            .map(entry -> {
                final MobCategory category = entry.getKey();
                final TextColor color = entry.getValue();

                final Component categoryHover = Component.join(JoinConfiguration.noSeparators(),
                    Component.text("该类别下的实体类型：", TextColor.color(0xE0E0E0)),
                    Component.text(category.getName(), color),
                    Component.text(':', NamedTextColor.GRAY),
                    Component.newline(),
                    Component.newline(),
                    BuiltInRegistries.ENTITY_TYPE.entrySet().stream()
                        .filter(it -> it.getValue().getCategory() == category)
                        .map(it -> Component.translatable(it.getValue().getDescriptionId()))
                        .collect(Component.toComponent(Component.text(", ", NamedTextColor.GRAY)))
                );

                final Component categoryComponent = Component.text()
                    .content("  " + category.getName())
                    .color(color)
                    .hoverEvent(categoryHover)
                    .build();

                final TextComponent.Builder builder = Component.text()
                    .append(
                        categoryComponent,
                        Component.text(": ", NamedTextColor.GRAY)
                    );
                final int limit = limitGetter.applyAsInt(category);
                if (limit != -1) {
                    builder.append(
                        Component.text(countGetter.applyAsInt(category)),
                        Component.text("/", NamedTextColor.GRAY),
                        Component.text(limit)
                    );
                } else {
                    builder.append(Component.text()
                        .append(
                            Component.text('n'),
                            Component.text("/", NamedTextColor.GRAY),
                            Component.text('a')
                        )
                        .hoverEvent(Component.text("该类别不会自然生成。"));
                }
                return builder;
            })
            .map(ComponentLike::asComponent)
            .collect(Component.toComponent(Component.newline()));
    }
}
