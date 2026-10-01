package io.papermc.paper.registry.data.dialog.input;

import com.google.common.base.Preconditions;
import java.util.List;
import net.kyori.adventure.text.Component;
import net.minecraft.commands.functions.StringTemplate;
import net.minecraft.server.dialog.body.PlainMessage;
import org.jspecify.annotations.Nullable;

import static io.papermc.paper.util.BoundChecker.requireRange;

public record SingleOptionDialogInputImpl(
    String key,
    int width,
    List<SingleOptionDialogInput.OptionEntry> entries,
    Component label,
    boolean labelVisible
) implements SingleOptionDialogInput {

    public SingleOptionDialogInputImpl {
        entries = List.copyOf(entries);
    }

    public record SingleOptionEntryImpl(String id, @Nullable Component display, boolean initial) implements OptionEntry {
    }

    public static final class BuilderImpl implements SingleOptionDialogInput.Builder {

        private final String key;
        private int width = PlainMessage.DEFAULT_WIDTH;
        private final List<OptionEntry> entries;
        private final Component label;
        private boolean labelVisible = true;

        public BuilderImpl(final String key, final List<OptionEntry> entries, final Component label) {
            Preconditions.checkArgument(StringTemplate.isValidVariableName(key), "key 必须是有效的输入名称");
            Preconditions.checkArgument(!entries.isEmpty(), "entries 不能为空");
            Preconditions.checkArgument(entries.stream().filter(OptionEntry::initial).count() <= 1, "初始时最多只能选中 1 个选项");

            this.key = key;
            this.entries = entries;
            this.label = label;
        }

        @Override
        public BuilderImpl width(final int width) {
            this.width = requireRange(width, "width", 1, 1024);
            return this;
        }

        @Override
        public BuilderImpl labelVisible(final boolean labelVisible) {
            this.labelVisible = labelVisible;
            return this;
        }

        @Override
        public SingleOptionDialogInput build() {
            return new SingleOptionDialogInputImpl(this.key, this.width, this.entries, this.label, this.labelVisible);
        }
    }
}
