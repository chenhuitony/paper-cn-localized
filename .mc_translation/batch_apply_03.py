#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply translations to all shard03 files. Translation map: original -> translated."""
import sys, os, json, subprocess

BASE = r"E:\编程\项目\Paper-main\paper-server\src\minecraft\java"
LIST = r"E:\编程\项目\Paper-main\.mc_translation\shard_03_world_item_server_adv.txt"
SCRIPT = r"E:\编程\项目\Paper-main\.mc_translation\file_translator.py"

# Global translation dictionary: English original -> Chinese translation
# Only includes strings that should be translated (LOGGER, exceptions, command output, chat, crash reports, GUI)
# Skips: thread names, debug format keys, profiler labels, AsyncCatcher ops, date formats, command templates,
#        resource keys, Content-Type headers, brand identifiers, suppress-warnings reasons
T = {
    # === Advancement.java ===
    "Advancement criteria cannot be empty": "进度标准不能为空",

    # === AdvancementProgress.java ===
    # "yyyy-MM-dd HH:mm:ss Z" SKIP (date format)
    # ", requirements=" SKIP (toString debug)

    # === AdvancementRequirements.java ===
    "Requirement entry cannot be empty": "需求条目不能为空",
    "Advancement completion requirements did not exactly match specified criteria. Missing: ": "进度完成需求与指定的标准不完全匹配。缺少：",
    ". Unknown: ": "。未知：",

    # === AdvancementTree.java ===
    "Forgot about advancement {}": "忘记了进度 {}",
    "Told to remove advancement {} but I don't know what that is": "被告知移除进度 {}，但我不知道那是什么",
    "Couldn't load advancements: {}": "无法加载进度：{}",

    # === TreeNodePosition.java ===
    "Can't position an invisible advancement!": "无法定位不可见的进度！",
    "Can't position children of an invisible root!": "无法定位不可见根进度的子项！",

    # === MinMaxBounds.java ===
    "Range must be within ": "范围必须在 ",
    ", but was ": " 之间，但实际是 ",
    "Swapped bounds in range: ": "范围中边界值颠倒：",
    " is higher than ": " 高于 ",

    # === EnterBlockTrigger.java / SlideDownBlockTrigger.java ===
    " has no property ":  " 没有属性 ",

    # === Bootstrap.java ===
    # "System.out setup" SKIP (SuppressForbidden reason)
    "Unable to load registries": "无法加载注册表",
    "Failed loading EntityTypes": "加载实体类型失败",
    "Not bootstrapped (called from ": "尚未初始化引导（调用自 ",
    "Not bootstrapped (failed to resolve location)": "尚未初始化引导（无法解析位置）",
    "Missing translations: {}": "缺少翻译：{}",

    # === ChainedJsonException.java ===
    "File not found": "文件未找到",
    "(Unknown file)": "(未知文件)",
    "(Unknown file) ": "(未知文件) ",

    # === Eula.java ===
    "Failed to load {}": "加载 {} 失败",
    "By changing the setting below to TRUE you are indicating your agreement to our EULA (": "将下面的设置改为TRUE即表示您同意我们的最终用户许可协议（",
    "Failed to save {}": "保存 {} 失败",

    # === Main.java ===
    # "System.out needed before bootstrap" SKIP
    # Thread names SKIP: "CrashReport preload thread", "DataConverter MCTypeRegistry init thread", "DataFixers init thread"
    "World upgrade and region file recreation are not yet implemented in Paper 26.1.": "世界升级和区域文件重建在 Paper 26.1 中尚未实现。",
    "Initialized '{}' and '{}'": "已初始化 '{}' 和 '{}'",
    "You have used the Paper command line EULA agreement flag.": "您使用了 Paper 命令行 EULA 同意标志。",
    "By using this setting you are indicating your agreement to Mojang's EULA (https://aka.ms/MinecraftEULA).": "使用此设置即表示您同意 Mojang 的 EULA（https://aka.ms/MinecraftEULA）。",
    "If you do not agree to the above EULA please stop your server and remove this flag immediately.": "如果您不同意上述 EULA，请立即停止服务端并移除此标志。",
    "You need to agree to the EULA in order to run the server. Go to eula.txt for more info.": "您需要同意 EULA 才能运行服务端。请查看 eula.txt 了解更多信息。",
    "You are using a headless JRE distribution.": "您正在使用 headless JRE 发行版。",
    "This distribution is missing certain graphic libraries that the Minecraft server needs to function.": "此发行版缺少 Minecraft 服务端运行所需的某些图形库。",
    "For instructions on how to install the non-headless JRE, see https://docs.papermc.io/misc/java-install": "有关如何安装非 headless JRE 的说明，请参见 https://docs.papermc.io/misc/java-install",
    "Failed to load world data. World files may be corrupted. Shutting down.": "加载世界数据失败。世界文件可能已损坏。正在关闭。",
    "This world must be opened in an older version (like 1.6.4) to be safely converted": "此世界必须在旧版本（如 1.6.4）中打开才能安全转换",
    "This world was created by an incompatible version.": "此世界由不兼容的版本创建。",
    "Safe mode active, only vanilla datapack will be loaded": "安全模式已启用，将仅加载原版数据包",
    "Failed to migrate world storage for ": "迁移世界存储失败：",
    "No existing world data, creating new world": "没有现有世界数据，正在创建新世界",
    "Failed to load datapacks, can't proceed with server load. You can either fix your datapacks or reset to vanilla with --safeMode": "加载数据包失败，无法继续加载服务端。您可以修复数据包或使用 --safeMode 重置为原版",
    "Failed to start the minecraft server": "启动 Minecraft 服务端失败",

    # === MinecraftServer.java ===
    "Demo World": "演示世界",
    "Anonymous Player": "匿名玩家",
    # "Server thread" SKIP (thread name constant)
    # "Server thread" SKIP (thread name)
    "Uncaught exception in server thread": "服务端线程中未捕获的异常",
    "Performing emergency save...": "正在执行紧急保存...",
    "Saving all players...": "正在保存所有玩家...",
    "Saved all players": "已保存所有玩家",
    "Saving all worlds...": "正在保存所有世界...",
    "Saving chunks in world '": "正在保存世界中的区块 '",
    "Saved chunks in world '": "已保存世界中的区块 '",
    "Saved all worlds": "已保存所有世界",
    "Performed emergency save": "已执行紧急保存",
    "Missing Overworld dimension data": "缺少主世界维度数据",
    # "Server Tick" SKIP (Tracy frame name)
    "Failed to stop JFR profiling": "停止 JFR 分析失败",
    "Exception initializing level": "初始化世界时异常",
    "Cannot set spawn point for ": "无法设置出生点：",
    " to be in another world (": " 位于另一个世界（",
    "Saving chunks for level '{}'/{}": "正在保存世界 '{}'/{} 的区块",
    "ThreadedAnvilChunkStorage ({}): All chunks are saved": "ThreadedAnvilChunkStorage（{}）：所有区块已保存",
    "ThreadedAnvilChunkStorage: All dimensions are saved": "ThreadedAnvilChunkStorage：所有维度已保存",
    # "Server stopped" SKIP (TraceUtil dump label)
    "Stopping server": "正在停止服务端",
    "Saving players": "正在保存玩家",
    "Saving worlds": "正在保存世界",
    "Failed to unlock level {}": "解锁世界 {} 失败",
    "Saving usercache.json": "正在保存 usercache.json",
    "Waiting for all RegionFile I/O tasks to complete...": "正在等待所有 RegionFile I/O 任务完成...",
    "All RegionFile I/O tasks to complete": "所有 RegionFile I/O 任务已完成",
    # "Server stopped" SKIP
    "Error while shutting down": "关闭时出错",
    # "waiting for tick or tasks" SKIP (LockSupport park name)
    "Failed to initialize server": "初始化服务端失败",
    "Running delayed init tasks": "正在运行延迟初始化任务",
    "Done ({})! For help, type \"help\"": "完成（{}）！如需帮助，请输入 \"help\"",
    "This is the first time you're starting this server.": "这是您第一次启动此服务端。",
    "It's recommended you read our 'Getting Started' documentation for guidance.": "建议您阅读我们的'入门指南'文档以获取指导。",
    "View this and more helpful information here: https://docs.papermc.io/paper/next-steps": "查看此内容及更多有用信息：https://docs.papermc.io/paper/next-steps",
    "Encountered an unexpected exception": "遇到意外异常",
    "This crash report has been saved to: {}": "此崩溃报告已保存至：{}",
    "We were unable to save this crash report to disk.": "我们无法将此崩溃报告保存到磁盘。",
    "Exception stopping the server": "停止服务端时异常",
    "Wrapped in": "包装于",
    "Wrapping exception": "包装异常",
    "Exception in server tick loop": "服务端 tick 循环中异常",
    # "executing tasks" SKIP (park name)
    # "waiting for tasks" SKIP (park name)
    "Invalid world icon size [": "无效的世界图标尺寸 [",
    "], but expected [64, 64]": "]，但预期为 [64, 64]",
    "Couldn't load server icon": "无法加载服务端图标",
    "Server empty for {} seconds, pausing": "服务端已空 {} 秒，正在暂停",
    "Chunk system crash propagated to tick()": "区块系统崩溃已传播到 tick()",
    "Autosave started": "自动保存已开始",
    "Autosave finished": "自动保存已完成",
    "Exception ticking world": "世界 tick 时异常",
    # "server gui refresh" SKIP (profiler)
    # "send chunks" SKIP (profiler)
    "Server Running": "服务端运行中",
    "Player Count": "玩家数量",
    "Active Data Packs": "已启用数据包",
    "Available Data Packs": "可用数据包",
    "Enabled Feature Flags": "已启用特性标志",
    "World Generation": "世界生成",
    "World Seed": "世界种子",
    "Suppressed Exceptions": "已抑制的异常",
    "Server Id": "服务端 ID",
    "Generating keypair": "正在生成密钥对",
    "Failed to generate key pair": "生成密钥对失败",
    "Server already shutting down": "服务端已在关闭中",
    "Missing data pack {}": "缺少数据包 {}",
    "Found new data pack {}, loading it automatically": "发现新数据包 {}，正在自动加载",
    "Found new data pack {}, but can't load it due to missing features {}": "发现新数据包 {}，但因缺少特性 {} 无法加载",
    "Pack {} requires features {} that are not enabled for this world, disabling pack.": "数据包 {} 需要此世界未启用的特性 {}，正在禁用该数据包。",
    "No datapacks selected, forcing vanilla": "未选择数据包，强制使用原版",
    "Tried to force '": "尝试强制 '",
    "', but it was already enabled": "'，但它已被启用",
    "Found feature pack ('{}') for requested feature, forcing to enabled": "为请求的特性找到特性数据包（'{}'），正在强制启用",
    "Called before server init": "在服务端初始化前调用",
    "Use ServerLevel.getWeatherData() instead": "请改用 ServerLevel.getWeatherData()",
    "Failed to save debug report": "保存调试报告失败",
    # Debug output keys SKIP: "pending_tasks: %d\n", "average_tick_time: %f\n", "tick_times: %s\n", "queue: %s\n"
    "Failed to list native modules": "列出本地模块失败",
    # "Async Chat Thread - #%d" SKIP (thread name)
    "Received custom click action {} with payload {}": "收到自定义点击操作 {}，载荷为 {}",
    "Use ServerLevel.getScheduledEvents() instead": "请改用 ServerLevel.getScheduledEvents()",
    "Use ServerLevel.getGameRules() instead": "请改用 ServerLevel.getGameRules()",
    "Not storing chunk IO report due to low space on drive {}": "由于驱动器 {} 空间不足，不存储区块 IO 报告",
    "Chunk Info": "区块信息",
    "Saved details to {}": "已将详情保存至 {}",
    "Failed to store chunk IO exception": "存储区块 IO 异常失败",
    "Failed to load chunk {},{}": "加载区块 {},{} 失败",
    "Chunk load failure": "区块加载失败",
    "Failed to save chunk {},{}": "保存区块 {},{} 失败",
    "Chunk save failure": "区块保存失败",
    "Low disk space! Might not be able to save the world.": "磁盘空间不足！可能无法保存世界。",

    # === PlayerAdvancements.java ===
    "Couldn't access player advancements in {}": "无法访问 {} 中的玩家进度",
    "Couldn't parse player advancements in {}": "无法解析 {} 中的玩家进度",
    "Couldn't save player advancements to {}": "无法将玩家进度保存到 {}",
    "Ignored advancement '{}' in progress file {} - it doesn't exist anymore?": "在进度文件 {} 中忽略了进度 '{}'——它已不存在？",

    # === ReloadableServerRegistries.java ===
    "Found loot table element validation problem in {}: {}": "在 {} 中发现战利品表元素验证问题：{}",

    # === ServerAdvancementManager.java ===
    "Loaded {} advancements": "已加载 {} 个进度",
    "Found validation problems in advancement {}: \n{}": "在进度 {} 中发现验证问题：\n{}",

    # === ServerFunctionLibrary.java ===
    "Failed to load function {}": "加载函数 {} 失败",

    # === ServerFunctionManager.java ===
    "Failed to execute function {}": "执行函数 {} 失败",

    # === SuppressedExceptionCollector.java ===
    # "ms ago)" SKIP (toString fragment)

    # === ChaseClient.java ===
    "Remote control client was asked to start, but it is already running. Will ignore.": "远程控制客户端被要求启动，但它已在运行。将忽略。",
    "Connecting to remote control server {}": "正在连接远程控制服务端 {}",
    "Connected to remote control server! Will continuously execute the command broadcasted by that server.": "已连接到远程控制服务端！将持续执行该服务端广播的命令。",
    "Lost connection to remote control server {}. Will retry in {}s.": "与远程控制服务端 {} 的连接断开。将在 {} 秒后重试。",
    "Failed to connect to remote control server {}. Will retry in {}s.": "连接远程控制服务端 {} 失败。将在 {} 秒后重试。",
    "Unknown message type '{}'": "未知消息类型 '{}'",
    "Could not parse message '{}', ignoring": "无法解析消息 '{}'，已忽略",
    # "execute in %s run tp @s %.3f %.3f %.3f %.3f %.3f" SKIP (command template)

    # === ChaseServer.java ===
    "Remote control server was asked to start, but it is already running. Will ignore.": "远程控制服务端被要求启动，但它已在运行。将忽略。",
    "Remote control client socket got an IO exception and will be closed": "远程控制客户端套接字发生 IO 异常，将被关闭",
    "Remote control server is listening for connections on port {}": "远程控制服务端正在端口 {} 上监听连接",
    "Remote control server received client connection on port {}": "远程控制服务端在端口 {} 收到客户端连接",
    "Remote control server closed by interrupt": "远程控制服务端被中断关闭",
    "Remote control server closed because of an IO exception": "远程控制服务端因 IO 异常而关闭",
    "Remote control server is now stopped": "远程控制服务端现已停止",

    # === ChaseCommand.java ===
    "You have now stopped chasing": "您已停止追踪",
    "You are no longer being chased": "您不再被追踪",
    "Chase server is already running. Stop it using /chase stop": "追踪服务端已在运行。使用 /chase stop 停止它",
    "You are already chasing someone. Stop it using /chase stop": "您已在追踪某人。使用 /chase stop 停止",
    "Chase server is now running on port ": "追踪服务端现已在端口 ",
    ". Clients can follow you using /chase follow <ip> <port>": "。客户端可使用 /chase follow <ip> <port> 跟随您",
    "Failed to start chase server": "启动追踪服务端失败",
    "Failed to start chase server on port ": "在端口 ",
    "You are now chasing ": "您现在正在追踪 ",
    ". If that server does '/chase lead' then you will automatically go to the same position. Use '/chase stop' to stop chasing.": "。如果该服务端执行 '/chase lead'，您将自动前往相同位置。使用 '/chase stop' 停止追踪。",

    # === DataPackCommand.java ===
    "Failed to create pack at {}": "在 {} 创建数据包失败",

    # === DebugCommand.java ===
    "Tracing failed": "追踪失败",

    # === DebugConfigCommand.java ===
    "Switched player ": "已切换玩家 ",
    ") to config mode": ") 到配置模式",
    "Can't find player to unconfig": "找不到要退出配置的玩家",
    "Can't find player to talk to": "找不到要对话的玩家",

    # === DebugPathCommand.java ===
    "Source is not a mob": "来源不是生物",
    "Path not found": "未找到路径",
    "Target not reached": "未到达目标",
    "Made path": "已创建路径",

    # === FetchProfileCommand.java ===
    # "give @s minecraft:player_head[profile=" SKIP (command template)
    # "summon minecraft:mannequin ~ ~ ~ {profile:" SKIP (command template)

    # === LocateCommand.java ===
    "Locating element {} took {} ms": "定位元素 {} 耗时 {} 毫秒",

    # === PerfCommand.java ===
    "Failed to create report name": "创建报告名称失败",
    "Failed to delete temporary profiling file {}": "删除临时分析文件 {} 失败",

    # === RaidCommand.java ===
    "Sorry, the max raid omen level you can set is ": "抱歉，您可设置的最大不祥之兆等级为 ",
    "Changed village's raid omen level from ": "已将村庄的不祥之兆等级从 ",
    "No raid found here": "此处未找到袭击",
    "Spawned a raid captain": "已生成袭击队长",
    "Pillager failed to spawn": "掠夺者生成失败",
    "Raid already started close by": "附近已开始袭击",
    "Created a raid in your local village": "已在您的村庄创建袭击",
    "Failed to create a raid in your local village": "在您的村庄创建袭击失败",
    "Stopped raid": "已停止袭击",
    "No raid here": "此处没有袭击",
    "Found a started raid! ": "发现已开始的袭击！",
    "Num groups spawned: ": "已生成组数：",
    " Raid omen level: ": " 不祥之兆等级：",
    " Num mobs: ": " 生物数量：",
    " Raid health: ": " 袭击血量：",
    "Found no started raids": "未找到已开始的袭击",

    # === ReloadCommand.java ===
    "Failed to execute reload": "执行重载失败",

    # === SpawnArmorTrimsCommand.java ===
    # "Invalid pattern" SKIP (Component.translatableEscape = translation key)
    "Armorstands with trimmed armor spawned around you": "已在您周围生成穿着镶饰盔甲的盔甲架",

    # === WaypointCommand.java ===
    # " run tp @s " SKIP (command template fragment)

    # === DedicatedPlayerList.java ===
    "Failed to save ip banlist: ": "保存 IP 封禁列表失败：",
    "Failed to save user banlist: ": "保存玩家封禁列表失败：",
    "Failed to load ip banlist: ": "加载 IP 封禁列表失败：",
    "Failed to load user banlist: ": "加载玩家封禁列表失败：",
    "Failed to load operators list: ": "加载管理员列表失败：",
    "Failed to save operators list: ": "保存管理员列表失败：",
    "Failed to load white-list: ": "加载白名单失败：",
    "Failed to save white-list: ": "保存白名单失败：",

    # === DedicatedServer.java ===
    "Code of Conduct folder does not exist: ": "行为准则文件夹不存在：",
    "Failed to read Code of Conduct file \\\"": "读取行为准则文件 \\\"",
    "Failed to read Code of Conduct file ": "读取行为准则文件 ",
    "Failed to read Code of Conduct folder": "读取行为准则文件夹失败",
    # "Server console handler" SKIP (thread name)
    "Starting minecraft server version {}": "正在启动 Minecraft 服务端，版本 {}",
    "To start the server with more ram, launch it as \"java -Xmx1024M -Xms1024M -jar minecraft_server.jar\"": "要以更多内存启动服务端，请使用 \"java -Xmx1024M -Xms1024M -jar minecraft_server.jar\" 命令启动",
    "YOU ARE RUNNING THIS SERVER AS AN ADMINISTRATIVE OR ROOT USER. THIS IS NOT ADVISED.": "您正在以管理员或 root 用户身份运行此服务端。不建议这样做。",
    "YOU ARE OPENING YOURSELF UP TO POTENTIAL RISKS WHEN DOING THIS.": "这样做会使您面临潜在风险。",
    "FOR MORE INFORMATION, SEE https://madelinemiller.dev/blog/root-minecraft-server/": "更多信息请参见 https://madelinemiller.dev/blog/root-minecraft-server/",
    "Loading properties": "正在加载属性配置",
    "Default game type: {}": "默认游戏模式：{}",
    "**** INVALID CONFIGURATION!": "**** 无效的配置！",
    "You are trying to use a Unix domain socket but you're not on a supported OS.": "您尝试使用 Unix 域套接字，但您的操作系统不受支持。",
    "Unix domain sockets require IPs to be forwarded from a proxy.": "Unix 域套接字需要从代理转发 IP。",
    "Starting Minecraft server on {}:{}": "正在启动 Minecraft 服务端于 {}:{}",
    "**** FAILED TO BIND TO PORT!": "**** 绑定端口失败！",
    "The exception was: {}": "异常为：{}",
    "Perhaps a server is already running on that port?": "可能该端口上已有服务端在运行？",
    "Failed to bind to port": "绑定端口失败",
    "**** SERVER IS RUNNING IN OFFLINE/INSECURE MODE!": "**** 服务端正以离线/非安全模式运行！",
    "The server will make no attempt to authenticate usernames. Beware.": "服务端不会尝试验证用户名。请注意。",
    "Whilst this makes it possible to use {}, unless access to your server is properly restricted, it also opens up the ability for hackers to connect with any username they choose.": "虽然这使得使用 {} 成为可能，但除非正确限制对您服务端的访问，否则黑客也可以使用任意用户名连接。",
    "Please see {} for further information.": "请参见 {} 获取更多信息。",
    "While this makes the game possible to play without internet access, it also opens up the ability for hackers to connect with any username they choose.": "虽然这使得无网络也能游戏，但黑客也可以使用任意用户名连接。",
    "To change this, set \"online-mode\" to \"true\" in the server.properties file.": "要更改此设置，请在 server.properties 文件中将 \"online-mode\" 设为 \"true\"。",
    "Preparing level \"{}\"": "正在准备世界 \"{}\"",
    "Done preparing level \"{}\" ({})": "世界 \"{}\" 准备完成（{}）",
    "Starting GS4 status listener": "正在启动 GS4 状态监听器",
    "Starting remote control listener": "正在启动远程控制监听器",
    # "Server Watchdog" SKIP (thread name)
    "JMX monitoring enabled": "JMX 监控已启用",
    "Is Modded": "是否安装模组",
    "Dedicated Server": "专用服务端",
    "Interrupted while stopping the management server": "停止管理服务端时被中断",
    # "paper debug chunks --async" SKIP (command string comparison)
    "Scheduling async debug chunks": "正在调度异步调试区块",
    "Async debug chunks executing": "异步调试区块正在执行",
    "Writing chunk information dump to ": "正在将区块信息转储写入 ",
    "Successfully written chunk information!": "区块信息写入成功！",
    "Failed to dump chunk information to file ": "将区块信息转储到文件 ",
    "Failed to dump chunk information, see console": "转储区块信息失败，请查看控制台",
    # "Async debug thread #" SKIP (thread name)
    "Encountered a problem while converting the user banlist, retrying in a few seconds": "转换玩家封禁列表时遇到问题，将在几秒后重试",
    "Encountered a problem while converting the ip banlist, retrying in a few seconds": "转换 IP 封禁列表时遇到问题，将在几秒后重试",
    "Encountered a problem while converting the op list, retrying in a few seconds": "转换管理员列表时遇到问题，将在几秒后重试",
    "Encountered a problem while converting the whitelist, retrying in a few seconds": "转换白名单时遇到问题，将在几秒后重试",
    "Encountered a problem while converting the player save files, retrying in a few seconds": "转换玩家存档文件时遇到问题，将在几秒后重试",
    # " on Bukkit " SKIP (modded status indicator)
    "Not supported - remote source required.": "不支持——需要远程源。",
    "Failed to parse bug link {}": "解析错误链接 {} 失败",

    # === DedicatedServerProperties.java ===
    "A Minecraft Server": "一个 Minecraft 服务端",
    "Failed to parse resource pack prompt '{}': {}": "解析资源包提示 '{}' 失败：{}",
    "Failed to parse resource pack prompt '{}'": "解析资源包提示 '{}' 失败",
    "resource-pack-hash is deprecated and found along side resource-pack-sha1. resource-pack-hash will be ignored.": "resource-pack-hash 已弃用，且与 resource-pack-sha1 同时存在。resource-pack-hash 将被忽略。",
    "resource-pack-hash is deprecated. Please use resource-pack-sha1 instead.": "resource-pack-hash 已弃用。请改用 resource-pack-sha1。",
    "You specified a resource pack without providing a sha1 hash. Pack will be updated on the client only if you change the name of the pack.": "您指定了资源包但未提供 sha1 哈希。仅当更改资源包名称时，客户端才会更新资源包。",
    "Invalid sha1 for resource-pack-sha1": "resource-pack-sha1 的 sha1 无效",
    "resource-pack-id missing, using default of {}": "缺少 resource-pack-id，使用默认值 {}",
    "Failed to parse '{}' into UUID": "将 '{}' 解析为 UUID 失败",
    "Invalid datapack contents: can't find default preset": "数据包内容无效：找不到默认预设",
    "Failed to parse level-type {}, defaulting to {}": "解析 level-type {} 失败，默认为 {}",

    # === ServerWatchdog.java ===
    "A single server tick took {} seconds (should be max {})": "单个服务端 tick 耗时 {} 秒（最大应为 {}）",
    "Considering it to be crashed, server will forcibly shutdown.": "判定为已崩溃，服务端将强制关闭。",
    "Watching Server": "监视服务端",
    "Performance stats": "性能统计",
    "Overworld random tick rate": "主世界随机 tick 速率",
    "Level stats": "世界统计",
    "Crash report:\n": "崩溃报告：\n",
    "This crash report has been saved to: {}": "此崩溃报告已保存至：{}",
    "We were unable to save this crash report to disk.": "我们无法将此崩溃报告保存到磁盘。",
    "Watchdog (": "看门狗（",
    "Thread Dump": "线程转储",

    # === Settings.java ===
    "Failed to load properties as UTF-8 from file {}, trying ISO_8859_1": "以 UTF-8 从文件 {} 加载属性失败，尝试 ISO_8859_1",
    "Failed to load properties from file: {}": "从文件 {} 加载属性失败",
    "Can not write to file {}, skipping.": "无法写入文件 {}，已跳过。",
    "Minecraft server properties": "Minecraft 服务端属性",
    "Failed to store properties to file: {}": "将属性存储到文件 {} 失败",
    "Could not load invalidly configured property '": "无法加载配置无效的属性 '",

    # === CommonDialogData.java ===
    "Dialogs that pause the game must use after_action values that unpause it after user action!": "暂停游戏的对话框必须使用在用户操作后取消暂停的 after_action 值！",

    # === ParsedTemplate.java ===
    " is not a valid input name": " 不是有效的输入名称",
    "Failed to parse template ": "解析模板 ",

    # === NumberRangeInput.java ===
    "Initial value ": "初始值 ",
    " is outside of range [": " 超出范围 [",

    # === SingleOptionInput.java ===
    "Multiple initial values": "多个初始值",

    # === TextInput.java ===
    "Default text length exceeds allowed size": "默认文本长度超出允许大小",

    # === MinecraftServerGui.java ===
    "Minecraft server": "Minecraft 服务端",
    "Minecraft server - shutting down!": "Minecraft 服务端——正在关闭！",
    "Couldn't build server GUI": "无法构建服务端 GUI",
    "Log and chat": "日志和聊天",
    "Server log monitor": "服务端日志监视器",
    "If you need help setting up your server you can visit:": "如果您需要帮助设置服务端，可以访问：",
    "Unable to find a default browser. Please manually visit the website: ": "找不到默认浏览器。请手动访问网站：",
    "This platform does not support the BROWSE action. Please manually visit the website: ": "此平台不支持 BROWSE 操作。请手动访问网站：",
    "This action has been denied by the security manager. Please manually visit the website: ": "此操作已被安全管理器拒绝。请手动访问网站：",

    # === StatsComponent.java ===
    "Memory use: ": "内存使用：",
    " mb (": " MB（",
    "% free)": "% 空闲）",
    "Avg tick: ": "平均 tick：",
    "TPS from last 1m, 5m, 15m: ": "最近 1 分钟、5 分钟、15 分钟的 TPS：",

    # === Connection.java (jsonrpc) ===
    "RPC method ": "RPC 方法 ",
    " timed out waiting for response": " 等待响应超时",
    "Management connection opened for {}": "管理连接已打开：{}",
    "Management connection closed for {}": "管理连接已关闭：{}",
    "Method cannot be dispatched pre server initialization: ": "方法不能在服务端初始化前分发：",
    "Invalid request id - only String, Number and NULL supported": "无效的请求 ID——仅支持字符串、数字和 NULL",
    "Received respose {} with id {} we did not request": "收到未请求的响应 {}，ID 为 {}",
    "Error while handling rpc request": "处理 RPC 请求时出错",
    "Unknown error handling request - check server logs for stack trace": "处理请求时出现未知错误——请查看服务端日志获取堆栈跟踪",
    "Invalid parameter invocation {}: {}, {}": "无效参数调用 {}：{}，{}",
    "Failed to encode json rpc response {}: {}": "编码 JSON RPC 响应 {} 失败：{}",
    "Error while dispatching rpc method {}": "分发 RPC 方法 {} 时出错",
    "Failed to parse method value: ": "解析方法值失败：",
    "Method not found: ": "未找到方法：",
    "Received unknown response (id: {}): {}": "收到未知响应（ID：{}）：{}",
    "Received error (id: {}): {}": "收到错误（ID：{}）：{}",

    # === IncomingRpcMethod.java ===
    "No response defined": "未定义响应",
    "No param schema defined": "未定义参数模式",
    "No method defined": "未定义方法",
    "Method defined as having parameters without describing them": "方法定义为有参数但未描述参数",
    "Params passed by-name, but expected param [%s] does not exist": "参数按名称传递，但预期的参数 [%s] 不存在",
    "Expected exactly one element in the params array": "参数数组中应恰好有一个元素",
    "No result codec defined": "未定义结果编解码器",
    "Expected params as array or named": "参数应为数组或命名参数",
    "Parameterless method unexpectedly has parameter description": "无参数方法意外地有参数描述",
    "Expected no params, or an empty array": "应为无参数或空数组",

    # === IncomingRpcMethods.java (descriptions) ===
    "Get the allowlist": "获取白名单",
    "Set the allowlist": "设置白名单",
    "Add players to allowlist": "将玩家添加到白名单",
    "Remove players from allowlist": "从白名单移除玩家",
    "Clear all players in allowlist": "清除白名单中的所有玩家",
    "Get the ban list": "获取封禁列表",
    "Set the banlist": "设置封禁列表",
    "Add players to ban list": "将玩家添加到封禁列表",
    "Remove players from ban list": "从封禁列表移除玩家",
    "Clear all players in ban list": "清除封禁列表中的所有玩家",
    "Get the ip ban list": "获取 IP 封禁列表",
    "Set the ip banlist": "设置 IP 封禁列表",
    "Add ip to ban list": "将 IP 添加到封禁列表",
    "Remove ip from ban list": "从封禁列表移除 IP",
    "Clear all ips in ban list": "清除封禁列表中的所有 IP",
    "Get all connected players": "获取所有已连接的玩家",
    "Kick players": "踢出玩家",
    "Get all oped players": "获取所有管理员玩家",
    "Set all oped players": "设置所有管理员玩家",
    "Op players": "给予玩家管理员权限",
    "Deop players": "移除玩家管理员权限",
    "Deop all players": "移除所有玩家的管理员权限",
    "Get server status": "获取服务端状态",
    "Save server state": "保存服务端状态",
    "Stop server": "停止服务端",
    "Send a system message": "发送系统消息",
    "Get whether automatic world saving is enabled on the server": "获取服务端是否启用自动世界保存",
    "Enable or disable automatic world saving on the server": "启用或禁用服务端自动世界保存",
    "Get the current difficulty level of the server": "获取服务端当前难度等级",
    "Set the difficulty level of the server": "设置服务端难度等级",
    "Get whether allowlist enforcement is enabled (kicks players immediately when removed from allowlist)": "获取是否启用白名单强制执行（从白名单移除时立即踢出玩家）",
    "Enable or disable allowlist enforcement (when enabled, players are kicked immediately upon removal from allowlist)": "启用或禁用白名单强制执行（启用后，玩家从白名单移除时立即被踢出）",
    "Get whether the allowlist is enabled on the server": "获取服务端是否启用白名单",
    "Enable or disable the allowlist on the server (controls whether only allowlisted players can join)": "启用或禁用服务端白名单（控制是否仅白名单玩家可加入）",
    "Get the maximum number of players allowed to connect to the server": "获取允许连接到服务端的最大玩家数",
    "Set the maximum number of players allowed to connect to the server": "设置允许连接到服务端的最大玩家数",
    "Get the number of seconds before the game is automatically paused when no players are online": "获取无玩家在线时自动暂停游戏的等待秒数",
    "Set the number of seconds before the game is automatically paused when no players are online": "设置无玩家在线时自动暂停游戏的等待秒数",
    "Get the number of seconds before idle players are automatically kicked from the server": "获取闲置玩家自动被踢出服务端的等待秒数",
    "Set the number of seconds before idle players are automatically kicked from the server": "设置闲置玩家自动被踢出服务端的等待秒数",
    "Get whether flight is allowed for players in Survival mode": "获取生存模式下是否允许玩家飞行",
    "Allow or disallow flight for players in Survival mode": "允许或禁止生存模式玩家飞行",
    "Get the server's message of the day displayed to players": "获取显示给玩家的服务端 MOTD",
    "Set the server's message of the day displayed to players": "设置显示给玩家的服务端 MOTD",
    "Get the spawn protection radius in blocks (only operators can edit within this area)": "获取出生点保护半径（方块）（仅管理员可在此区域内编辑）",
    "Set the spawn protection radius in blocks (only operators can edit within this area)": "设置出生点保护半径（方块）（仅管理员可在此区域内编辑）",
    "Get whether players are forced to use the server's default game mode": "获取是否强制玩家使用服务端默认游戏模式",
    "Enable or disable forcing players to use the server's default game mode": "启用或禁用强制玩家使用服务端默认游戏模式",
    "Get the server's default game mode": "获取服务端默认游戏模式",
    "Set the server's default game mode": "设置服务端默认游戏模式",
    "Get the server's view distance in chunks": "获取服务端视距（区块）",
    "Set the server's view distance in chunks": "设置服务端视距（区块）",
    "Get the server's simulation distance in chunks": "获取服务端模拟距离（区块）",
    "Set the server's simulation distance in chunks": "设置服务端模拟距离（区块）",
    "Get whether the server accepts player transfers from other servers": "获取服务端是否接受其他服务端的玩家转移",
    "Enable or disable accepting player transfers from other servers": "启用或禁用接受其他服务端的玩家转移",
    "Get the interval in seconds between server status heartbeats": "获取服务端状态心跳间隔（秒）",
    "Set the interval in seconds between server status heartbeats": "设置服务端状态心跳间隔（秒）",
    "Get default operator permission level": "获取默认管理员权限等级",
    "Set default operator permission level": "设置默认管理员权限等级",
    "Get whether the server hides online player information from status queries": "获取服务端是否对状态查询隐藏在线玩家信息",
    "Enable or disable hiding online player information from status queries": "启用或禁用对状态查询隐藏在线玩家信息",
    "Get whether the server responds to connection status requests": "获取服务端是否响应连接状态请求",
    "Enable or disable the server responding to connection status requests": "启用或禁用服务端响应连接状态请求",
    "Get the entity broadcast range as a percentage": "获取实体广播范围（百分比）",
    "Set the entity broadcast range as a percentage": "设置实体广播范围（百分比）",
    "Get the available game rule keys and their current values": "获取可用的游戏规则键及其当前值",
    "Update game rule value": "更新游戏规则值",

    # === JsonRPCErrors.java ===
    "Parse error": "解析错误",
    "Invalid Request": "无效请求",
    "Method not found": "未找到方法",
    "Invalid params": "无效参数",
    "Internal error": "内部错误",

    # === JsonRpc.java ===
    "Invalid management server secret, must be 40 alphanumeric characters": "管理服务端密钥无效，必须为 40 个字母数字字符",
    "Starting json RPC server on {}": "正在启动 JSON RPC 服务端于 {}",
    "Failed to configure TLS for the server management protocol": "为服务端管理协议配置 TLS 失败",

    # === JsonRpcLogger.java ===
    "RPC Connection #{}: ": "RPC 连接 #{}：",

    # === ManagementServer.java ===
    # "Management server IO #%d" SKIP (thread name)
    "The existing heartbeat was not canceled and the new heartbeat of {} seconds has not been applied.": "现有心跳未被取消，新的 {} 秒心跳尚未应用。",
    "Json-RPC Management connection listening on {}:{}": "JSON-RPC 管理连接正在监听 {}:{}",

    # === OutgoingRpcMethod.java ===
    "Method defined as having no parameters": "方法定义为无参数",
    "Method defined as having no result": "方法定义为无返回值",

    # === OutgoingRpcMethods.java ===
    "Server started": "服务端已启动",
    "Server shutting down": "服务端正在关闭",
    "Server save started": "服务端保存已开始",
    "Server save completed": "服务端保存已完成",
    "Server activity occurred. Rate limited to 1 notification per 30 seconds": "服务端活动发生。限流为每 30 秒通知一次",
    "Player joined": "玩家已加入",
    "Player left": "玩家已离开",
    "Player was oped": "玩家被给予管理员权限",
    "Player was deoped": "玩家被移除管理员权限",
    "Player was added to allowlist": "玩家被添加到白名单",
    "Player was removed from allowlist": "玩家从白名单被移除",
    "Ip was added to ip ban list": "IP 被添加到 IP 封禁列表",
    "Ip was removed from ip ban list": "IP 从 IP 封禁列表被移除",
    "Player was added to ban list": "玩家被添加到封禁列表",
    "Player was removed from ban list": "玩家从封禁列表被移除",
    "Gamerule was changed": "游戏规则已更改",
    "Server status heartbeat, including before the server has spun up": "服务端状态心跳，包括服务端启动前",

    # === Schema.java ===
    "Should not deserialize schema": "不应反序列化模式",

    # === JsonRpcApiSchema.java ===
    "Json RPC API schema": "JSON RPC API 模式",

    # === MinecraftAllowListServiceImpl.java ===
    "Add player '{}' to allowlist": "将玩家 '{}' 添加到白名单",
    "Clear allowlist": "清除白名单",
    "Remove player '{}' from allowlist": "从白名单移除玩家 '{}'",
    "Kick unlisted players": "踢出未在白名单中的玩家",

    # === MinecraftBanListServiceImpl.java ===
    "Add player '{}' to banlist. Reason: '{}'": "将玩家 '{}' 添加到封禁列表。原因：'{}'",
    "Remove player '{}' from banlist": "从封禁列表移除玩家 '{}'",
    "Add ip '{}' to ban list": "将 IP '{}' 添加到封禁列表",
    "Clear ip ban list": "清除 IP 封禁列表",
    "Remove ip '{}' from ban list": "从封禁列表移除 IP '{}'",

    # === MinecraftGameRuleServiceImpl.java ===
    "Game rule '{}' updated from '{}' to '{}'": "游戏规则 '{}' 从 '{}' 更新为 '{}'",

    # === MinecraftOperatorListServiceImpl.java ===
    "Op '{}'": "给予管理员权限 '{}'",
    "Deop '{}'": "移除管理员权限 '{}'",
    "Clear operator list": "清除管理员列表",

    # === MinecraftPlayerListServiceImpl.java ===
    "Remove player '{}'": "移除玩家 '{}'",

    # === MinecraftServerSettingsServiceImpl.java ===
    "Update autosave from {} to {}": "自动保存从 {} 更新为 {}",
    "Update difficulty from '{}' to '{}'": "难度从 '{}' 更新为 '{}'",
    "Update enforce allowlist from {} to {}": "白名单强制执行从 {} 更新为 {}",
    "Update using allowlist from {} to {}": "白名单启用从 {} 更新为 {}",
    "Update max players from {} to {}": "最大玩家数从 {} 更新为 {}",
    "Update pause when empty from {} seconds to {} seconds": "空服暂停时间从 {} 秒更新为 {} 秒",
    "Update player idle timeout from {} minutes to {} minutes": "玩家闲置超时从 {} 分钟更新为 {} 分钟",
    "Update allow flight from {} to {}": "允许飞行从 {} 更新为 {}",
    "Update spawn protection radius from {} to {}": "出生点保护半径从 {} 更新为 {}",
    "Update MOTD from '{}' to '{}'": "MOTD 从 '{}' 更新为 '{}'",
    "Update force game mode from {} to {}": "强制游戏模式从 {} 更新为 {}",
    "Update game mode from '{}' to '{}'": "游戏模式从 '{}' 更新为 '{}'",
    "Update view distance from {} to {}": "视距从 {} 更新为 {}",
    "Update simulation distance from {} to {}": "模拟距离从 {} 更新为 {}",
    "Update accepts transfers from {} to {}": "接受转移从 {} 更新为 {}",
    "Updated status heartbeat interval from {} to {}": "状态心跳间隔从 {} 更新为 {}",
    "The heartbeat interval was not updated to the new value of {} seconds as the json rpc server is null or a pre-existing heartbeat failed to get canceled": "心跳间隔未更新为新值 {} 秒，因为 JSON RPC 服务端为 null 或现有心跳未能取消",
    "Update operator user permission level from {} to {}": "管理员权限等级从 {} 更新为 {}",
    "Update hides online players from {} to {}": "隐藏在线玩家从 {} 更新为 {}",
    "Update replies to status from {} to {}": "响应状态查询从 {} 更新为 {}",
    "Update entity broadcast range percentage from {}% to {}%": "实体广播范围百分比从 {}% 更新为 {}%",

    # === MinecraftServerStateServiceImpl.java ===
    "Save everything. SuppressLogs: {}, flush: {}, force: {}": "保存所有内容。抑制日志：{}，刷新：{}，强制：{}",
    "Halt server. WaitForShutdown: {}": "停止服务端。等待关闭：{}",
    "Send system message: '{}'": "发送系统消息：'{}'",
    "Send system message to '{}' players (overlay: {}): '{}'": "向 '{}' 名玩家发送系统消息（覆盖层：{}）：'{}'",
    "Broadcast system message (overlay: {}): '{}'": "广播系统消息（覆盖层：{}）：'{}'",

    # === BanlistService.java / IpBanlistService.java ===
    # "Management server" SKIP (ban source identifier stored as data)

    # === DiscoveryService.java ===
    "Minecraft Server JSON-RPC": "Minecraft 服务端 JSON-RPC",

    # === GameRulesService.java ===
    "Stated type \\\"": "声明的类型 \\\"",

    # === AuthenticationHandler.java ===
    "Authentication rejected for connection with ip {}: {}": "IP 为 {} 的连接认证被拒绝：{}",
    "Dropping unauthenticated connection with ip {}": "正在丢弃 IP 为 {} 的未认证连接",
    "Invalid API key": "无效的 API 密钥",
    "Origin Not Allowed": "来源不被允许",
    "Missing API key": "缺少 API 密钥",

    # === JsonRpcSslContextProvider.java ===
    "TLS is enabled but keystore is not configured": "TLS 已启用但未配置密钥库",
    "Supplied keystore is not a file or does not exist: '": "提供的密钥库不是文件或不存在：'",
    "To use TLS for the management server, please follow these steps:": "要为管理服务端使用 TLS，请按以下步骤操作：",

    # === ChunkGenerationTask.java ===
    "Can't load chunk, but didn't expect to need to generate": "无法加载区块，但未预期需要生成",

    # === ChunkHolder.java ===
    "Unloaded level chunk": "已卸载的世界区块",
    "Already sent chunk ": "已发送区块 ",
    " in world '": " 在世界 '",
    "' to player ": "' 给玩家 ",

    # === ChunkMap.java ===
    "Unloaded chunks found in range": "在范围内找到已卸载的区块",
    # "St: §" SKIP (debug display format)
    # "Ch: §" SKIP (debug display format)
    # " - status: " SKIP (debug toString)
    "Chunk loading": "区块加载",
    "Use ServerChunkCache#close": "请使用 ServerChunkCache#close",
    "Exception loading chunk": "加载区块时异常",
    "Chunk being loaded": "正在加载的区块",
    "not completed": "未完成",
    # "entity track" SKIP (AsyncCatcher)
    "Illegal ChunkMap::addEntity for world ": "非法的 ChunkMap::addEntity 调用，世界 ",
    " ALREADY CONTAINED (This would have crashed your server)": " 已包含该实体（这会导致您的服务端崩溃）",
    "Entity is already tracked!": "实体已被追踪！",
    "Entity is already tracked": "实体已被追踪",
    # "entity untrack" SKIP
    # "player tracker clear" SKIP
    # "player tracker update" SKIP

    # === ChunkTaskDispatcher.java ===
    # "RES {} {} -> {}" SKIP (debug format)
    # "SUB {} {} {} {}" SKIP (debug format)

    # === DistanceManager.java ===
    # "player ticket throttler" SKIP (task scheduler name)

    # === GenerationChunkHolder.java ===
    "Not done yet": "尚未完成",
    "Unloaded chunk": "已卸载区块",
    "Trying to create chunk out of reasonable bounds: ": "尝试在合理范围外创建区块：",

    # === PlayerSpawnFinder.java ===
    "Searching for spawn": "搜索出生点",
    "Spawn Lookup": "出生点查找",
    " out of ": " 共 ",

    # === ServerChunkCache.java ===
    "Chunk system has shut down, cannot process chunk requests in world '": "区块系统已关闭，无法处理世界 '",
    "' at ": "' 于 ",
    ") status: ": ") 状态：",
    "Chunk not loaded when requested": "请求时区块未加载",
    "Failed to create dimension data storage directory": "创建维度数据存储目录失败",
    # "Scheduling chunk load off-main" SKIP (TickThread message)
    # "Chunk source main thread executor for " SKIP (thread name)

    # === ServerLevel.java ===
    # "Cannot add ticking request async" SKIP (TickThread message)
    # "Cannot remove ticking request async" SKIP
    "Negative counter": "计数器为负",
    # "world border" SKIP (profiler)
    # "Cannot tick an entity off-main" SKIP (TickThread message)
    "Force-added player with duplicate UUID {}": "强制添加了具有重复 UUID {} 的玩家",
    # "entity add" SKIP (AsyncCatcher)
    "Attempted Double World add on {}": "尝试重复添加世界到 {}",
    "recursive call to sendBlockUpdated": "递归调用 sendBlockUpdated",
    # Debug output keys SKIP: "spawning_chunks: %d\n", "spawn_count.%s: %d\n", "entities: %s\n", "block_entity_tickers: %d\n", "block_ticks: %d\n", "fluid_ticks: %d\n", "pending_tasks: %d\n"
    "Level dump": "世界转储",
    # "players: %s, entities: %s [%s], block_entities: %d [%s], block_ticks: %d, fluid_ticks: %d, chunk_source: %s" SKIP (debug format)
    # "Chunk getEntities call" SKIP (AsyncCatcher)
    # "Chunks[S] W: " SKIP (toString)
    "Loaded entity count": "已加载实体数",
    "Server weather": "服务端天气",
    "Rain time: %d (now: %b), thunder time: %d (now: %b)": "降雨时间：%d（当前：%b），雷暴时间：%d（当前：%b）",
    # "entity register" SKIP
    "onTrackingStart called during navigation iteration": "在导航迭代期间调用了 onTrackingStart",
    # "entity unregister" SKIP

    # === ServerPlayer.java ===
    "Failed to hash ": "哈希失败：",
    "Couldn't reattach entity to player": "无法将实体重新附加到玩家",
    "Trying to save removed ender pearl, skipping": "尝试保存已移除的末影珍珠，已跳过",
    "Failed to spawn player ender pearl in level ({}), skipping": "在世界（{}）中生成玩家末影珍珠失败，已跳过",
    "Trying to load ender pearl without level ({}) being loaded, skipping": "尝试加载末影珍珠但世界（{}）未加载，已跳过",
    "Ticking player": "玩家 tick",
    "Player being ticked": "正在 tick 的玩家",

    # === ServerPlayerGameMode.java ===
    # "Server ACK {} {} {} {}" SKIP (debug)
    # "too far" SKIP (debug reason)
    # "too high" SKIP (debug reason)
    # "spawn protection" SKIP (debug reason)
    # "may not interact" SKIP (debug reason)
    # "creative destroy" SKIP (debug reason)
    # "block action restricted" SKIP (debug reason)
    # "insta mine" SKIP (debug reason)
    # "abort destroying since another started (client insta mine, server disagreed)" SKIP (debug reason)
    # "actual start of destroying" SKIP (debug reason)
    # "stopped destroying" SKIP (debug reason)
    "Mismatch in destroy block pos: {} {}": "破坏方块位置不匹配：{} {}",
    # "aborted mismatched destroying" SKIP (debug reason)
    # "aborted destroying" SKIP (debug reason)
    # "server broke {} {} -> {}" SKIP (debug)

    # === ThreadedLevelLightEngine.java ===
    "Ran automatically on a different thread!": "在不同线程上自动运行！",

    # === Ticket.java ===
    "Nullability of identifier should match nullability of comparator": "标识符的可空性应与比较器的可空性匹配",
    # ") to die in " SKIP (toString)

    # === WorldGenRegion.java ===
    "Requested chunk unavailable during world generation": "世界生成期间请求的区块不可用",
    "Exception generating new chunk": "生成新区块时异常",
    "Chunk request details": "区块请求详情",
    "Requested chunk": "请求的区块",
    "Generating status": "生成状态",
    "Requested status": "请求的状态",
    "Actual status": "实际状态",
    "[out of cache bounds]": "[缓存范围外]",
    "Maximum allowed status": "最大允许状态",
    "Requested distance": "请求的距离",
    "Generating chunk": "正在生成的区块",
    "Tried to access a block entity before it was created. {}": "尝试在方块实体创建前访问它。{}",
    "Detected unsafe terrain read during worldgen: reading from chunk [": "检测到世界生成期间不安全的地形读取：从区块 [",
    "] while generating chunk [": "] 读取，而正在生成区块 [",
    "] (distance: ": "]（距离：",
    ", write radius: ": "，写入半径：",
    "), step: ": "），步骤：",
    ", currently generating: ": "，当前正在生成：",
    "Detected setBlock in a far chunk [": "检测到在远端区块 [",
    "], pos: ": "], 位置：",
    ", status: ": "，状态：",
    ", currently generating: ": "，当前正在生成：",
    # "far setBlock call" SKIP (trace dump)
    "We are asking a region for a chunk out of bound": "正在向区域请求超出边界的区块",

    # === LoggingLevelLoadListener.java ===
    "Selecting spawn point for level '{}'...": "正在为世界 '{}' 选择出生点...",
    "Selecting global world spawn...": "正在选择全局世界出生点...",
    "Loading {} persistent chunks for level '{}'...": "正在为世界 '{}' 加载 {} 个持久区块...",
    "Loading {} persistent chunks...": "正在加载 {} 个持久区块...",
    "Loading {} chunks for player spawn...": "正在为玩家出生点加载 {} 个区块...",
    "Prepared spawn area in {} ms": "已在 {} 毫秒内准备好出生区域",

    # === EventLoopGroupHolder.java ===
    # "Unix Domain Socket" SKIP (internal name)
    # " IO #%d" SKIP (thread name)

    # === LegacyQueryHandler.java ===
    "Ping: (<1.3.x) from {}": "Ping：（<1.3.x）来自 {}",
    "<ip address withheld>": "<IP 地址已隐藏>",
    "Ping: (1.4-1.5.x) from {}": "Ping：（1.4-1.5.x）来自 {}",
    "Ping: (1.6) from {}": "Ping：（1.6）来自 {}",

    # === LegacyTextFilter.java ===
    "Missing API key": "缺少 API 密钥",  # duplicate key, same translation
    "Failed to parse chat filter config {}": "解析聊天过滤器配置 {} 失败",
    "Failed to send join/leave packet to {} for player {}": "向 {} 发送玩家 {} 的加入/离开数据包失败",

    # === MemoryServerHandshakePacketListenerImpl.java ===
    "Invalid intention ": "无效的意图 ",

    # === PlayerChunkSender.java ===
    # "SEN {}" SKIP (debug)

    # === PlayerSafetyServiceTextFilter.java ===
    "Failed to open certificate file": "打开证书文件失败",
    "Failed to create confidential client application": "创建机密客户端应用失败",

    # === ServerCommonPacketListenerImpl.java ===
    "Stopping singleplayer server as player logged out": "玩家已退出，正在停止单人服务端",
    "Disconnecting {} for sending keepalive response ({}) out-of-order!": "正在断开 {} 的连接，因其发送了乱序的保活响应（{}）！",
    "Disconnecting {} for sending keepalive response ({}) without matching challenge!": "正在断开 {} 的连接，因其发送了不匹配质询的保活响应（{}）！",
    "Couldn't handle custom payload on channel {}": "无法处理通道 {} 上的自定义载荷",
    "Invalid custom payload payload!": "无效的自定义载荷！",
    "Disconnecting {} due to resource pack {} rejection": "因资源包 {} 被拒绝，正在断开 {} 的连接",
    "Unexpected value: ": "意外的值：",
    "{} was kicked due to keepalive timeout!": "{} 因保活超时而被踢出！",
    "Sending packet": "发送数据包",
    "Packet being sent": "正在发送的数据包",
    "Packet class": "数据包类",
    "{} was kicked for floating too long!": "{} 因悬浮过久而被踢出！",
    "{} was kicked for floating a vehicle too long!": "{} 因载具悬浮过久而被踢出！",

    # === ServerConfigurationPacketListenerImpl.java ===
    "{} ({}) lost connection: {}, while in configuration phase {}": "{}（{}）断开连接：{}，当时处于配置阶段 {}",
    "{} ({}) lost connection: {}": "{}（{}）断开连接：{}",
    "Unexpected response from client: received pack selection, but no negotiation ongoing": "客户端响应异常：收到数据包选择，但没有进行中的协商",
    "Couldn't place player in world": "无法将玩家放入世界",
    "Failed to tick configuration task {}": "tick 配置任务 {} 失败",
    " has not finished yet": " 尚未完成",
    "Failed to start configuration task {}": "启动配置任务 {} 失败",
    "Unexpected request for task finish, current task: ": "任务完成请求异常，当前任务：",
    ", requested: ": "，请求：",

    # === ServerConnectionListener.java ===
    "Using HAProxy, please ensure the server port is adequately firewalled.": "正在使用 HAProxy，请确保服务端端口已充分设置防火墙。",
    "Paper: Using ": "Paper：使用 ",
    " compression from Velocity.": " 压缩（来自 Velocity）。",
    " cipher from Velocity.": " 加密（来自 Velocity）。",
    "Timed out whilst waiting for channel to close": "等待通道关闭时超时",
    "Interrupted whilst closing channel": "关闭通道时被中断",
    "Interrupted whilst closing TCP listener": "关闭 TCP 监听器时被中断",
    "Ticking memory connection": "内存连接 tick",
    "Failed to handle packet for {}": "处理 {} 的数据包失败",
    "Internal server error": "服务端内部错误",
    "Timed out whilst waiting for player connection channel to close": "等待玩家连接通道关闭时超时",
    # "Latency Simulator #%d" SKIP (thread name)

    # === ServerGamePacketListenerImpl.java ===
    "Player profile key for {} has expired!": "玩家 {} 的配置文件密钥已过期！",
    "Ignoring packet due to disconnection": "因已断开连接，正在忽略数据包",
    " is sending move packets too frequently (": " 发送移动数据包过于频繁（",
    " packets since last tick)": " 个数据包，自上次 tick 起）",
    "{} (vehicle of {}) moved too quickly! {},{},{}": "{}（{} 的载具）移动过快！{},{},{}",
    "{} (vehicle of {}) moved wrongly! {}": "{}（{} 的载具）移动异常！{}",
    # "Async Tab Complete Thread - #%d" SKIP (thread name)
    "Player {} interacted with invalid menu {}": "玩家 {} 与无效菜单 {} 交互",
    "Player {} tried to set invalid beacon effects": "玩家 {} 尝试设置无效的信标效果",
    "Player {} tried to set game rule values without required permissions": "玩家 {} 尝试在没有所需权限的情况下设置游戏规则值",
    "Received request to set unknown game rule: {}": "收到设置未知游戏规则的请求：{}",
    "{} tried to send a book too large. Book size: {} - Allowed: {} - Pages: {}": "{} 尝试发送过大的书。书大小：{}——允许：{}——页数：{}",
    "Book too large!": "书太大！",
    "Book edited too quickly!": "书编辑太快！",
    "{} is sending move packets too frequently ({} packets since last tick)": "{} 发送移动数据包过于频繁（自上次 tick 起 {} 个数据包）",
    "{} moved too quickly! {},{},{}": "{} 移动过快！{},{},{}",
    "{} moved wrongly!": "{} 移动异常！",
    "Attempt to teleport removed player {} restricted": "尝试传送已移除的玩家 {} 被限制",
    # "Attempt to teleport removed player" SKIP (trace dump)
    " dropped their items too quickly!": " 丢弃物品过快！",
    "You dropped your items too quickly (Hacking?)": "您丢弃物品过快（开挂？）",
    "Invalid player action": "无效的玩家操作",
    "{} lost connection: {}": "{} 断开连接：{}",
    "Expected packet sequence nr >= 0": "预期数据包序列号 >= 0",
    "{} tried to set an invalid carried item": "{} 尝试设置无效的手持物品",
    "Invalid hotbar selection (Hacking?)": "无效的快捷栏选择（开挂？）",
    "{} issued server command: {}": "{} 执行了服务端命令：{}",
    "Received unsigned command packet from {}, but the command requires signable arguments: {}": "从 {} 收到未签名的命令数据包，但该命令需要可签名参数：{}",
    "Failed to update secure chat state for {}: '{}'": "更新 {} 的安全聊天状态失败：'{}'",
    "Signed command mismatch between server and client ('{}'): got [{}] from client, but expected [{}]": "服务端与客户端之间签名命令不匹配（'{}'）：客户端发来 [{}]，但预期 [{}]",
    "Failed to validate message acknowledgements from {}: {}": "验证 {} 的消息确认失败：{}",
    # "Asynchronous player chat is not allowed here" SKIP (AsyncCatcher)
    "{} tried to send an empty message": "{} 尝试发送空消息",
    "Failed to validate message acknowledgement offset from {}: {}": "验证 {} 的消息确认偏移失败：{}",
    "Invalid client command!": "无效的客户端命令！",
    "Cannot interact with self!": "不能与自己交互！",
    "Player {} tried to attack an invalid entity": "玩家 {} 尝试攻击无效实体",
    "Player {} tried to request game rule values without required permissions": "玩家 {} 尝试在没有所需权限的情况下请求游戏规则值",
    "Player {} clicked invalid slot index: {}, available slots: {}": "玩家 {} 点击了无效的槽位索引：{}，可用槽位：{}",
    "Player {} tried to place impossible recipe {}": "玩家 {} 尝试放置不可能的配方 {}",
    "Player {} was dropping items too fast in creative mode, ignoring.": "玩家 {} 在创造模式中丢弃物品过快，已忽略。",
    "Disconnecting {} for invalid view distance: {}": "因无效视距断开 {} 的连接：{}",
    "Invalid client settings": "无效的客户端设置",
    "Player {} tried to change difficulty to {} without required permissions": "玩家 {} 尝试在没有所需权限的情况下将难度更改为 {}",
    "Player {} tried to change game mode to {} without required permissions": "玩家 {} 尝试在没有所需权限的情况下将游戏模式更改为 {}",
    "Ignoring chat session from {} due to missing Services public key": "因缺少服务公钥，忽略来自 {} 的聊天会话",
    "Client acknowledged config, but none was requested": "客户端确认了配置，但未请求任何配置",

    # === ServerHandshakePacketListenerImpl.java ===
    "Invalid intention ": "无效的意图 ",  # duplicate
    "Failed to check connection throttle": "检查连接限流失败",
    "If you wish to use IP forwarding, please enable it in your BungeeCord config as well!": "如果您希望使用 IP 转发，请同时在 BungeeCord 配置中启用！",
    "Unknown data in login hostname, did you forget to enable BungeeCord in spigot.yml?": "登录主机名中有未知数据，您是否忘记在 spigot.yml 中启用 BungeeCord？",

    # === ServerLoginPacketListenerImpl.java ===
    # "User Authenticator #" SKIP (thread name)
    "Disconnecting {}: {}": "正在断开 {} 的连接：{}",
    "Error whilst disconnecting player": "断开玩家连接时出错",
    "{} lost connection: {}": "{} 断开连接：{}",  # duplicate
    "Unexpected hello packet": "意外的 hello 数据包",
    "Invalid characters in username": "用户名中有无效字符",
    "UUID of player {} is {}": "玩家 {} 的 UUID 为 {}",
    "Failed to verify username!": "验证用户名失败！",
    "Exception verifying ": "验证时异常：",
    "Unexpected key packet": "意外的密钥数据包",
    "Protocol error": "协议错误",
    "Player name not initialized": "玩家名称未初始化",
    "Failed to verify username but will let them in anyway!": "验证用户名失败，但仍允许其加入！",
    "Username '{}' tried to join with an invalid session": "用户名 '{}' 尝试使用无效会话加入",
    "Authentication servers are down but will let them in anyway!": "认证服务端宕机，但仍允许其加入！",
    "Couldn't verify username because servers are unavailable": "因服务端不可用，无法验证用户名",
    "This server requires you to connect with Velocity.": "此服务端要求您通过 Velocity 连接。",
    "Unable to verify player details": "无法验证玩家详情",
    "Unsupported forwarding version ": "不支持的转发版本：",
    ", wanted upto ": "，最高支持到 ",
    "Login phase": "登录阶段",

    # === ServerTextFilter.java ===
    "Could not create text filter - unsupported text filtering version used": "无法创建文本过滤器——使用了不支持的文本过滤版本",
    "Failed to validate message '{}'": "验证消息 '{}' 失败",
    # "application/json; charset=utf-8" SKIP (Content-Type header)
    # "Minecraft server" SKIP (User-Agent)
    # "chat stream for " SKIP (thread name)

    # === PrepareSpawnTask.java ===
    "Unknown respawn dimension {}, defaulting to overworld": "未知的重生维度 {}，默认使用主世界",
    "Player spawn was not ready": "玩家出生点尚未准备好",

    # === NotificationManager.java ===
    "Server already set": "服务端已设置",

    # === DownloadCacheCleaner.java ===
    "Failed to delete cache file {}": "删除缓存文件 {} 失败",
    "Failed to delete empty(?) cache directory {}": "删除空的（？）缓存目录 {} 失败",
    "Failed to vacuum cache dir {}": "清理缓存目录 {} 失败",

    # === DownloadQueue.java ===
    "Failed to download {}": "下载 {} 失败",
    "Failed to log download of {}": "记录 {} 的下载日志失败",
    "Failed to get file size of {}": "获取 {} 的文件大小失败",

    # === FilePackResources.java ===
    "Non {} character in namespace {} in pack {}, ignoring": "数据包 {} 中的命名空间 {} 中有非 {} 字符，已忽略",
    "Invalid path in datapack: {}:{}, ignoring": "数据包中的路径无效：{}:{}，已忽略",
    "Failed to open pack {}": "打开数据包 {} 失败",

    # === OverlayMetadataSection.java ===
    " is not accepted directory name": " 不是可接受的目录名",

    # === PathPackResources.java ===
    "Failed to resolve real path for {}": "解析 {} 的真实路径失败",
    "Invalid path {}: {}": "无效路径 {}：{}",
    "Invalid path in pack: %s:%s, ignoring": "数据包中的路径无效：%s:%s，已忽略",
    "Failed to list path {}": "列出路径 {} 失败",
    "Non-directory entry {} found in namespace directory, rejecting": "在命名空间目录中发现非目录条目 {}，已拒绝",
    "Non {} character in namespace {} in pack directory {}, ignoring": "数据包目录 {} 中的命名空间 {} 中有非 {} 字符，已忽略",

    # === VanillaPackResources.java ===
    "Invalid path {}: {}": "无效路径 {}：{}",  # duplicate
    "Failed to parse vanilla pack metadata": "解析原版数据包元数据失败",

    # === VanillaPackResourcesBuilder.java ===
    "File {} does not exist in classpath": "类路径中不存在文件 {}",
    "Assets URL '{}' uses unexpected schema": "资源 URL '{}' 使用了意外的协议",
    "Couldn't resolve path to vanilla assets": "无法解析原版资源路径",
    " is not directory": " 不是目录",
    "Failed to extract path from {}": "从 {} 提取路径失败",

    # === LinkFSPath.java ===
    " does not represent file": " 不代表文件",
    "Invalid index: ": "无效索引：",
    "All content types should be already handled": "所有内容类型应已被处理",
    "absolute mismatch": "绝对路径不匹配",
    "Failed to create URI": "创建 URI 失败",

    # === LinkFSProvider.java ===
    "Attributes of type ": "类型为 ",
    " not supported": " 的属性不受支持",

    # === LinkFileSystem.java ===
    "Empty paths not allowed": "不允许空路径",
    "Path can't be empty": "路径不能为空",

    # === PackFormat.java ===
    "Unknown or broken overlay entry {}": "未知或损坏的覆盖层条目 {}",
    "Overlay \\\"": "覆盖层 \\\"",
    " missing field, must declare both min_format and max_format": " 缺少字段，必须同时声明 min_format 和 max_format",
    " missing required field ": " 缺少必填字段 ",
    ", must be present in all overlays for any overlays to work across game versions": "，必须存在于所有覆盖层中，覆盖层才能跨游戏版本工作",
    " declares support for version newer than ": " 声明支持比 ",
    ", but is missing mandatory fields min_format and max_format": " 更新的版本，但缺少必填字段 min_format 和 max_format",
    " could not be parsed, missing format version information": " 无法解析，缺少格式版本信息",
    " min_format (": " min_format（",
    ") is greater than max_format (": "）大于 max_format（",
    " is deprecated starting from pack format ": " 从数据包格式 ",
    ". Remove ": " 起已弃用。请从 ",
    " from your pack.mcmeta.": " 中移除。",
    " declares support for format ": " 声明支持格式 ",
    ", but game versions supporting formats 17 to ": "，但支持格式 17 到 ",
    " require a ": " 的游戏版本需要 ",
    " field. Add \\\"": " 字段。请添加 \\\"",
    "] or require a version greater or equal to ": "] 或要求版本大于等于 ",
    " version declaration mismatch between ": " 版本声明不匹配：",
    ") and min_format (": "）和 min_format（",
    " (up to ": "（最高 ",
    ") and max_format (": "）和 max_format（",
    " declares support for formats up to ": " 声明支持最高格式 ",
    ", but game versions supporting formats 17 to ": "，但支持格式 17 到 ",
    " require a pack_format field. Add \\\"pack_format\\\": ": " 的游戏版本需要 pack_format 字段。请添加 \\\"pack_format\\\"：",
    " or require a version greater or equal to ": " 或要求版本大于等于 ",
    "Pack declared support for versions ": "数据包声明支持版本 ",
    " but declared main format is ": "，但声明的主格式为 ",
    "Multi-version packs cannot support minimum version of less than 15, since this will leave versions in range unable to load pack.": "多版本数据包不能支持低于 15 的最低版本，否则范围内的版本将无法加载数据包。",

    # === BuiltInPackSource.java ===
    "Failed to discover packs in {}": "在 {} 中发现数据包失败",

    # === FolderRepositorySource.java ===
    "Failed to list packs in {}": "列出 {} 中的数据包失败",
    "Ignoring potential pack entry: {}": "忽略潜在数据包条目：{}",
    "Found non-pack entry '{}', ignoring": "发现非数据包条目 '{}'，已忽略",
    "Failed to read properties of '{}', ignoring": "读取 '{}' 的属性失败，已忽略",
    "Can't open pack archive at {}": "无法在 {} 处打开数据包归档",

    # === Pack.java ===
    "Error reading pack metadata, attempting fallback type": "读取数据包元数据出错，尝试回退类型",
    "Missing metadata in pack {}": "数据包 {} 中缺少元数据",
    "Failed to read pack {} metadata": "读取数据包 {} 元数据失败",

    # === FallbackResourceManager.java ===
    "Resource {} not found, but was filtered by pack {}": "未找到资源 {}，但被数据包 {} 过滤",
    "Leaked resource: '": "泄漏的资源：'",
    "' loaded from pack: '": "' 从数据包 '",

    # === MultiPackResourceManager.java ===
    "Failed to get filter section from pack {}": "从数据包 {} 获取过滤区段失败",
    "Trailing slash in path ": "路径中有尾部斜杠：",

    # === ProfiledReloadInstance.java ===
    "Finished reloading {}": "完成重载 {}",
    "Resource reload finished after {} ms": "资源重载在 {} 毫秒后完成",
    "{} took approximately {} tasks/{} ms ({} tasks/{} ms preparing, {} tasks/{} ms applying)": "{} 耗时约 {} 个任务/{} 毫秒（{} 个任务/{} 毫秒准备，{} 个任务/{} 毫秒应用）",
    "Total blocking time: {} ms": "总阻塞时间：{} 毫秒",

    # === ReloadableResourceManager.java ===
    "Reloading ResourceManager: {}": "正在重载资源管理器：{}",

    # === SimpleJsonResourceReloadListener.java ===
    "Duplicate data file ignored with ID ": "ID 为 ",
    "Couldn't parse data file '{}' from '{}': {}": "无法从 '{}' 解析数据文件 '{}'：{}",
    "Couldn't parse data file '{}' from '{}'": "无法从 '{}' 解析数据文件 '{}'",

    # === SimpleReloadInstance.java ===
    "not started": "未开始",

    # === LevelBasedPermissionSet.java ===
    # "permission level: " SKIP (toString)

    # === PermissionSetUnion.java ===
    "Cannot have PermissionSetUnion within another PermissionSetUnion": "PermissionSetUnion 不能嵌套在另一个 PermissionSetUnion 中",

    # === BanListEntry.java / CachedUserNameToIdResolver.java ===
    # "yyyy-MM-dd HH:mm:ss Z" SKIP (date format)
    "Usercache.json is corrupted or has bad formatting. Deleting it to prevent further issues.": "Usercache.json 已损坏或格式错误。正在删除以防止进一步问题。",
    "Failed to load profile cache {}": "加载配置文件缓存 {} 失败",
    "Failed to parse date {}": "解析日期 {} 失败",

    # === OldUsersConverter.java ===
    "Could not load existing file {}": "无法加载现有文件 {}",
    "Could not convert user banlist entry for {}": "无法转换玩家 {} 的封禁列表条目",
    "Profile not in the conversionlist": "配置文件不在转换列表中",
    "Could not lookup user banlist entry for {}": "无法查找玩家 {} 的封禁列表条目",
    "Could not request user ": "无法请求玩家 ",
    " from backend systems": " 从后端系统",
    "Could not read old user banlist to convert it!": "无法读取旧的玩家封禁列表进行转换！",
    "Conversion failed, please try again later": "转换失败，请稍后重试",
    "Could not parse old ip banlist to convert it!": "无法解析旧的 IP 封禁列表进行转换！",
    "Could not lookup oplist entry for {}": "无法查找 {} 的管理员列表条目",
    "Could not read old oplist to convert it!": "无法读取旧的管理员列表进行转换！",
    "Could not lookup user whitelist entry for {}": "无法查找玩家 {} 的白名单条目",
    "Could not read old whitelist to convert it!": "无法读取旧的白名单进行转换！",
    "Could not lookup user uuid for {}": "无法查找玩家 {} 的 UUID",
    "Could not convert file for ": "无法转换文件：",
    "Could not find the filename for ": "找不到 ",
    "Can't create directory ": "无法创建目录 ",
    " in world save directory.": " 在世界存档目录中。",
    "**** FAILED TO START THE SERVER AFTER ACCOUNT CONVERSION!": "**** 账户转换后启动服务端失败！",
    "** please remove the following files and restart the server:": "** 请删除以下文件并重启服务端：",

    # === PlayerList.java ===
    # "yyyy-MM-dd 'at' HH:mm:ss z" SKIP (date format)
    "{}[{}] logged in with entity id {} at ([{}]{}, {}, {})": "{}[{}] 已登录，实体 ID 为 {}，位于 ([{}]{}, {}, {})",
    # "loading single player" SKIP (debug)
    # "<singleplayer owner>" SKIP (debug identifier)
    "Removing player mount": "正在移除玩家坐骑",
    # "Save Players" SKIP (ensureMain label)
    # "Not Secure" SKIP (log tag)
    "Failed to copy file {} to {}": "复制文件 {} 到 {} 失败",

    # === StoredUserList.java ===
    "Could not save the list after adding a user.": "添加用户后无法保存列表。",
    "Could not save the list after removing a user.": "移除用户后无法保存列表。",
    "Unable to read file {}, backing it up to {} and creating new copy.": "无法读取文件 {}，正在备份到 {} 并创建新副本。",

    # === GenericThread.java ===
    "Thread {} started": "线程 {} 已启动",
    "Waited {} seconds attempting force stop!": "等待了 {} 秒尝试强制停止！",
    "Thread {} ({}) failed to exit after {} second(s)": "线程 {}（{}）在 {} 秒后仍未退出",
    "Thread {} stopped": "线程 {} 已停止",

    # === QueryThreadGs4.java ===
    # "Query Listener" SKIP (thread name)
    "Unable to determine local host IP, please set server-ip in server.properties": "无法确定本地主机 IP，请在 server.properties 中设置 server-ip",
    "Invalid query port {} found in server.properties (queries disabled)": "server.properties 中发现无效的查询端口 {}（查询已禁用）",
    # Debug messages SKIP: "Packet len {} [{}]", "Packet '{}' [{}]", "Invalid challenge [{}]", "Rules [{}]", "Status [{}]", "Challenge [{}]", "Invalid packet [{}]"
    "Query running on {}:{}": "查询服务端正在 {}:{} 上运行",
    # "closeSocket: {}:{}" SKIP (debug)
    "Unexpected exception": "意外异常",
    "Failed to recover from exception, shutting down!": "无法从异常中恢复，正在关闭！",
    "Unable to initialise query system on {}:{}": "无法在 {}:{} 上初始化查询系统",

    # === RconClient.java ===
    # "RCON Client " SKIP (thread name)
    "Error executing: ": "执行出错：",
    "Unknown request %s": "未知请求 %s",
    "Exception whilst parsing RCON input": "解析 RCON 输入时异常",
    "Thread {} shutting down": "线程 {} 正在关闭",
    "Failed to close socket": "关闭套接字失败",

    # === RconThread.java ===
    # "RCON Listener" SKIP (thread name)
    "IO exception: ": "IO 异常：",
    "No rcon password set in server.properties, rcon disabled!": "server.properties 中未设置 RCON 密码，RCON 已禁用！",
    "RCON running on {}:{}": "RCON 正在 {}:{} 上运行",
    "Unable to initialise RCON on {}:{}": "无法在 {}:{} 上初始化 RCON",
    "Invalid rcon port {} found in server.properties, rcon disabled!": "server.properties 中发现无效的 RCON 端口 {}，RCON 已禁用！",
    # "closeSocket: {}" SKIP (debug)

    # === BlockItem.java ===
    "Player {} tried placing invalid block": "玩家 {} 尝试放置无效方块",
    "Packet processing error": "数据包处理错误",

    # === CreativeModeTab.java ===
    "Special tabs can't have display items": "特殊标签页不能有显示物品",
    "Stack size must be exactly 1": "堆叠大小必须恰好为 1",
    "Accidentally adding the same item stack twice ": "意外地将同一物品堆叠添加了两次 ",
    " to a Creative Mode Tab: ": " 到创造模式物品栏：",

    # === CreativeModeTabs.java ===
    "Duplicate position: ": "重复位置：",

    # === Item.java ===
    "Item must not be minecraft:air": "物品不能是 minecraft:air",
    " does not have components yet": " 尚未有组件",
    "Item classes should end with Item and {} doesn't.": "物品类应以 Item 结尾，但 {} 不是。",
    "Mismatched flag sets": "标志集不匹配",
    "Item id not set": "物品 ID 未设置",
    "Item cannot have both durability and be stackable": "物品不能同时有耐久度和可堆叠",

    # === ItemStack.java ===
    "Empty ItemStack not allowed": "不允许空的 ItemStack",
    "Item stack with stack size of ": "物品堆叠大小为 ",
    " was larger than maximum: ": " 超过最大值：",
    "Item cannot be both damageable and stackable": "物品不能同时可损坏和可堆叠",
    "Item stack with count of ": "物品堆叠数量为 ",
    "Failed to apply component patch '{}' to item: '{}'": "将组件补丁 '{}' 应用到物品 '{}' 失败",

    # === ItemStackTemplate.java ===
    "Item must be non-empty": "物品不能为空",
    "Stack must be non-empty": "堆叠不能为空",
    "Can't create item stack with properties {}, error: {}": "无法创建属性为 {} 的物品堆叠，错误：{}",

    # === KnowledgeBookItem.java ===
    "Invalid recipe: {}": "无效配方：{}",

    # === PotionBrewing.java ===
    "Duplicate recipe ignored with ID ": "ID 为 ",
    "Expected a potion, got: ": "应为药水，但得到：",

    # === BundleContents.java ===
    "Too many items": "物品过多",
    "Excessive total bundle weight": "背包总重量过大",

    # === ChargedProjectiles.java ===
    " items, but maximum is 1024": " 个物品，但最大为 1024",
    "Tried to load invalid items as charged projectiles": "尝试将无效物品加载为已装填弹射物",

    # === DebugStickState.java ===
    "No property on ": "在 ",
    " with name: ": " 上没有名为 ",

    # === Fireworks.java ===
    " explosions, but maximum is 256": " 个烟花，但最大为 256",

    # === ItemContainerContents.java ===
    " items, but maximum is 256": " 个物品，但最大为 256",

    # === ItemLore.java ===
    " lines, but maximum is 256": " 行，但最大为 256",

    # === TypedEntityData.java ===
    "Expected 'id' field in ": "在 ",
    "Failed to apply custom data to block entity at {}": "在 {} 处将自定义数据应用到方块实体失败",
    "Failed to rollback block entity at {} after failure": "失败后回滚 {} 处的方块实体失败",

    # === WritableBookContent.java ===
    " pages, but maximum is 100": " 页，但最大为 100",

    # === WrittenBookContent.java ===
    "Generation was ": "代次为 ",
    ", but must be between 0 and 3": "，但必须在 0 到 3 之间",

    # === Ingredient.java ===
    "Ingredients can't be empty": "配方成分不能为空",
    "Ingredient can't contain air": "配方成分不能包含空气",

    # === RecipeManager.java ===
    "Loaded {} recipes": "已加载 {} 个配方",
    # "Recipe Add" SKIP (AsyncCatcher)
    "Recipe {} can't be placed due to empty ingredients and will be ignored": "配方 {} 因成分为空而无法放置，将被忽略",

    # === RecipeMap.java ===
    "Duplicate recipe ignored with ID ": "ID 为 ",  # duplicate

    # === ShapedRecipePattern.java ===
    "Cannot encode unpacked recipe": "无法编码未展开的配方",
    "Pattern references symbol '": "图案引用了符号 '",
    "' but it's not defined in the key": "'，但它未在键中定义",
    "Key defines symbols that aren't used in pattern: ": "键定义了图案中未使用的符号：",
    "Invalid pattern: too many rows, 3 is maximum": "无效图案：行数过多，最大为 3",
    "Invalid pattern: empty pattern not allowed": "无效图案：不允许空图案",
    "Invalid pattern: too many columns, 3 is maximum": "无效图案：列数过多，最大为 3",
    "Invalid pattern: each row must be the same width": "无效图案：每行宽度必须相同",
    "Invalid key entry: '": "无效的键条目：'",
    "' is an invalid symbol (must be 1 character only).": "' 是无效符号（必须仅为 1 个字符）。",
    "Invalid key entry: ' ' is a reserved symbol.": "无效的键条目：' ' 是保留符号。",

    # === SingleRecipeInput.java ===
    "No item for index ": "索引 ",

    # === SmithingRecipeInput.java ===
    "Recipe does not contain slot ": "配方不包含槽位 ",

    # === ShapedCraftingRecipeDisplay.java ===
    "Invalid shaped recipe display contents": "无效的有序配方显示内容",

    # === SlotDisplay.java ===
    "<any fuel>": "<任意燃料>",

    # === Enchantable.java ===
    "Enchantment value must be positive, but was ": "附魔值必须为正数，但实际为 ",

    # === ItemEnchantments.java ===
    " has invalid level ": " 的附魔等级无效：",

    # === LevelBasedValue.java ===
    "Max must be larger than min, min: ": "最大值必须大于最小值，最小值：",
    ", max: ": "，最大值：",

    # === RunFunction.java ===
    "Enchantment run_function effect failed for non-existent function {}": "附魔 run_function 效果失败，函数 {} 不存在",

    # === SpawnParticlesEffect.java ===
    "Cannot scale an entity position coordinate source": "无法缩放实体位置坐标源",

    # === MaterialAssetGroup.java ===
    "Invalid string to use as a resource path element: ": "用作资源路径元素的字符串无效：",
}

def main():
    with open(LIST, 'r', encoding='utf-8') as f:
        files = [l.strip() for l in f if l.strip()]

    applied_files = 0
    total_applied = 0
    skipped_files = 0
    failed_files = []

    for i, rel in enumerate(files):
        fpath = os.path.join(BASE, rel.replace('/', os.sep))
        if not os.path.isfile(fpath):
            skipped_files += 1
            continue

        # Write translations JSON to temp file
        tmp_json = os.path.join(os.path.dirname(SCRIPT), "_tmp_translations.json")
        with open(tmp_json, 'w', encoding='utf-8') as f:
            json.dump(T, f, ensure_ascii=False)

        # Run apply via subprocess piping
        try:
            with open(tmp_json, 'r', encoding='utf-8') as fin:
                proc = subprocess.run(
                    [sys.executable, SCRIPT, "apply", fpath],
                    stdin=fin, capture_output=True, text=True, encoding='utf-8', timeout=30
                )
            if proc.returncode == 0:
                # Parse "Applied N translations"
                out = proc.stdout.strip()
                if "Applied 0" in out or "applied 0" in out:
                    pass  # no changes
                else:
                    applied_files += 1
                    # Extract count
                    import re
                    m = re.search(r'Applied (\d+) translations', out)
                    if m:
                        total_applied += int(m.group(1))
            else:
                err = proc.stderr.strip()
                if "VERIFICATION FAILED" in err:
                    failed_files.append((rel, err[:200]))
                # else: no translations matched, that's fine
        except Exception as e:
            failed_files.append((rel, str(e)[:200]))

        if (i+1) % 100 == 0:
            print(f"Processed {i+1}/{len(files)}, modified files: {applied_files}, translations applied: {total_applied}", flush=True)

    print(f"\n=== BATCH APPLY COMPLETE ===")
    print(f"Files processed: {len(files)}")
    print(f"Files modified: {applied_files}")
    print(f"Total translations applied: {total_applied}")
    print(f"Files skipped (not found): {skipped_files}")
    if failed_files:
        print(f"Failed files: {len(failed_files)}")
        for rel, err in failed_files[:20]:
            print(f"  {rel}: {err}")

if __name__ == '__main__':
    main()
