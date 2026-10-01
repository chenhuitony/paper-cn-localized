#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply shard_04 translations driven by a global dict, using file_translator core."""
import os, json, importlib_util_path if False else None
import importlib.util

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("ft", os.path.join(SCRIPT_DIR, "file_translator.py"))
ft = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ft)

BASE = r"E:\编程\项目\Paper-main\paper-server\src\minecraft\java"

# ---- Global translation dict: original string content (raw, between quotes) -> Chinese ----
T = {
 # data/DataGenerator
 "Generator {} already run for version {}": "生成器 {} 已针对版本 {} 运行过",
 "Starting provider: {}": "正在启动提供器：{}",
 "{} finished after {} ms": "{} 用时 {} ms 完成",
 "All providers took: {} ms": "所有提供器共耗时：{} ms",
 "Duplicate provider: ": "重复的提供器：",
 "Starting uncached provider: {}": "正在启动未缓存提供器：{}",
 # data/BlockFamilies
 "Duplicate family definition for ": "重复的族定义：",
 # data/DataProvider
 "Failed to save file to {}": "保存文件到 {} 失败",
 # data/HashCache
 "Failed to parse cache {}, discarding": "解析缓存 {} 失败，丢弃",
 "Provider not registered: ": "提供器未注册：",
 "Failed to delete file {}": "删除文件 {} 失败",
 "Caching: total files: {}, old count: {}, new count: {}, removed stale: {}, written: {}": "缓存中：总文件数：{}，旧数量：{}，新数量：{}，移除过期：{}，写入：{}",
 "Cannot write to cache as it has already been closed": "缓存已关闭，无法写入",
 "Missing cache file header": "缺少缓存文件头",
 "Unable write cachefile {}: {}": "无法写入缓存文件 {}：{}",
 # data/Main (CLI help)
 "Show the help menu": "显示帮助菜单",
 "Include server generators": "包含服务端生成器",
 "Include development tools": "包含开发工具",
 "Include data reports": "包含数据报告",
 "Validate inputs": "校验输入",
 "Include all generators": "包含所有生成器",
 "Output folder": "输出文件夹",
 "Input folder": "输入文件夹",
 # advancements
 "Duplicate advancement ": "重复的进度：",
 "Found EntityType with MobCategory only in either expected exceptions or kill_all_mobs advancement: ": "发现具有生物类别但仅出现在预期例外或 kill_all_mobs 进度中的实体类型：",
 "Found EntityType in both expected exceptions and kill_all_mobs advancement: ": "发现同时出现在预期例外和 kill_all_mobs 进度中的实体类型：",
 "Found (new?) EntityType with MobCategory %s which are in neither expected exceptions nor kill_all_mobs advancement: %s": "发现具有生物类别 %s 且既不在预期例外也不在 kill_all_mobs 进度中的（新？）实体类型：%s",
 "Found inconsistencies with kill_all_mobs advancement": "发现 kill_all_mobs 进度存在不一致",
 # info reports
 "Couldn't serialize element {}: {}": "无法序列化元素 {}：{}",
 "Biome Parameters": "生物群系参数",
 "Failed to serialize block ": "序列化方块失败：",
 " (is type registered in BlockTypes?): ": "（类型是否已在 BlockTypes 中注册？）：",
 "Block List": "方块列表",
 "Command Syntax": "命令语法",
 "Datapack Structure": "数据包结构",
 "Duplicate entry for key ": "键存在重复条目：",
 "Packet Report": "数据包报告",
 "Failed to encode components for item ": "为物品编码组件失败：",
 "Default Components": "默认组件",
 "Registry Dump": "转储注册表",
 # loot
 "Missing loottable '%s' for '%s'": "缺少用于 '%s' 的战利品表 '%s'",
 "Created block loot tables for non-blocks: ": "为非方块创建了方块战利品表：",
 " does not have loot table": " 没有战利品表",
 "Duplicate loottable '%s' for '%s'": "用于 '%s' 的战利品表 '%s' 重复",
 "Weird loottables '%s' for '%s', not a LivingEntity so should not have loot": "异常的战利品表 '%s'（用于 '%s'）：不是生物实体，不应有战利品",
 "Created loot tables for entities not supported by datapack: ": "为数据包不支持的实体创建了战利品表：",
 " has no loot table": " 没有战利品表",
 "Loot table random sequence seed collision on ": "战利品表随机序列种子冲突于 ",
 "Found validation problem in {}: {}": "在 {} 中发现校验问题：{}",
 "Failed to validate loot tables, see logs": "校验战利品表失败，详见日志",
 "Loot Tables": "战利品表",
 "Missing built-in table: ": "缺少内置表：",
 # metadata
 "Pack Metadata": "资源包元数据",
 # recipes
 " should remove its 'save' argument as it is equal to default one": " 应移除其 'save' 参数，因为它与默认值相同",
 " is not defined for the family.": " 未在该族中定义。",
 "Duplicate recipe ": "重复的配方：",
 "No way of obtaining recipe ": "无法获取配方：",
 "Symbol '": "符号 '",
 "' is already defined!": "' 已被定义！",
 "Symbol ' ' (whitespace) is reserved and cannot be defined": "符号 ' '（空白）已被保留，不能定义",
 "Pattern must be the same width on every line!": "图案每行宽度必须一致！",
 "Vanilla Recipes": "原版配方",
 # registries
 "Couldn't generate file '": "无法生成文件 '",
 "Placed feature ": "已放置的特性 ",
 " in biome ": " 在生物群系 ",
 " is missing BiomeFilter.biome()": " 缺少 BiomeFilter.biome()",
 "Placed inline feature in biome ": "生物群系中已放置的内联特性 ",
 # structures
 "Failed to read structure input directory": "读取结构输入目录失败",
 "Converted {} from NBT to SNBT": "已将 {} 从 NBT 转换为 SNBT",
 "Couldn't convert {} from NBT to SNBT at {}": "无法在 {} 处将 {} 从 NBT 转换为 SNBT",
 "Failed to read structure input directory, aborting": "读取结构输入目录失败，正在中止",
 "Couldn't write structure {} at {}": "无法在 {} 处写入结构 {}",
 "SNBT Too old, do not forget to update: {} < {}: {}": "SNBT 过旧，别忘了更新：{} < {}：{}",
 # tags
 "Not all enchantments were registered for tooltip ordering. Missing: ": "并非所有附魔都已注册用于提示排序。缺失：",
 "Tags for ": "标签：",
 "Couldn't define tag %s as it is missing following references: %s": "无法定义标签 %s，因为缺少以下引用：%s",
 # placement
 "Chance data cannot be represented as list weight": "概率数据无法表示为列表权重",
 # util/ByIdMap
 "Empty value list": "值列表为空",
 "Duplicate entry on id ": "ID 上存在重复条目：",
 ": current=": "：当前=",
 ", previous=": "，先前=",
 "Values are not continous, found index ": "值不连续，发现索引 ",
 " for value ": "，对应值 ",
 "Missing value at index: ": "索引处缺少值：",
 # ClassInstanceMultiMap
 "Don't know how to search for ": "不知道如何搜索 ",
 # CrudeIncrementalIntIdentityHashBiMap
 "Overflowed :(": "溢出 :(",
 # Crypt
 "Public key must be RSA": "公钥必须是 RSA",
 "Private key must be RSA": "私钥必须是 RSA",
 # CsvOutput
 "Invalid number of columns, expected ": "列数无效，应为 ",
 ", but got ": "，实际为 ",
 # CubicSpline
 "Please register points in ascending order": "请按升序注册点",
 "No elements added": "未添加任何元素",
 "All lengths must be equal, got: ": "所有长度必须相等，实际为：",
 "Cannot create a multipoint spline with no points": "不能在没有点的情况下创建多点样条",
 # DirectoryLock
 "already locked (possibly by other Minecraft instance?)": "已被锁定（可能由另一个 Minecraft 实例占用？）",
 # EasingType
 "x1 must be in range [0; 1]": "x1 必须在范围 [0; 1] 内",
 "x2 must be in range [0; 1]": "x2 必须在范围 [0; 1] 内",
 # ExtraCodecs
 "Unsigned byte was too large: ": "无符号字节过大：",
 "Value must be non-negative: ": "值必须非负：",
 "Value must be positive: ": "值必须为正：",
 "Invalid regex pattern '": "无效的正则表达式模式：'",
 "Malformed base64 string": "base64 字符串格式错误",
 "Cannot have more than 16 properties, but was ": "属性不能超过 16 个，实际为 ",
 "Player name contained disallowed characters: '": "玩家名称包含不允许的字符：'",
 "Expected non-empty string": "应为非空字符串",
 "Expected one codepoint, got: ": "应为一个码点，实际为：",
 "Invalid string to use as a resource path element: ": "用作资源路径元素的字符串无效：",
 "Disallowed chat character: '": "不允许的聊天字符：'",
 "Hex color must begin with #": "十六进制颜色必须以 # 开头",
 "Hex color is wrong size, expected ": "十六进制颜色长度错误，应为 ",
 " digits but got ": " 位，实际为 ",
 "Color value out of range: ": "颜色值超出范围：",
 "Invalid color value: ": "无效的颜色值：",
 " -> using default)": " -> 使用默认值)",
 "Unknown element id: ": "未知的元素 id：",
 "Element with unknown id: ": "具有未知 id 的元素：",
 "Value must be within range [": "值必须在范围 [",
 "List must have contents": "列表必须有内容",
 "Map must have contents": "映射必须有内容",
 "Mixed type list: element ": "混合类型列表：元素 ",
 " had type ": " 的类型为 ",
 ", but list is of type ": "，但列表类型为 ",
 "Caught exception decoding ": "解码时捕获到异常：",
 "Map is too long: ": "映射过长：",
 ", expected range [0-": "，期望范围 [0-",
 "Missing \\": "缺少 \\\"",
 "No value with id: ": "没有 id 对应的值：",
 "Illegal absolute path: ": "非法的绝对路径：",
 "Illegal path traversal: ": "非法的路径遍历：",
 "Value for ": "值 ",
 " is null": " 为 null",
 "Map entry '": "映射条目 '",
 "Empty or invalid map contents are not allowed": "不允许空或无效的映射内容",
 # FileSystemUtil
 "Unable to get path for: {}": "无法获取路径：{}",
 # FileUtil
 "Invalid path '": "无效路径：'",
 "Invalid segment '": "无效段：'",
 "' in path '": "'，在路径 '",
 "Path must have at least one element": "路径至少要有一个元素",
 "Illegal segment ": "非法段 ",
 " in path ": "，在路径 ",
 # FileZipper
 "Compressed to {}": "已压缩到 {}",
 # FutureChain
 "Chain link failed, continuing to next one": "链环节失败，继续下一个",
 # GsonHelper
 "Missing field ": "缺少字段 ",
 " to be a string, was ": " 应为字符串，实际为 ",
 ", expected to find a string": "，期望找到一个字符串",
 " to be an item, was unknown string '": " 应为物品，但是未知字符串 '",
 " to be an item, was ": " 应为物品，实际为 ",
 ", expected to find an item": "，期望找到一个物品",
 " to be a Boolean, was ": " 应为布尔值，实际为 ",
 ", expected to find a Boolean": "，期望找到一个布尔值",
 " to be a Double, was ": " 应为 Double，实际为 ",
 ", expected to find a Double": "，期望找到一个 Double",
 " to be a Float, was ": " 应为 Float，实际为 ",
 ", expected to find a Float": "，期望找到一个 Float",
 " to be a Long, was ": " 应为 Long，实际为 ",
 ", expected to find a Long": "，期望找到一个 Long",
 " to be a Int, was ": " 应为 Int，实际为 ",
 ", expected to find a Int": "，期望找到一个 Int",
 " to be a Byte, was ": " 应为 Byte，实际为 ",
 ", expected to find a Byte": "，期望找到一个 Byte",
 " to be a Character, was ": " 应为 Character，实际为 ",
 ", expected to find a Character": "，期望找到一个 Character",
 " to be a BigDecimal, was ": " 应为 BigDecimal，实际为 ",
 ", expected to find a BigDecimal": "，期望找到一个 BigDecimal",
 " to be a BigInteger, was ": " 应为 BigInteger，实际为 ",
 ", expected to find a BigInteger": "，期望找到一个 BigInteger",
 " to be a Short, was ": " 应为 Short，实际为 ",
 ", expected to find a Short": "，期望找到一个 Short",
 " to be a JsonObject, was ": " 应为 JsonObject，实际为 ",
 ", expected to find a JsonObject": "，期望找到一个 JsonObject",
 " to be a JsonArray, was ": " 应为 JsonArray，实际为 ",
 ", expected to find a JsonArray": "，期望找到一个 JsonArray",
 "null (missing)": "null（缺失）",
 "null (json)": "null（json）",
 "an array (": "数组（",
 "an object (": "对象（",
 "a number (": "数字（",
 "a boolean (": "布尔值（",
 "JSON data was null or empty": "JSON 数据为空或 null",
 "Couldn't write ": "无法写入 ",
 "Character count over limit: ": "字符数超过限制：",
 # HashOps
 "Unsupported operation": "不支持的操作",
 "Can't convert from this type": "无法从该类型转换",
 # HttpUtil
 "Returning cached file since actual hash matches requested": "实际哈希与请求匹配，返回缓存文件",
 "Failed to check cached file {}": "检查缓存文件 {} 失败",
 "Existing file {} not found or had mismatched hash": "已存在的文件 {} 未找到或哈希不匹配",
 "Failed to remove existing file ": "移除已存在的文件失败：",
 "Filesize is bigger than maximum allowed (file is ": "文件大小超过最大允许值（文件大小为 ",
 ", limit is ": "，限制为 ",
 "Hash of downloaded file (": "已下载文件的哈希（",
 ") did not match requested (": "）与请求的（",
 "HTTP response error: {}": "HTTP 响应错误：{}",
 "Failed to read response from server": "从服务端读取响应失败",
 "Failed to download file ": "下载文件失败：",
 "Failed to update modification time of {}": "更新 {} 的修改时间失败",
 "Mismatched hash of file {}, expected {} but found {}": "文件 {} 哈希不匹配，应为 {}，实际为 {}",
 "Filesize was bigger than maximum allowed (got >= ": "文件大小超过最大允许值（达到 >= ",
 ", limit was ": "，限制为 ",
 "Download interrupted": "下载中断",
 # InclusiveRange
 "min_inclusive must be less than or equal to max_inclusive": "min_inclusive 必须小于或等于 max_inclusive",
 "Range limit too low, expected at least ": "范围下限过低，至少应为 ",
 "Range limit too high, expected at most ": "范围上限过高，至多应为 ",
 # KeyframeTrack
 "Track has no keyframes": "轨道没有关键帧",
 "Keyframes must not be empty": "关键帧不能为空",
 "Keyframes must be ordered by ticks field": "关键帧必须按 ticks 字段排序",
 "More than 2 keyframes on same tick: ": "同一 tick 上有超过 2 个关键帧：",
 "Keyframe at tick ": "tick 处的关键帧 ",
 " must be in range [0; ": " 必须在范围 [0; ",
 # ModCheck
 " brand changed to '": " 品牌已更改为 '",
 " jar signature invalidated": " jar 签名已失效",
 " jar signature and brand is untouched": " jar 签名和品牌未改动",
 "Probably not.": "很可能不是。",
 "Very likely;": "很可能是；",
 # Mth
 "itemCount must be greater than or equal to zero": "itemCount 必须大于或等于零",
 "Something went wrong when converting from HSV to RGB. Input was ": "从 HSV 转换为 RGB 时出错。输入为 ",
 "upperBound %d expected to be > lowerBound %d": "upperBound %d 应大于 lowerBound %d",
 "step size expected to be >= 1, was %d": "步长应 >= 1，实际为 %d",
 # NativeModuleLister
 "Failed to find module info for {}": "找不到 {} 的模块信息",
 "Can't get version value ": "无法获取版本值：",
 # PngInfo
 "Bad PNG Signature: ": "PNG 签名错误：",
 "Bad length for IHDR chunk: ": "IHDR 块长度错误：",
 "Bad type for IHDR chunk: ": "IHDR 块类型错误：",
 "PNG header missing": "缺少 PNG 头",
 "Bad PNG Signature": "PNG 签名错误",
 "Bad length for IHDR chunk!": "IHDR 块长度错误！",
 "Bad type for IHDR chunk!": "IHDR 块类型错误！",
 # ProblemReporter
 "[{}] Serialization errors:\\n{}": "[{}] 序列化错误：\\n{}",
 # RandomSource
 "bound - origin is non positive": "bound - origin 非正",
 # SegmentedAnglePrecision
 "Precision cannot be less than 2 bits": "精度不能小于 2 位",
 "Precision cannot be greater than 30 bits": "精度不能大于 30 位",
 # SignatureValidator
 "Failed to verify signature": "校验签名失败",
 "Failed to verify Services signature": "校验 Services 签名失败",
 # Signer
 "Failed to sign message": "签名消息失败",
 # SimpleBitStorage
 "Invalid length given for storage, got: ": "给定的存储长度无效，实际为：",
 " but expected: ": "，但应为：",
 "Size > 4096 not supported": "不支持 Size > 4096",
 # SortedArraySet
 "Initial capacity (": "初始容量（",
 ") is negative": "）为负",
 # StaticCache2D
 "Requested out of range value (": "请求的值超出范围（",
 ") from ": "）来自 ",
 # StrictJsonParser
 "Did not consume the entire document.": "未消费完整文档。",
 # TaskChainer
 "Task failed": "任务失败",
 # ThreadingDetector
 " from multiple threads": " 来自多个线程",
 "Thread dumps": "线程转储",
 "Thread dumps: \\n{}": "线程转储：\\n{}",
 # Util
 "Uncaught exception in thread ": "线程中未捕获的异常：",
 "No jar file system provider found": "找不到 jar 文件系统提供器",
 "{} died": "{} 已终止",
 "{} shutdown": "{} 已关闭",
 "Wrong {} property value '{}'. Should be an integer value between 1 and {}.": "{} 属性值 '{}' 错误。应为 1 到 {} 之间的整数。",
 "Could not parse {} property value '{}'. Should be an integer value between 1 and {}.": "无法解析 {} 属性值 '{}'。应为 1 到 {} 之间的整数。",
 "Caught exception in thread {}": "线程 {} 中捕获到异常",
 "Exception on worker thread": "工作线程上的异常",
 "No data fixer registered for {}": "没有为 {} 注册数据修复器",
 "Missing protocol in URI: ": "URI 中缺少协议：",
 "Unsupported protocol in URI: ": "URI 中协议不受支持：",
 "Trying to throw a fatal exception, pausing in IDE": "试图抛出致命异常，在 IDE 中暂停",
 "Did you remember to set a breakpoint here?": "你是否记得在这里设置断点？",
 "Failed to rename": "重命名失败",
 "Failed to delete": "删除失败",
 "Input is not a list of ": "输入不是列表，应为 ",
 "Timer hack thread interrupted, that really should not happen": "Timer hack 线程被中断，这本不该发生",
 "Interrupted wait": "等待被中断",
 "Tasks left in queue: {}": "队列中剩余任务：{}",
 "Reading type": "读取类型",
 "Couldn't open location '{}'": "无法打开位置 '{}'",
 "Couldn't open uri '{}'": "无法打开 URI '{}'",
 # ContextKeySet
 " is already optional": " 已经是可选的",
 " is already required": " 已经是必需的",
 # ContextMap
 "Parameters not allowed in this parameter set: ": "此参数集中不允许的参数：",
 "Missing required parameters: ": "缺少必需参数：",
 # datafix/PackedBitStorage
 # (same keys as SimpleBitStorage already covered)
 # datafix/fixes
 "Poi type is not what was expected.": "POI 类型与预期不符。",
 "Could not inject: key type is not the same": "无法注入：键类型不一致",
 "%s: Unknown type %s in '%s'": "%s：'%s' 中存在未知类型 %s",
 "Could not create new piston block entity.": "无法创建新的活塞方块实体。",
 "Could not parse newly created block state tag.": "无法解析新创建的方块状态标签。",
 "Could not create record item stack.": "无法创建唱片物品栈。",
 "Expected and actual types don't match.": "预期类型与实际类型不匹配。",
 "block type is not what was expected.": "方块类型与预期不符。",
 "Tile entity type is not a list type.": "方块实体类型不是列表类型。",
 "Could not parse newly created bed block entity.": "无法解析新创建的床方块实体。",
 "Malformed Chunk.Level.Sections": "Chunk.Level.Sections 格式错误",
 "ChunkNibbleArrays should be 2048 bytes not: ": "ChunkNibbleArrays 应为 2048 字节，实际为：",
 "In chunk: {}x{} found a duplicate block entity at position: [{}, {}, {}]": "在区块：{}x{} 中发现位置 [{}, {}, {}] 处存在重复的方块实体",
 "Input entity_equipment type does not match expected": "输入 entity_equipment 类型与预期不符",
 "Output entity_equipment type does not match expected": "输出 entity_equipment 类型与预期不符",
 "Could not parse newly created empty itemstack.": "无法解析新创建的空物品栈。",
 "Dynamic type check failed: %s not equal to %s": "动态类型检查失败：%s 不等于 %s",
 "Old entity type is not what was expected.": "旧实体类型与预期不符。",
 "New entity type is not what was expected.": "新实体类型与预期不符。",
 "angry_at has no value.": "angry_at 没有值。",
 "Trusted contained invalid data.": "Trusted 包含无效数据。",
 "item name type is not what was expected.": "物品名称类型与预期不符。",
 "Expecting sections to be a list.": "期望 sections 为列表。",
 "Block state type is not what was expected.": "方块状态类型与预期不符。",
 "Text component type did not match, expected ": "文本组件类型不匹配，应为 ",
 " but got ": "，实际为 ",
 "Legacy hoverEvent: ": "旧版 hoverEvent：",
 "CustomBossEvents contains invalid UUIDs.": "CustomBossEvents 包含无效 UUID。",
 "List exptected": "应为列表",
 "Entity name type is not what was expected.": "实体名称类型与预期不符。",
 "Can't find choice type for criteria": "找不到条件选项类型",
 "Failed to find custom criterion type variant": "找不到自定义条件类型变体",
 "Encountered unknown structure in datafixer: {}": "数据修复器中遇到未知结构：{}",
 "<missing key>": "<缺失的键>",
 "Trapped Chest fix": "陷阱箱修复",
 "Block Entity was expected to be a chest": "方块实体应为箱子",
 "Failed to parse NBT for ": "解析以下对象的 NBT 失败：",
 "Failed to parse Trial Spawner NBT config: ": "解析试炼生成器 NBT 配置失败：",
 "Failed to unflatten text component json: {}": "展开文本组件 JSON 失败：{}",
 "Unable load old custom worlds.": "无法加载旧的自定义世界。",
 "Failed to parse tag: {}": "解析标签失败：{}",
 "Failed to parse block properties: {}": "解析方块属性失败：{}",
 "Failed to parse particle options: {}": "解析粒子选项失败：{}",
 # schemas
 "Didn't find ": "未找到 ",
 " in schema": "，在 schema 中",
 "Unable to resolve BlockEntity for ItemStack: {}": "无法为物品栈解析方块实体：{}",
 # debug
 " ticks ago": " tick 前",
 # debugchart
 "defaults have incorrect length of ": "defaults 长度不正确：",
 " out of bounds for dimensions ": " 超出维度范围 ",
 " out of bounds for length ": " 超出长度范围 ",
 # eventlog
 "Compressed target file already exists: ": "压缩目标文件已存在：",
 "Raw log file is already locked, cannot compress: ": "原始日志文件已被锁定，无法压缩：",
 "Failed to delete expired event log file: {}": "删除过期事件日志文件失败：{}",
 "Failed to compress event log file: {}": "压缩事件日志文件失败：{}",
 "Event log has already been closed": "事件日志已关闭",
 # filefix exceptions
 "Moves that failed to revert": "回滚失败的移动",
 "World upgrade": "世界升级",
 "New Name": "新名称",
 "Upgrading world failed with errors": "升级世界时出错",
 "File system capabilities": "文件系统能力",
 "Hard Links": "硬链接",
 "Atomic Move": "原子移动",
 "Target already exists, skipping move from {} to {}": "目标已存在，跳过从 {} 到 {} 的移动",
 "Attempting to delete DS_Store at '{}'": "尝试删除位于 '{}' 的 DS_Store",
 "Failed to delete file '{}' at '{}'": "删除位于 '{}' 的文件 '{}' 失败",
 "Failed to delete directory '{}', as it's not empty. Content: {}": "删除目录 '{}' 失败，因为它非空。内容：{}",
 "Failed to delete directory '{}' because {}": "删除目录 '{}' 失败，原因：{}",
 'Starting upgrade for world "{}"': '开始升级世界 "{}"',
 "Found previously interrupted world upgrade, attempting to continue it": "发现之前中断的世界升级，尝试继续",
 "Failed to clean up": "清理失败",
 "File system capabilities: {}": "文件系统能力：{}",
 'Applying file structure changes for world "{}"': '正在为世界 "{}" 应用文件结构变更',
 "Moving new hardlinked world to top level": "将新的硬链接世界移动到顶层",
 "Encountered error trying to move world folder:": "移动世界文件夹时出错：",
 "Moving files into new file structure": "正在将文件移入新文件结构",
 "Moving new world to top level": "将新世界移动到顶层",
 "Encountered error while trying to create new world folder:": "创建新世界文件夹时出错：",
 "Failed to delete {}": "删除 {} 失败",
 "Complete move": "完成移动",
 "Start cleanup": "开始清理",
 "Failed to delete outdated level.dat files: ": "删除过时的 level.dat 文件失败：",
 "Moving out old world folder": "移出旧世界文件夹",
 "Failed to move outdated world folder out of the way; will try to delete instead: ": "移动过时世界文件夹失败，将改为尝试删除：",
 "Failed to delete outdated world folder: ": "删除过时世界文件夹失败：",
 "Moving in new world folder": "移入新世界文件夹",
 "Failed to move in new world folder: ": "移入新世界文件夹失败：",
 'Done applying file structure changes for world "{}". Cleaning up outdated data...': '已完成对世界 "{}" 的文件结构变更。正在清理过时数据...',
 "Failed to clean up old world folder": "清理旧世界文件夹失败",
 'Upgrade done for world "{}"': '世界 "{}" 升级完成',
 "Tried to add file fixer with unknown schema. Add it through FileFixerUpper#addSchema instead": "试图添加具有未知 schema 的文件修复器。请改为通过 FileFixerUpper#addSchema 添加",
 "Tried to add too recent file fix for version: %s. The data version of the game is: %s": "试图添加版本过新的文件修复器：%s。游戏的数据版本为：%s",
 "Tried to add too recent file fix for version: %s. The most recent file fix version is %s": "试图添加版本过新的文件修复器：%s。最新的文件修复器版本为 %s",
 "Missing file: {}": "缺少文件：{}",
 "Failed to write to {}: {}": "写入 {} 失败：{}",
 "Cannot access world files": "无法访问世界文件",
 "Trying to get only file, but there are ": "试图获取唯一文件，但存在 ",
 "Failed to close file: ": "关闭文件失败：",
 "Cannot request new file access here.": "不能在此请求新的文件访问。",
 "Failed to discover dimensions, assuming default: {}": "发现维度失败，使用默认值：{}",
 "'other' is different type of Path": "'other' 是不同类型的 Path",
 "Other path is of mismatching file system": "其他路径的文件系统不匹配",
 "DELETE_ON_CLOSE is not supported by CowFS": "CowFS 不支持 DELETE_ON_CLOSE",
 ": not a regular file": "：不是常规文件",
 "Can't remove root": "无法移除根",
 ": can't move root directory": "：无法移动根目录",
 "CowFs does not support atomic move": "CowFs 不支持原子移动",
 "Temporary directory already exists: ": "临时目录已存在：",
 "Cannot build copy-on-write file system when symlink is present: ": "存在符号链接时无法构建写时复制文件系统：",
 "Cannot build copy-on-write file system, missing write access for file: ": "无法构建写时复制文件系统，缺少对文件的写权限：",
 "Not a regular file: ": "不是常规文件：",
 "Reverted move from {} to {}": "已回滚从 {} 到 {} 的移动",
 "Failed to revert move from {} to {}": "回滚从 {} 到 {} 的移动失败",
 "Skipping reverting move from {} to {} as it's not a file": "跳过回滚从 {} 到 {} 的移动，因为它不是文件",
 "Successfully reverted back to previous world state": "已成功回滚到之前的世界状态",
 "Completed reverting with errors": "回滚完成，但存在错误",
 " was a file, expected directory": " 是文件，应为目录",
 # jmx
 "Historical tick times (ms)": "历史 tick 时间（ms）",
 "Current average tick time (ms)": "当前平均 tick 时间（ms）",
 "metrics for dedicated server": "专用服务端指标",
 "Failed to initialise server as JMX bean": "将服务端初始化为 JMX Bean 失败",
 # packrat
 "Trying to override rule: ": "试图覆盖规则：",
 "Unbound names: ": "未绑定的名称：",
 "No rule called ": "没有名为 的规则：",
 "Unbound rule ": "未绑定的规则 ",
 "Malformed scope: ": "作用域格式错误：",
 "No value for atom ": "atom 没有对应的值：",
 "No value for atoms ": "atoms 没有对应的值：",
 "Corrupted stack": "栈已损坏",
 "Too deep": "过深",
 "Failed to parse: ": "解析失败：",
 # profiling
 "Profiler tick already started - missing endTick()?": "分析器 tick 已开始——是否缺少 endTick()？",
 "Profiler tick already ended - missing startTick()?": "分析器 tick 已结束——是否缺少 startTick()？",
 "Profiler tick ended before path was fully popped (remainder: '{}'). Mismatched push/pop?": "分析器 tick 在路径完全弹出前结束（剩余：'{}'）。push/pop 不匹配？",
 "Cannot push '{}' to profiler if profiler tick hasn't started - missing startTick()?": "分析器 tick 未开始时无法 push '{}'——是否缺少 startTick()？",
 "Cannot pop from profiler if profiler tick hasn't started - missing startTick()?": "分析器 tick 未开始时无法 pop——是否缺少 startTick()？",
 "Tried to pop one too many times! Mismatched push() and pop()?": "pop 次数过多！push() 和 pop() 不匹配？",
 "Something's taking too long! '{}' took aprox {} ms": "某个操作耗时过长！'{}' 约耗时 {} ms",
 "Could not save profiler results to {}": "无法将分析器结果保存到 {}",
 "Time span: ": "时间跨度：",
 "Tick span: ": "tick 跨度：",
 " ticks per second. It should be ": " ticks/秒。应为 ",
 " ticks per second\\n\\n": " ticks/秒\\n\\n",
 "--- BEGIN PROFILE DUMP ---\\n\\n": "--- 开始分析转储 ---\\n\\n",
 "--- END PROFILE DUMP ---\\n\\n": "--- 结束分析转储 ---\\n\\n",
 "--- BEGIN COUNTER DUMP ---\\n\\n": "--- 开始计数器转储 ---\\n\\n",
 "--- END COUNTER DUMP ---\\n\\n": "--- 结束计数器转储 ---\\n\\n",
 "[[ EXCEPTION ": "[[ 异常 ",
 "-- Counter: ": "-- 计数器： ",
 "Profiler is already active": "分析器已处于活动状态",
 "Profiler was not active": "分析器未处于活动状态",
 "Recorded long tick -- wrote info to: {}": "记录到过长 tick——信息已写入：{}",
 "Could not find default flight recorder config at {}": "在 {} 找不到默认的飞行记录器配置",
 "Failed to start flight recorder using configuration at {}": "使用位于 {} 的配置启动飞行记录器失败",
 "Not currently profiling": "当前未在分析",
 "Profiling already in progress": "分析已在进行中",
 "Failed to start jfr profiling": "启动 JFR 分析失败",
 "Started flight recorder profiling id({}):name({}) - will dump to {} on exit or stop command": "已启动飞行记录器分析 id({})：name({})——将在退出或停止命令时转储到 {}",
 "Attempted to start Flight Recorder, but it's not supported on this JVM": "试图启动飞行记录器，但此 JVM 不支持",
 "Attempted to stop Flight Recorder, but it's not supported on this JVM": "试图停止飞行记录器，但此 JVM 不支持",
 "Dumped flight recorder profiling to ": "已将飞行记录器分析转储到 ",
 "Failed to parse JFR recording": "解析 JFR 记录失败",
 "Dumped recording summary to ": "已将记录摘要转储到 ",
 "Failed to output JFR report": "输出 JFR 报告失败",
 "Thread allocation stat timestamps are not in chronological order for thread {}, skipping it": "线程 {} 的线程分配统计时间戳未按时间顺序排列，已跳过",
 "Not running": "未运行",
 "Sampler for metric %s not started!": "指标 %s 的采样器未启动！",
 "Not started!": "未启动！",
 "Failed to query cpu, no cpu stats will be recorded": "查询 CPU 失败，将不记录 CPU 统计",
 "Expected at least one sampler to persist": "至少应有一个采样器需要持久化",
 "Flushed metrics to {}": "已将指标刷新到 {}",
 # random
 "Weight should be >= 0": "权重应 >= 0",
 "Found 0 weight, make sure this is intentional!": "发现权重为 0，请确认这是有意的！",
 "Weighted list has no elements": "权重列表没有元素",
 "Weighted list must contain at least one entry with non-zero weight": "权重列表必须至少包含一个非零权重的条目",
 " exceeded total weight": " 超出总权重",
 "Sum of weights must be <= 2147483647": "权重之和必须 <= 2147483647",
 "Negative total weight in getRandomItem": "getRandomItem 中总权重为负",
 # thread
 "Could not schedule ConsecutiveExecutor": "无法调度 ConsecutiveExecutor",
 "Error executing task on {}": "在 {} 上执行任务时出错",
 "Priority %d not supported. Expected range [0-%d]": "不支持优先级 %d。期望范围 [0-%d]",
 # valueproviders
 "Max must be at least min, min_inclusive: ": "Max 必须至少为 min，min_inclusive：",
 ", max_inclusive: ": "，max_inclusive：",
 "Max must be larger than min: [": "Max 必须大于 min：[",
 "Value provider too low: ": "值提供器过低：",
 "Value provider too high: ": "值提供器过高：",
 "Plateau can at most be the full span: [": "平台最多可为整个区间：[",
 "Max must be larger than min, min: ": "Max 必须大于 min，min：",
 ", max: ": "，max：",
 "Max must exceed min": "Max 必须大于 min",
 # worldupdate
 "RegionStorageUpgrader has not been initialized": "RegionStorageUpgrader 尚未初始化",
 "Failed to convert region file {}": "转换区域文件 {} 失败",
 "Error upgrading chunk": "升级区块时出错",
 "Failed to read chunks from region file {}": "从区域文件 {} 读取区块失败",
 "Error upgrading chunk {}": "升级区块 {} 时出错",
 "Failed to replace an old region file. New file {} does not exist.": "替换旧区域文件失败。新文件 {} 不存在。",
 "Failed to replace an old region file": "替换旧区域文件失败",
 "Can't add two fixers for the same data version": "不能为同一数据版本添加两个修复器",
 "Upgrading progress: {}%": "升级进度：{}%",
 "Invalid Status received: ": "收到无效的状态：",
 "Error upgrading world": "升级世界时出错",
 "Chunk {} has invalid position {}": "区块 {} 的位置 {} 无效",
 "Upgrading entities": "正在升级实体",
 "Upgrading POIs": "正在升级 POI",
 "Upgrading blocks": "正在升级方块",
 "World optimization finished after {} seconds": "世界优化在 {} 秒后完成",
}

def main():
    with open(os.path.join(SCRIPT_DIR, "shard04_collected.json"), encoding="utf-8") as f:
        data = json.load(f)
    ws = data["with_strings"]

    modified_files = []
    total_applied = 0
    no_applied_files = []
    failures = []

    for rel, items in ws.items():
        path = os.path.join(BASE, rel.replace("/", os.sep))
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        strings = ft.find_strings_with_positions(content)
        repls = []
        for start, end, sc, is_tb in strings:
            if sc in T:
                trans = T[sc]
                if trans != sc:
                    repls.append((start, end, sc, trans, is_tb))
        if not repls:
            no_applied_files.append(rel)
            continue
        repls.sort(key=lambda x: x[0], reverse=True)
        modified = content
        applied = 0
        for start, end, orig, trans, is_tb in repls:
            actual = modified[start+1:end-1] if not is_tb else modified[start+3:end-3]
            if actual != orig:
                failures.append((rel, f"mismatch at {start}"))
                continue
            if is_tb:
                modified = modified[:start+3] + trans + modified[end-3:]
            else:
                modified = modified[:start+1] + trans + modified[end-1:]
            applied += 1
        issues = ft.verify_file(modified)
        if issues:
            failures.append((rel, "; ".join(issues)))
            continue
        with open(path, "w", encoding="utf-8") as f:
            f.write(modified)
        modified_files.append((rel, applied))
        total_applied += applied

    report = {
        "modified_files_count": len(modified_files),
        "total_translated": total_applied,
        "no_applied_files_count": len(no_applied_files),
        "no_applied_files": no_applied_files,
        "failures": failures,
    }
    with open(os.path.join(SCRIPT_DIR, "shard04_apply_report.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=1)
    print("modified files:", len(modified_files))
    print("translated strings:", total_applied)
    print("no-apply files:", len(no_applied_files))
    print("failures:", len(failures))
    for rel, msg in failures:
        print("  FAIL:", rel, "->", msg)

if __name__ == "__main__":
    main()
