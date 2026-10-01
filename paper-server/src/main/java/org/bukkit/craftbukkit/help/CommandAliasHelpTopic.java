package org.bukkit.craftbukkit.help;

import com.google.common.base.Preconditions;
import org.bukkit.ChatColor;
import org.bukkit.command.CommandSender;
import org.bukkit.help.HelpMap;
import org.bukkit.help.HelpTopic;

public class CommandAliasHelpTopic extends HelpTopic {

    private final String aliasFor;
    private final HelpMap helpMap;

    public CommandAliasHelpTopic(String alias, String aliasFor, HelpMap helpMap) {
        this.aliasFor = aliasFor.startsWith("/") ? aliasFor : "/" + aliasFor;
        this.helpMap = helpMap;
        this.name = alias.startsWith("/") ? alias : "/" + alias;
        Preconditions.checkArgument(!this.name.equals(this.aliasFor), "命令 %s 不能成为自身的别名", this.name);
        this.shortText = ChatColor.YELLOW + "别名指向 " + ChatColor.WHITE + this.aliasFor;
    }

    @Override
    public String getFullText(CommandSender forWho) {
        Preconditions.checkArgument(forWho != null, "CommandServer forWho 不能为 null");
        StringBuilder sb = new StringBuilder(this.shortText);
        HelpTopic aliasForTopic = this.helpMap.getHelpTopic(this.aliasFor);
        if (aliasForTopic != null) {
            sb.append("\n");
            sb.append(aliasForTopic.getFullText(forWho));
        }
        return sb.toString();
    }

    @Override
    public boolean canSee(CommandSender commandSender) {
        Preconditions.checkArgument(commandSender != null, "CommandServer 不能为 null");
        if (this.amendedPermission == null) {
            HelpTopic aliasForTopic = this.helpMap.getHelpTopic(this.aliasFor);
            if (aliasForTopic != null) {
                return aliasForTopic.canSee(commandSender);
            } else {
                return false;
            }
        } else {
            return commandSender.hasPermission(this.amendedPermission);
        }
    }
}
