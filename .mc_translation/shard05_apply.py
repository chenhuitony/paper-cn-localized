#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply shard05 translations. Master dict: {relpath: {original: translated}}."""
import sys, os, json, subprocess

BASE = r"E:\编程\项目\Paper-main\paper-server\src\minecraft\java"
TRANSLATOR = r"E:\编程\项目\Paper-main\.mc_translation\file_translator.py"

T = {
# ===== ca/spottedleaf/dataconverter/minecraft/MCVersionRegistry.java =====
"ca/spottedleaf/dataconverter/minecraft/MCVersionRegistry.java": {
    "Error registering version \\\"": "注册版本时出错：\\\"",
    "' is already associated with \\\"": "' 已与 \\\"",
    "Added too late!": "添加得太晚了！",
    " is not registered to have dataconverters, yet has a dataconverter": " 未注册数据转换器，却存在数据转换器",
},
# ===== ConverterFlattenChunk.java =====
"ca/spottedleaf/dataconverter/minecraft/converters/chunk/ConverterFlattenChunk.java": {
    "ChunkNibbleArrays should be 2048 bytes not: ": "区块半字节数组应为 2048 字节，实际为：",
    "In chunk: {}x{} found a duplicate block entity at position (ConverterFlattenChunk): [{}, {}, {}]": "在区块：{}x{} 中发现重复的方块实体，位置 (ConverterFlattenChunk)：[{}, {}, {}]",
    "In chunk: {}x{} found an invalid chunk section y (ConverterFlattenChunk): {}": "在区块：{}x{} 中发现无效的区块段 y (ConverterFlattenChunk)：{}",
    "In chunk: {}x{} found a duplicate chunk section (ConverterFlattenChunk): {}": "在区块：{}x{} 中发现重复的区块段 (ConverterFlattenChunk)：{}",
},
# ===== ConverterEntityToVariant.java =====
"ca/spottedleaf/dataconverter/minecraft/converters/entity/ConverterEntityToVariant.java": {
    " cannot return null value!": " 不能返回空值！",
},
# ===== HelperBlockFlatteningV1450.java =====
"ca/spottedleaf/dataconverter/minecraft/converters/helpers/HelperBlockFlatteningV1450.java": {
    "Already contains mapping for ": "已存在映射：",
    "Exception parsing ": "解析时发生异常：",
    "Mapping already exists for id ": "映射已存在，id：",
    "Name does not exist for pre flattenings for id ": "扁平化前名称不存在，id：",
},
# ===== HelperItemNameV102.java =====
"ca/spottedleaf/dataconverter/minecraft/converters/helpers/HelperItemNameV102.java": {
    "Mapping already exists for ": "映射已存在：",
    ": prev: ": "：先前：",
    ", new: ": "，新：",
},
# ===== ConverterFlattenItemStack.java =====
"ca/spottedleaf/dataconverter/minecraft/converters/itemstack/ConverterFlattenItemStack.java": {
    "Item '": "物品 '",
    "' requires flattening but found no mapping for it! (ConverterFlattenItemStack)": "' 需要扁平化，但未找到对应映射！(ConverterFlattenItemStack)",
},
# ===== ConverterParticleToNBT.java =====
"ca/spottedleaf/dataconverter/minecraft/converters/particle/ConverterParticleToNBT.java": {
    "Failed to parse nbt: ": "解析 NBT 失败：",
    "Failed to parse block properties: ": "解析方块属性失败：",
    "Failed to parse dust particle: ": "解析尘埃粒子失败：",
    "Failed to parse color transition dust particle: ": "解析颜色渐变尘埃粒子失败：",
    "Failed to parse sculk particle: ": "解析幽匿粒子失败：",
    "Failed to parse vibration particle: ": "解析振动粒子失败：",
    "Failed to parse shriek particle: ": "解析尖啸粒子失败：",
},
# ===== MCTypeRegistry.java =====
"ca/spottedleaf/dataconverter/minecraft/datatypes/MCTypeRegistry.java": {
    "Initialising converters for DataConverter...": "正在初始化 DataConverter 转换器……",
    "Failed to register data converters": "注册数据转换器失败",
    "Finished initialising converters for DataConverter in ": "DataConverter 转换器初始化完成，耗时：",
},
# ===== V102.java =====
"ca/spottedleaf/dataconverter/minecraft/versions/V102.java": {
    "Unknown legacy integer id (V102) ": "未知的旧整数 id (V102)：",
},
# ===== V108.java =====
"ca/spottedleaf/dataconverter/minecraft/versions/V108.java": {
    "Failed to parse UUID for legacy entity (V108): ": "解析旧实体的 UUID 失败 (V108)：",
},
# ===== V1624.java =====
"ca/spottedleaf/dataconverter/minecraft/versions/V1624.java": {
    "Block Entity ({},{},{}) was expected to be a chest (V1624)": "方块实体 ({},{},{}) 应为箱子 (V1624)",
},
# V2523.java - SKIP (legacy attribute name map keys)
# V2701.java
"ca/spottedleaf/dataconverter/minecraft/versions/V2701.java": {
    "Missing path": "缺少路径",
},
# ===== V2832.java =====
"ca/spottedleaf/dataconverter/minecraft/versions/V2832.java": {
    "Expected size ": "期望大小 ",
    ", got: ": "，实际：",
    "Old data storage has values that cannot be moved into new palette (would erase data)!": "旧数据存储中存在无法移入新调色板的值（将丢失数据）！",
    "Failed to rewrite mismatched palette and data storage for section y: ": "重写不匹配的调色板与数据存储失败，区块段 y：",
    " for chunk [": "，区块 [",
    "], palette entries: ": "]，调色板条目：",
    ", data storage size: ": "，数据存储大小：",
},
# ===== V2833.java / V2852.java =====
"ca/spottedleaf/dataconverter/minecraft/versions/V2833.java": {
    "Unable load old custom worlds.": "无法加载旧的自定义世界。",
},
"ca/spottedleaf/dataconverter/minecraft/versions/V2852.java": {
    "Unable load old custom worlds.": "无法加载旧的自定义世界。",
},
# ===== V2970.java =====
"ca/spottedleaf/dataconverter/minecraft/versions/V2970.java": {
    "Encountered unknown structure in dataconverter: ": "数据转换器中遇到未知结构：",
    "Encountered unknown structure reference in dataconverter: ": "数据转换器中遇到未知结构引用：",
    "Duplicate biome remap: ": "重复的生物群系重映射：",
    ", but already mapped to ": "，但已映射到：",
},
# ===== V3447.java =====
"ca/spottedleaf/dataconverter/minecraft/versions/V3447.java": {
    "Duplicate target ": "重复的目标：",
},
# V3945.java - SKIP (legacy stats name map keys)
# V4061.java - SKIP (all NBT literal data)
# ===== V4290.java =====
"ca/spottedleaf/dataconverter/minecraft/versions/V4290.java": {
    "Legacy HoverEvent with action=show_item has invalid value, expected string: ": "旧 HoverEvent 的 action=show_item 值无效，应为字符串：",
    "Failed to parse SNBT for legacy item HoverEvent: ": "解析旧物品 HoverEvent 的 SNBT 失败：",
    "Legacy HoverEvent with action=show_entity has invalid value, expected string: ": "旧 HoverEvent 的 action=show_entity 值无效，应为字符串：",
    "Failed to parse SNBT for legacy entity HoverEvent: ": "解析旧实体 HoverEvent 的 SNBT 失败：",
    "Wrong type for text component: ": "文本组件类型错误：",
    "Unexpected byte[] output from JsonTypeUtil": "JsonTypeUtil 返回了意外的 byte[]",
    "Unexpected int[] output from JsonTypeUtil": "JsonTypeUtil 返回了意外的 int[]",
    "Unexpected long[] output from JsonTypeUtil": "JsonTypeUtil 返回了意外的 long[]",
    "Unknown nbt type: ": "未知的 NBT 类型：",
    "Failed to convert json to nbt: ": "JSON 转 NBT 失败：",
},
# ===== V704.java =====
"ca/spottedleaf/dataconverter/minecraft/versions/V704.java": {
    "Duplicate item id to tile key: ": "物品 id 与方块实体键重复：",
    "(V704) Failed to find walkers for ": "(V704) 未找到对应的遍历器：",
    "Unable to resolve Entity for ItemStack (V704): ": "无法解析物品栈对应的实体 (V704)：",
    "Unable to resolve BlockEntity for ItemStack (V704): ": "无法解析物品栈对应的方块实体 (V704)：",
},
# ===== V99.java =====
"ca/spottedleaf/dataconverter/minecraft/versions/V99.java": {
    "Unable to resolve Entity for ItemStack (V99): ": "无法解析物品栈对应的实体 (V99)：",
    "Unable to resolve BlockEntity for ItemStack (V99): ": "无法解析物品栈对应的方块实体 (V99)：",
},
# ===== JsonListType / JsonMapType =====
"ca/spottedleaf/dataconverter/types/json/JsonListType.java": {
    ", compressed=": "，压缩=",
},
"ca/spottedleaf/dataconverter/types/json/JsonMapType.java": {
    ", compressed=": "，压缩=",
},
# ===== JsonTypeUtil.java =====
"ca/spottedleaf/dataconverter/types/json/JsonTypeUtil.java": {
    "Unknown type: ": "未知类型：",
    "Unrecognized type ": "无法识别的类型：",
},
# ===== NBTTypeUtil.java =====
"ca/spottedleaf/dataconverter/types/nbt/NBTTypeUtil.java": {
    "Unknown type: ": "未知类型：",
    "Unknown tag: ": "未知标签：",
    "Unrecognized type ": "无法识别的类型：",
},
# ===== ConvertUtil.java =====
"ca/spottedleaf/dataconverter/util/ConvertUtil.java": {
    "Not in benchmark mode": "不在基准测试模式",
    "No benchmark data recorded.": "未记录基准测试数据。",
    "Benchmark data for ": "基准测试数据：",
    ": total: ": "：总计：",
    ": mean: ": "：平均：",
    ". median: ": "。中位数：",
    "Unknown type: ": "未知类型：",
},
# ===== NearbyPlayers.java =====
"ca/spottedleaf/moonrise/common/misc/NearbyPlayers.java": {
    "Already have player ": "已存在玩家：",
    "Don't have player ": "不存在玩家：",
    "Already contains player ": "已包含玩家：",
    "Does not contain player ": "不包含玩家：",
    "Chunk should exist at ": "区块应存在于：",
},
# ===== MoonriseRegionFileIO.java =====
"ca/spottedleaf/moonrise/patches/chunk_system/io/MoonriseRegionFileIO.java": {
    "Unknown controller type ": "未知的控制器类型：",
    "Result already exists for type ": "该类型的结果已存在：",
    "Result does not exist for type ": "该类型的结果不存在：",
    "Types cannot be null": "类型不能为 null",
    "Types cannot be empty": "类型不能为空",
    " synchronously failed to handle chunk data for task ": "同步处理区块数据失败，任务：",
    "Write completed concurrently, expected this task: ": "并发写入完成，预期任务：",
    ", report this!": "，请报告此问题！",
    "Chunk task mismatch, expected this task: ": "区块任务不匹配，预期任务：",
    ", got: ": "，实际：",
    "Failed to read chunk data for task: ": "读取区块数据失败，任务：",
    "Unknown state: ": "未知状态：",
    "Failed to decompress chunk data for task: ": "解压区块数据失败，任务：",
    "Should be writable": "应为可写状态",
    "Serialization task for chunk data failed: ": "区块数据序列化任务失败：",
    "Failed to write chunk data for task: ": "写入区块数据失败，任务：",
    "Task for world: '": "任务所属世界：'",
    "' at (": "'，位于 (",
    ") type: ": ")，类型：",
    ", hash: ": "，哈希：",
    " failed to handle chunk data (read) for task ": "处理区块数据（读）失败，任务：",
    " failed to handle chunk data (write) for task ": "处理区块数据（写）失败，任务：",
},
# ===== EntityDataController.java =====
"ca/spottedleaf/moonrise/patches/chunk_system/io/datacontroller/EntityDataController.java": {
    "Entity chunk coordinate and serialized data do not have matching coordinates, trying to serialize coordinate ": "实体区块坐标与序列化数据坐标不匹配，尝试序列化坐标：",
    " but compound says coordinate is ": "，但复合标签中的坐标为：",
},
# ===== ChunkEntitySlices.java =====
"ca/spottedleaf/moonrise/patches/chunk_system/level/entity/ChunkEntitySlices.java": {
    "Entity type ": "实体类型 ",
    " failed to serialize": " 序列化失败",
},
# ===== EntityLookup.java =====
"ca/spottedleaf/moonrise/patches/chunk_system/level/entity/EntityLookup.java": {
    "Length must be no greater-than the array length": "长度不能大于数组长度",
    "Entity status change must only happen on the main thread": "实体状态变更只能在主线程进行",
    "Cannot recursively update entity chunk status for entity ": "不能递归更新实体区块状态，实体：",
    "Cannot update chunk status for entity ": "无法更新实体的区块状态：",
    " since entity chunk (": "，因为实体区块 (",
    ") is receiving update": ") 正在接收更新",
    "Root entity ": "根实体 ",
    " is outside of serialized chunk ": " 在已序列化区块之外：",
    "Cannot add entity off-main thread": "不能在非主线程添加实体",
    "Refusing to add removed entity: ": "拒绝添加已移除的实体：",
    " is currently prevented from being added/removed to world since it is processing section status updates": " 当前被阻止添加/移除到世界，因为它正在处理区块段状态更新",
    "Entity id already exists: ": "实体 id 已存在：",
    ", mapped to ": "，映射到：",
    ", can't add ": "，无法添加：",
    "Entity uuid already exists: ": "实体 UUID 已存在：",
    " added to world '": " 已添加到世界 '",
    "', but was already contained in entity chunk (": "'，但已包含于实体区块 (",
    "Cannot remove entity off-main": "不能在非主线程移除实体",
    "Only call Entity#setRemoved to remove an entity": "只能通过 Entity#setRemoved 移除实体",
    "Cannot remove entity ": "无法移除实体：",
    " from null entity slices (": "，来自空实体切片 (",
    "Attempting to remove entity ": "尝试移除实体：",
    " from entity slices (": "，来自实体切片 (",
    ") that is receiving status updates": ")，而该切片正在接收状态更新",
    "Failed to remove entity ": "移除实体失败：",
    " from entity slices (": "，来自实体切片 (",
    " by id, current entity mapped: ": "，按 id，当前映射实体：",
    " by uuid, current entity mapped: ": "，按 uuid，当前映射实体：",
    "Cannot move entity off-main": "不能在非主线程移动实体",
    "Could not remove entity ": "无法移除实体：",
    " from its old chunk section (": "，来自其旧区块段 (",
    ") since it was not contained in the section": ")，因为它并不在该区块段中",
    "Could not add entity ": "无法添加实体：",
    " to its new chunk section (": "，到其新区切段 (",
    ") as it is already contained in the section": ")，因为它已在该区块段中",
    "Cannot load in entity section off-main": "不能在非主线程加载实体区块段",
    "Cannot unload entity section off-main": "不能在非主线程卸载实体区块段",
    "Cannot remove entity off-main": "不能在非主线程移除实体",
},
# ===== PoiChunk.java =====
"ca/spottedleaf/moonrise/patches/chunk_system/level/poi/PoiChunk.java": {
    "Incorrect length used, expected ": "使用了错误的长度，期望：",
    ", got ": "，实际：",
    "Loading in poi chunk off-main": "在非主线程加载 POI 区块",
    "chunkY is out of bounds, chunkY: ": "chunkY 越界，chunkY：",
    " outside [": "，超出范围 [",
    "Failed to serialize poi chunk for world: ": "为世界序列化 POI 区块失败：",
    ", chunk: (": "，区块：(",
    "); description: ": ")，描述：",
    "Failed to deserialize poi chunk for world: ": "为世界反序列化 POI 区块失败：",
},
# ===== RegionizedPlayerChunkLoader.java =====
"ca/spottedleaf/moonrise/patches/chunk_system/player/RegionizedPlayerChunkLoader.java": {
    "Cannot add player to player chunk loader async": "不能异步将玩家加入玩家区块加载器",
    "Player is already added to player chunk loader": "玩家已加入玩家区块加载器",
    "Cannot remove player from player chunk loader async": "不能异步从玩家区块加载器移除玩家",
    "Cannot tick player chunk loader async": "不能异步 tick 玩家区块加载器",
    "Ticking removed player chunk loader": "正在 tick 已移除的玩家区块加载器",
    "Previous state should be ": "先前状态应为：",
    ", not ": "，而不是：",
    "Cannot add player asynchronously": "不能异步添加玩家",
    "Adding removed player chunk loader": "正在添加已移除的玩家区块加载器",
    "Cannot update player asynchronously": "不能异步更新玩家",
    "Updating removed player chunk loader": "正在更新已移除的玩家区块加载器",
    "Unknown stage: ": "未知阶段：",
    "Removing removed player chunk loader": "正在移除已移除的玩家区块加载器",
},
# ===== ChunkHolderManager.java =====
"ca/spottedleaf/moonrise/patches/chunk_system/scheduling/ChunkHolderManager.java": {
    "Duplicate chunkholder in auto save queue": "自动保存队列中存在重复的区块持有者",
    "Closing world off-main": "在非主线程关闭世界",
    "Waiting 60s for chunk system to halt for world '": "等待 60 秒以停止区块系统，世界：'",
    "Failed to halt generation/loading tasks for world '": "停止世界的生成/加载任务失败：'",
    "Halted chunk system for world '": "已停止区块系统，世界：'",
    "Waiting 60s for chunk I/O to halt for world '": "等待 60 秒以停止区块 I/O，世界：'",
    "Failed to halt I/O tasks for world '": "停止世界的 I/O 任务失败：'",
    "Halted I/O scheduler for world '": "已停止 I/O 调度器，世界：'",
    "Failed to close '": "关闭失败：'",
    "' regionfile cache for world '": "' 区域文件缓存，世界：'",
    "Emergency saving all chunkholders for world '": "紧急保存所有区块持有者，世界：'",
    "Saving all chunkholders for world '": "正在保存所有区块持有者，世界：'",
    "Failed to save chunk (": "保存区块失败：(",
    ") in world '": ")，世界：'",
    " block chunks, ": " 个方块区块，",
    " entity chunks, ": " 个实体区块，",
    " poi chunks in world '": " 个 POI 区块，世界：'",
    "', progress: ": "'，进度：",
    "Exception when flushing regions in world '": "刷新世界区域时发生异常：'",
    "' in ": "'，耗时：",
    "Expected chunk holder to be created": "应已创建区块持有者",
    "Should have been able to add ": "应能够添加：",
    "Must hold ticket level update lock!": "必须持有工单等级更新锁！",
    "Must hold scheduler lock!!": "必须持有调度器锁！！",
    "Cannot create entity chunk off-main": "不能在非主线程创建实体区块",
    "Cannot create poi chunk off-main": "不能在非主线程创建 POI 区块",
    "Cannot unload chunks off-main": "不能在非主线程卸载区块",
    "Cannot unload chunks recursively": "不能递归卸载区块",
    " is not safe to unload but is inside the unload queue?": " 不安全卸载，却在卸载队列中？",
    "Cannot update ticket level while unloading chunks or updating entity manager": "在卸载区块或更新实体管理器时不能更新工单等级",
    "Cannot asynchronously process ticket updates": "不能异步处理工单更新",
},
# ===== ChunkTaskScheduler.java =====
"ca/spottedleaf/moonrise/patches/chunk_system/scheduling/ChunkTaskScheduler.java": {
    "Chunk system error at chunk (": "区块系统错误，区块 (",
    "), holder: ": ")，持有者：",
    ", exception:": "，异常：",
    "Chunk system error": "区块系统错误",
    "Chunk system details": "区块系统详情",
    "Chunk coordinate": "区块坐标",
    "unrecoverableChunkSystemFailure caller thread": "unrecoverableChunkSystemFailure 调用线程",
    "Chunk System Objects of Interest": "区块系统相关对象",
    "Chunk system crash propagated from unrecoverableChunkSystemFailure": "区块系统崩溃由 unrecoverableChunkSystemFailure 传播而来",
    "Cannot execute main thread task off-main": "不能在非主线程执行主线程任务",
    "Cannot schedule chunk load during ticket level update": "工单等级更新期间不能调度区块加载",
    "Cannot schedule chunk loading recursively": "不能递归调度区块加载",
    "Cannot wait for INACCESSIBLE status": "不能等待 INACCESSIBLE 状态",
    "Failed to process chunk full status callback": "处理区块完整状态回调失败",
    "Chunk system has shut down, cannot process chunk requests in world '": "区块系统已关闭，无法处理世界中的区块请求：'",
    "' at ": "'，位于：",
    ") status: ": ")，状态：",
    "Expected chunk to be loaded for status ": "区块应已加载以达到状态：",
    "Failed to process chunk status callback": "处理区块状态回调失败",
    "Not holding scheduling lock": "未持有调度锁",
    "Missing chunkholder when required": "需要时缺少区块持有者",
    ") in '": ")，位于 '",
    "Chunk wait task info below: ": "区块等待任务信息如下：",
    "Chunk wait: ": "区块等待：",
    "Chunk holder: ": "区块持有者：",
    "Writing chunk information dump to ": "正在将区块信息转储写入：",
    "Successfully written chunk information!": "区块信息写入成功！",
    "Failed to dump chunk information to file ": "将区块信息转储到文件失败：",
},
# ===== NewChunkHolder.java =====
"ca/spottedleaf/moonrise/patches/chunk_system/scheduling/NewChunkHolder.java": {
    "Cannot sync load entity data off-main": "不能在非主线程同步加载实体数据",
    "Must load entity data from disk before loading in the entity chunk!": "加载实体区块前必须先从磁盘加载实体数据！",
    "Unhandled entity data load exception, data data will be lost: ": "未处理的实体数据加载异常，数据将丢失：",
    "Cannot load entity data, it is already loaded": "无法加载实体数据，它已被加载",
    "Must hold scheduling lock": "必须持有调度锁",
    "Unhandled poi load exception, poi data will be lost: ": "未处理的 POI 加载异常，POI 数据将丢失：",
    "Cannot load poi data, it is already loaded": "无法加载 POI 数据，它已被加载",
    "Double calling schedule()": "重复调用 schedule()",
    "May not be completed here": "不能在此处完成",
    "Cannot be uncompleted at this point": "此时不能取消完成",
    "Result cannot be null (cancelled)": "结果不能为 null（已取消）",
    "Neighbours using this chunk cannot be negative": "使用此区块的邻居数不能为负数",
    "Unknown regionfile type ": "未知的区域文件类型：",
    "Corrupt state": "状态损坏",
    "Cannot update full status thread off-main": "不能在非主线程更新完整状态线程",
    "toStatus cannot be null": "toStatus 不能为 null",
    "Failed to process chunk status callback": "处理区块状态回调失败",
    "Cannot have neighbours blocking this gen task": "不能让邻居阻塞此生成任务",
    "Neighbour is not waiting for us?": "邻居并未在等待我们？",
    "Currently generating or provided task is trying to generate to a level we are already at!": "正在生成，或提供的任务试图生成到我们已处于的等级！",
    "Cannot schedule generation task when not requested": "未被请求时不能调度生成任务",
    "Cannot complete generation task '": "无法完成生成任务：'",
    "' because we are waiting on '": "'，因为我们正在等待：'",
    "' instead!": "'！",
    "Ignoring exception for ": "忽略异常：",
    "Generation task": "生成任务",
    "Task to status": "任务目标状态",
    "Cannot save data off-main": "不能在非主线程保存数据",
    "Failed to save chunk data (": "保存区块数据失败：(",
    ") in world '": ")，世界：'",
    "Cannot merge transient entities for chunk (": "无法为区块合并临时实体：(",
    "', data on disk will be replaced": "'，磁盘上的数据将被替换",
    "Failed to save entity data (": "保存实体数据失败：(",
    "Failed to save poi data (": "保存 POI 数据失败：(",
    ", chunkX=": "，chunkX=",
    ", chunkZ=": "，chunkZ=",
    ", entityChunkFromDisk=": "，entityChunkFromDisk=",
    ", lastChunkCompletion={chunk_class=": "，lastChunkCompletion={chunk_class=",
    ", currentGenStatus=": "，currentGenStatus=",
    ", requestedGenStatus=": "，requestedGenStatus=",
    ", generationTask=": "，generationTask=",
    ", generationTaskStatus=": "，generationTaskStatus=",
    ", priority=": "，priority=",
    ", priorityLocked=": "，priorityLocked=",
    ", neighbourRequestedPriority=": "，neighbourRequestedPriority=",
    ", effective_priority=": "，effective_priority=",
    ", oldTicketLevel=": "，oldTicketLevel=",
    ", currentTicketLevel=": "，currentTicketLevel=",
    ", totalNeighboursUsingThisChunk=": "，totalNeighboursUsingThisChunk=",
    ", fullNeighbourChunksLoadedBitset=": "，fullNeighbourChunksLoadedBitset=",
    ", currentChunkStatus=": "，currentChunkStatus=",
    ", pendingChunkStatus=": "，pendingChunkStatus=",
    ", is_unload_safe=": "，is_unload_safe=",
    ", killed=": "，killed=",
},
# ===== PriorityHolder.java =====
"ca/spottedleaf/moonrise/patches/chunk_system/scheduling/PriorityHolder.java": {
    "Invalid priority ": "无效的优先级：",
    "schedule() called twice": "schedule() 被调用了两次",
},
# ===== ThreadedTicketLevelPropagator.java =====
"ca/spottedleaf/moonrise/patches/chunk_system/scheduling/ThreadedTicketLevelPropagator.java": {
    "Race condition while creating new section": "创建新区段时发生竞态条件",
    "levels x=": "levels x=",
    "sources x=": "sources x=",
    "Adjust COORDINATE_BITS": "请调整 COORDINATE_BITS",
    "Section at ": "区段位于 ",
    " should not be null": " 不应为 null",
},
# ===== ChunkFullTask.java =====
"ca/spottedleaf/moonrise/patches/chunk_system/scheduling/task/ChunkFullTask.java": {
    "Expected poi chunk to be loaded with chunk for task ": "POI 区块应随任务区块一同加载：",
    "Cannot double call schedule()": "不能重复调用 schedule()",
    "Invalid priority ": "无效的优先级：",
},
# ===== ChunkLightTask.java =====
"ca/spottedleaf/moonrise/patches/chunk_system/scheduling/task/ChunkLightTask.java": {
    "Failed to light chunk ": "光照区块失败：",
    " in world '": "，世界：'",
},
# ===== ChunkLoadTask.java =====
"ca/spottedleaf/moonrise/patches/chunk_system/scheduling/task/ChunkLoadTask.java": {
    "Called tryCompleteLoad() too many times": "tryCompleteLoad() 被调用次数过多",
    "schedule() called twice": "schedule() 被调用了两次",
    "Completed throwable": "完成时抛出的异常",
    "CallbackDataLoadTask impl": "CallbackDataLoadTask 实现",
    "Already completed": "已完成",
    "Failed to load chunk data for task: ": "为任务加载区块数据失败：",
    ", chunk data will be lost": "，区块数据将丢失",
    "Deserialized chunk for task: ": "为任务反序列化区块：",
    " produced null, chunk data will be lost?": " 产生了 null，区块数据将丢失？",
    "Failed to parse chunk data for task: ": "为任务解析区块数据失败：",
    "Failed to load poi data for task: ": "为任务加载 POI 数据失败：",
    ", poi data will be lost": "，POI 数据将丢失",
    "Failed to run parse poi data for task: ": "为任务运行 POI 数据解析失败：",
    "Failed to load entity data for task: ": "为任务加载实体数据失败：",
    ", entity data will be lost": "，实体数据将丢失",
    "Failed to run converters for entity data for task: ": "为任务运行实体数据转换器失败：",
},
# ===== ChunkProgressionTask.java =====
"ca/spottedleaf/moonrise/patches/chunk_system/scheduling/task/ChunkProgressionTask.java": {
    "Completed throwable": "完成时抛出的异常",
    "Already completed": "已完成",
    ", for world: ": "，世界：",
    ", chunk: (": "，区块：(",
    "), hashcode: ": ")，哈希码：",
    ", priority: ": "，优先级：",
    ", status: ": "，状态：",
    ", scheduled: ": "，已调度：",
},
# ===== ChunkUpgradeGenericStatusTask.java =====
"ca/spottedleaf/moonrise/patches/chunk_system/scheduling/task/ChunkUpgradeGenericStatusTask.java": {
    "Invalid priority ": "无效的优先级：",
    "Infinite write radius is not supported": "不支持无限写入半径",
    "Target status": "目标状态",
    "From status": "来源状态",
    "Generation task": "生成任务",
    "Failed to complete status for chunk: status:": "为区块完成状态失败，状态：",
    ", chunk: (": "，区块：(",
    "), world: ": ")，世界：",
    "Future status not complete after scheduling: ": "调度后未来状态仍未完成：",
    ", generate: ": "，生成：",
    "Chunk for status: ": "对应状态的区块：",
    ", generation: ": "，生成：",
    " should not be null! Future: ": " 不应为 null！Future：",
    "Cannot double call schedule()": "不能重复调用 schedule()",
},
# ===== GenericDataLoadTask.java =====
"ca/spottedleaf/moonrise/patches/chunk_system/scheduling/task/GenericDataLoadTask.java": {
    "Illegal class implementation: ": "非法的类实现：",
    ", should be able to schedule at least one task!": "，应至少能调度一个任务！",
    ", world: ": "，世界：",
    ", chunk: (": "，区块：(",
    "), hashcode: ": ")，哈希码：",
    ", priority: ": "，优先级：",
    ", type: ": "，类型：",
    "Reference count cannot be zero here": "此处引用计数不能为零",
    "Data callback says cancelled, but stage does not?": "数据回调显示已取消，但阶段并非如此？",
    "Failed I/O callback for task: ": "任务的 I/O 回调失败：",
    "Callback throwable": "回调抛出的异常",
    "Regionfile type": "区域文件类型",
    "schedule() called twice": "schedule() 被调用了两次",
},
# ===== TicketSet.java =====
"ca/spottedleaf/moonrise/patches/chunk_system/util/stream/TicketSet.java": {
    "Cannot service more than Integer.MAX_VALUE elements!": "处理的元素不能超过 Integer.MAX_VALUE！",
},
# ===== CollisionUtil.java =====
"ca/spottedleaf/moonrise/patches/collisions/CollisionUtil.java": {
    "Unknown axis: ": "未知轴：",
    "Slice shape mismatch": "切片形状不匹配",
    "Ambiguous operator: (false, false) -> true": "运算符有歧义：(false, false) -> true",
    "size x: ": "size x：",
    "size y: ": "size y：",
    "size z: ": "size z：",
    "): shape1: ": ")：shape1：",
    ", shape2: ": "，shape2：",
},
# ===== SWMRNibbleArray.java =====
"ca/spottedleaf/moonrise/patches/starlight/light/SWMRNibbleArray.java": {
    "Data of wrong length: ": "数据长度错误：",
    "Data cannot be null and have state be initialised": "数据不能为 null 而状态却已初始化",
},
# ===== StarLightEngine.java =====
"ca/spottedleaf/moonrise/patches/starlight/light/StarLightEngine.java": {
    "Trying to propagate light update before 1 radius neighbours ready": "在 1 格半径邻居就绪前尝试传播光照更新",
},
# ===== SaveUtil.java =====
"ca/spottedleaf/moonrise/patches/starlight/util/SaveUtil.java": {
    "Failed to inject light data into save data for chunk ": "为区块注入光照数据到存档失败：",
    ", chunk light will be recalculated on its next load": "，区块光照将在下次加载时重新计算",
    "Failed to load light for chunk ": "为区块加载光照失败：",
    ", light will be recalculated": "，光照将重新计算",
},
# ===== net/minecraft/commands/Commands.java =====
"net/minecraft/commands/Commands.java": {
    "Cannot perform command async": "不能异步执行命令",
    "Command exception: /{}": "命令异常：/{}",
    "'/{}' threw an exception": "'/{}' 抛出了异常",
    "Ambiguity between arguments {} and {} with inputs: {}": "参数 {} 与 {} 之间存在歧义，输入：{}",
    "Missing type registration for following arguments:\\n {}": "以下参数缺少类型注册：\\n {}",
    "Unregistered argument types": "未注册的参数类型",
    # thread pool name skipped
},
# ComponentArgument / MessageArgument / StyleArgument - SKIP (command syntax examples)
# ===== NbtPathArgument.java =====
"net/minecraft/commands/arguments/NbtPathArgument.java": {
    "Failed to parse path ": "解析路径失败：",
},
# ===== ItemParser.java =====
"net/minecraft/commands/arguments/item/ItemParser.java": {
    "Parser gave no item": "解析器未给出物品",
},
# ===== EntitySelector.java =====
"net/minecraft/commands/arguments/selector/EntitySelector.java": {
    "Invalid selector component": "无效的选择器组件",
},
# ===== CustomCommandExecutor / CustomModifierExecutor =====
"net/minecraft/commands/execution/CustomCommandExecutor.java": {
    "This function should not run": "此函数不应被执行",
},
"net/minecraft/commands/execution/CustomModifierExecutor.java": {
    "This function should not run": "此函数不应被执行",
},
# ===== ExecutionContext.java =====
"net/minecraft/commands/execution/ExecutionContext.java": {
    "Command execution stopped due to limit (executed {} commands)": "命令执行因达到上限而停止（已执行 {} 条命令）",
    "Command execution stopped due to command queue overflow (max {})": "命令执行因命令队列溢出而停止（上限 {}）",
},
# ===== CommandFunction.java =====
"net/minecraft/commands/functions/CommandFunction.java": {
    "Line continuation at end of file": "文件末尾存在行续接符",
    "Unknown or invalid command '": "未知或无效的命令：'",
    "' on line ": "'，位于第 ",
    " (if you intended to make a comment, use '#' not '//')": "（如果你想写注释，请使用 '#' 而不是 '//'）",
    " (did you mean '": "（你是否想输入 '",
    "'? Do not use a preceding forwards slash.)": "'？请勿在前面加斜杠。）",
    "Whilst parsing command on line ": "解析命令时出错，第 ",
    "Command too long: ": "命令过长：",
    " characters, contents: ": " 个字符，内容：",
},
# ===== FunctionBuilder.java =====
"net/minecraft/commands/functions/FunctionBuilder.java": {
    "Can't parse function line ": "无法解析函数行：",
},
# ===== StringTemplate.java =====
"net/minecraft/commands/functions/StringTemplate.java": {
    "Unterminated macro variable": "未闭合的宏变量",
    "Invalid macro variable name '": "无效的宏变量名：'",
    "No variables in macro": "宏中没有变量",
},
# ===== ArgumentTypeInfos.java =====
"net/minecraft/commands/synchronization/ArgumentTypeInfos.java": {
    "Unrecognized argument type %s (%s)": "无法识别的参数类型 %s（%s）",
},
# ===== ArgumentUtils.java =====
"net/minecraft/commands/synchronization/ArgumentUtils.java": {
    "Could not serialize node {} ({})!": "无法序列化节点 {}（{}）！",
    "Failed to serialize requirement: ": "序列化需求失败：",
},
# ===== SuggestionProviders.java =====
"net/minecraft/commands/synchronization/SuggestionProviders.java": {
    "A command suggestion provider is already registered with the name '": "命令建议提供器已注册，名称为：'",
},
# ===== CompressionDecoder.java =====
"net/minecraft/network/CompressionDecoder.java": {
    "Badly compressed packet - size of ": "压缩包异常 - 大小：",
    " is below server threshold of ": " 低于服务端阈值：",
    " is larger than protocol maximum of 8388608": " 超过协议最大值 8388608",
    "Badly compressed packet - actual length of uncompressed payload ": "压缩包异常 - 解压后实际负载长度：",
    " is does not match declared size ": " 与声明的大小不匹配：",
},
# ===== CompressionEncoder.java =====
"net/minecraft/network/CompressionEncoder.java": {
    "Packet too big (is ": "数据包过大（实际为 ",
    ", should be less than 8388608)": "，应小于 8388608）",
},
# ===== Connection.java =====
"net/minecraft/network/Connection.java": {
    "Skipping packet due to errors": "因错误跳过数据包",
    "Internal Exception: ": "内部异常：",
    "Failed to sent packet": "发送数据包失败",
    "Double fault": "双重故障",
    "Received a packet before the packet listener was initialized": "在数据包监听器初始化之前收到了数据包",
    "{} kicked for packet spamming: {}": "{} 因刷屏数据包被踢出：{}",
    "Received {} that couldn't be processed": "收到无法处理的数据包 {}：",
    "Trying to set listener for wrong side: connection is ": "试图为错误的一侧设置监听器：连接为 ",
    ", but listener is ": "，但监听器为 ",
    "Listener protocol (": "监听器协议 (",
    ") does not match requested one ": ") 与请求的协议不匹配：",
    "Connection closed during protocol change": "协议切换期间连接已关闭",
    "Invalid inbound protocol: ": "无效的入站协议：",
    "Invalid outbound protocol: ": "无效的出站协议：",
    "Listener already set": "监听器已设置",
    "Invalid initial listener": "无效的初始监听器",
    "Mismatched initial protocols": "初始协议不匹配",
    "NetworkException: {}": "NetworkException：{}",
    "IP hidden": "IP 已隐藏",
},
# ===== FriendlyByteBuf.java =====
"net/minecraft/network/FriendlyByteBuf.java": {
    "Failed to decode: ": "解码失败：",
    "Failed to encode: ": "编码失败：",
    "Failed to decode JSON: ": "解码 JSON 失败：",
    " is larger than limit ": " 超过限制：",
    "ByteArray with size ": "ByteArray 大小为 ",
    " is bigger than allowed ": "，超过允许上限：",
    "VarIntArray with size ": "VarIntArray 大小为 ",
    "LongArray with size ": "LongArray 大小为 ",
    "Not a compound tag: ": "不是复合标签：",
    "Malformed public key bytes": "公钥字节格式错误",
    "BitSet is larger than expected size (": "BitSet 大于预期大小（",
},
# ===== PacketBundlePacker.java =====
"net/minecraft/network/PacketBundlePacker.java": {
    "Terminal message received in bundle": "在数据包束中收到终止消息",
},
# ===== PacketDecoder.java =====
"net/minecraft/network/PacketDecoder.java": {
    ") was larger than I expected, found ": ") 比预期大，多出：",
    " bytes extra whilst reading packet ": " 个额外字节，读取数据包时：",
    " IN: [{}:{}] {} -> {} bytes": " IN: [{}:{}] {} -> {} 字节",
},
# ===== PacketEncoder.java =====
"net/minecraft/network/PacketEncoder.java": {
    "OUT: [{}:{}] {} -> {} bytes": "OUT: [{}:{}] {} -> {} 字节",
    "Error sending packet {}": "发送数据包 {} 时出错",
    "PacketTooLarge - ": "PacketTooLarge - ",
    ". Max is ": "。最大值为：",
},
# ===== PacketProcessor.java =====
"net/minecraft/network/PacketProcessor.java": {
    "Server already shutting down": "服务端正在关闭",
    "Ignoring packet due to disconnection: {}": "因断开连接而忽略数据包：{}",
},
# ===== PacketSendListener.java =====
"net/minecraft/network/PacketSendListener.java": {
    "Failed to deliver packet, sending fallback {}": "数据包投递失败，发送回退包 {}",
},
# ===== RateKickingConnection.java =====
"net/minecraft/network/RateKickingConnection.java": {
    "Player exceeded rate-limit (sent {} packets per second)": "玩家超出速率限制（每秒发送 {} 个数据包）",
},
# ===== UnconfiguredPipelineHandler.java =====
"net/minecraft/network/UnconfiguredPipelineHandler.java": {
    "Pipeline has no inbound protocol configured, can't process packet ": "管道未配置入站协议，无法处理数据包：",
    "Pipeline has no outbound protocol configured, can't process packet ": "管道未配置出站协议，无法处理数据包：",
},
# ===== Utf8String.java =====
"net/minecraft/network/Utf8String.java": {
    "The received encoded string buffer length is longer than maximum allowed (": "接收到的编码字符串缓冲区长度超过最大允许值（",
    "The received encoded string buffer length is less than zero! Weird string!": "接收到的编码字符串缓冲区长度小于零！字符串异常！",
    "Not enough bytes in buffer, expected ": "缓冲区字节不足，期望：",
    ", but got ": "，实际：",
    "The received string length is longer than maximum allowed (": "接收到的字符串长度超过最大允许值（",
    "String too big (was ": "字符串过大（实际 ",
    " characters, max ": " 个字符，最大：",
    " bytes encoded, max ": " 字节编码，最大：",
},
# ===== VarInt / VarLong =====
"net/minecraft/network/VarInt.java": {
    "VarInt too big": "VarInt 过大",
},
"net/minecraft/network/VarLong.java": {
    "VarLong too big": "VarLong 过大",
},
# ===== Varint21FrameDecoder.java =====
"net/minecraft/network/Varint21FrameDecoder.java": {
    "length wider than 21-bit": "长度超过 21 位",
    "Frame length cannot be zero": "帧长度不能为零",
},
# ===== Varint21LengthFieldPrepender.java =====
"net/minecraft/network/Varint21LengthFieldPrepender.java": {
    "Packet too large: size ": "数据包过大，大小：",
    " is over 8": " 超过 8",
},
# ===== ChatDecorator.java =====
"net/minecraft/network/chat/ChatDecorator.java": {
    "Must override this implementation": "必须重写此实现",
},
# ===== ClickEvent.java =====
"net/minecraft/network/chat/ClickEvent.java": {
    "Click event type not allowed: ": "不允许的点击事件类型：",
},
# ===== ComponentSerialization.java =====
"net/minecraft/network/chat/ComponentSerialization.java": {
    "Failed to decode: ": "解码失败：",
    "Failed to encode: ": "编码失败：",
    "Component was too large: greater than max size ": "组件过大：超过最大大小 ",
    "No matching codec found": "未找到匹配的编解码器",
},
# ===== FontDescription.java =====
"net/minecraft/network/chat/FontDescription.java": {
    "Unsupported font description type: ": "不支持的字体描述类型：",
},
# ===== HoverEvent.java =====
"net/minecraft/network/chat/HoverEvent.java": {
    "Action not allowed: ": "不允许的操作：",
},
# ===== LastSeenMessagesValidator.java =====
"net/minecraft/network/chat/LastSeenMessagesValidator.java": {
    "Advanced last seen window by ": "提前了最后已读窗口 ",
    " messages, but expected at most ": " 条消息，但最多允许 ",
    "Last seen update contained ": "最后已读更新包含 ",
    " messages, but maximum window size is ": " 条消息，但窗口最大大小为 ",
    "Last seen update acknowledged unknown or previously ignored message at index ": "最后已读更新确认了未知或先前已忽略的消息，索引：",
    "Last seen update ignored previously acknowledged message at index ": "最后已读更新忽略了先前已确认的消息，索引：",
    " and signature ": "，签名：",
    "Checksum mismatch on last seen update: the client and server must have desynced": "最后已读更新的校验和不匹配：客户端与服务端可能已失步",
},
# ===== MessageSignature.java =====
"net/minecraft/network/chat/MessageSignature.java": {
    "Invalid message signature size": "消息签名大小无效",
    "<no signature>": "<无签名>",
},
# ===== PlayerChatMessage.java =====
"net/minecraft/network/chat/PlayerChatMessage.java": {
    ", message #": "，消息 #",
},
# ===== SignedMessageChain.java =====
"net/minecraft/network/chat/SignedMessageChain.java": {
    "Received expired chat: '{}'. Is the client/server system time unsynchronized?": "收到过期聊天消息：'{}'。客户端/服务端系统时间是否未同步？",
},
# ===== SignedMessageValidator.java =====
"net/minecraft/network/chat/SignedMessageValidator.java": {
    "Received chat message from {}, but they have no chat session initialized and secure chat is enforced": "收到来自 {} 的聊天消息，但其未初始化聊天会话，且已强制安全聊天",
    "Received out-of-order chat message from {}: expected index > {} for session {}, but was {} for session {}": "收到来自 {} 的乱序聊天消息：会话 {} 期望索引 > {}，但会话 {} 为 {}",
    "Received message with expired profile public key from {} with session {}": "收到来自 {} 的消息，其 profile 公钥已过期，会话 {}",
    "Received message with invalid signature (is the session wrong, or signature cache out of sync?): {}": "收到签名无效的消息（会话错误，还是签名缓存失步？）：{}",
},
# ===== TextColor.java =====
"net/minecraft/network/chat/TextColor.java": {
    "Color value out of range: ": "颜色值超出范围：",
    "Invalid color value: ": "无效的颜色值：",
    "Invalid color name: ": "无效的颜色名称：",
},
# ===== NbtContents.java =====
"net/minecraft/network/chat/contents/NbtContents.java": {
    "Invalid NBT path: ": "无效的 NBT 路径：",
    "'interpret' and 'plain' flags can't be both on": "'interpret' 与 'plain' 标志不能同时开启",
    "Failed to parse component: {}": "解析组件失败：{}",
},
# ScoreContents - toString debug, skip structural
# ===== TranslatableContents.java =====
"net/minecraft/network/chat/contents/TranslatableContents.java": {
    "This value needs to be parsed as component": "此值需要解析为组件",
    "Unsupported format: '": "不支持的格式：'",
    "Too long": "过长",
    ", fallback='": "，fallback='",
    ", args=": "，args=",
},
# ===== TranslatableFormatException.java =====
"net/minecraft/network/chat/contents/TranslatableFormatException.java": {
    "Error parsing: %s: %s": "解析错误：%s：%s",
    "Invalid index %d requested for %s": "为 %s 请求了无效索引 %d",
    "Error while parsing: %s": "解析时出错：%s",
},
# ===== BlockDataSource.java =====
"net/minecraft/network/chat/contents/data/BlockDataSource.java": {
    "Invalid coordinates path: ": "无效的坐标路径：",
},
# ===== PlayerSprite.java =====
"net/minecraft/network/chat/contents/objects/PlayerSprite.java": {
    "[unknown player head]": "[未知玩家头颅]",
},
# ===== ByteBufCodecs.java =====
"net/minecraft/network/codec/ByteBufCodecs.java": {
    "Expected non-null compound tag": "期望非空复合标签",
    "Not a compound tag: ": "不是复合标签：",
    "Failed to decode: ": "解码失败：",
    "Failed to encode: ": "编码失败：",
    "Too deep": "过深",
    " elements exceeded max size of: ": " 个元素，超过最大大小：",
    "Buffer size ": "缓冲区大小 ",
    " is larger than allowed limit of ": " 超过允许限制：",
    " is  larger than allowed limit of ": " 超过允许限制：",
    "Failed to parse JSON": "解析 JSON 失败",
},
# ===== IdDispatchCodec.java =====
"net/minecraft/network/codec/IdDispatchCodec.java": {
    "Failed to decode packet '": "解码数据包失败：'",
    "Received unknown packet id ": "收到未知数据包 id：",
    "Sending unknown packet '": "正在发送未知数据包：'",
    "Failed to encode packet '": "编码数据包失败：'",
    "Duplicate registration for type ": "类型重复注册：",
},
# ===== StreamCodec.java =====
"net/minecraft/network/codec/StreamCodec.java": {
    "Can't encode '": "无法编码：'",
    "', expected '": "'，期望：'",
},
# ===== BundleDelimiterPacket.java =====
"net/minecraft/network/protocol/BundleDelimiterPacket.java": {
    "This packet should be handled by pipeline": "此数据包应由管道处理",
},
# ===== BundlerInfo.java =====
"net/minecraft/network/protocol/BundlerInfo.java": {
    "Too many packets in a bundle": "数据包束中的数据包过多",
},
# ===== PacketUtils.java =====
"net/minecraft/network/protocol/PacketUtils.java": {
    "Main thread packet handler": "主线程数据包处理器",
    "Incoming Packet": "入站数据包",
    "Is Terminal": "是否为终止包",
    "Is Skippable": "是否可跳过",
},
# ===== ProtocolCodecBuilder.java =====
"net/minecraft/network/protocol/ProtocolCodecBuilder.java": {
    "Invalid packet flow for packet ": "数据包的数据包流向无效：",
    ", expected ": "，期望：",
},
# ===== ClientboundResourcePackPushPacket.java =====
"net/minecraft/network/protocol/common/ClientboundResourcePackPushPacket.java": {
    "Hash is too long (max 40, was ": "哈希过长（最大 40，实际为 ",
},
# ===== DiscardedPayload.java =====
"net/minecraft/network/protocol/common/custom/DiscardedPayload.java": {
    "Payload may not be larger than ": "负载不能大于：",
},
# ===== ClientboundChunksBiomesPacket.java =====
"net/minecraft/network/protocol/game/ClientboundChunksBiomesPacket.java": {
    "Didn't fill biome buffer: expected ": "未填满生物群系缓冲区，期望：",
    " bytes, got ": " 字节，实际：",
},
# ===== ClientboundCommandsPacket.java =====
"net/minecraft/network/protocol/game/ClientboundCommandsPacket.java": {
    "Server sent an impossible command tree": "服务端发送了不可能的命令树",
    "Unknown node type ": "未知节点类型：",
},
# ===== ClientboundLevelChunkPacketData.java =====
"net/minecraft/network/protocol/game/ClientboundLevelChunkPacketData.java": {
    "Chunk Packet trying to allocate too much memory on read.": "区块数据包在读取时尝试分配过多内存。",
    "Didn't fill chunk buffer: expected ": "未填满区块缓冲区，期望：",
    " bytes, got ": " 字节，实际：",
},
# ===== ClientboundSetPlayerTeamPacket.java =====
"net/minecraft/network/protocol/game/ClientboundSetPlayerTeamPacket.java": {
    "Parameters not present, but method is": "参数不存在，但方法为",
},
# ===== GameProtocols.java =====
"net/minecraft/network/protocol/game/GameProtocols.java": {
    "Not in creative mode": "不在创造模式",
},
# ===== ServerPacketListener.java =====
"net/minecraft/network/protocol/game/ServerPacketListener.java": {
    "Failed to handle packet {}, suppressing error": "处理数据包 {} 失败，已忽略错误",
},
# ===== ServerboundSelectBundleItemPacket.java =====
"net/minecraft/network/protocol/game/ServerboundSelectBundleItemPacket.java": {
    "Invalid selectedItemIndex: ": "无效的 selectedItemIndex：",
},
# ===== ClientIntent.java =====
"net/minecraft/network/protocol/handshake/ClientIntent.java": {
    "Unknown connection intent: ": "未知的连接意图：",
},
# ===== ClientboundCustomQueryPacket.java =====
"net/minecraft/network/protocol/login/ClientboundCustomQueryPacket.java": {
    "Payload may not be larger than 1048576 bytes": "负载不能大于 1048576 字节",
},
# ===== ServerboundCustomQueryAnswerPacket.java =====
"net/minecraft/network/protocol/login/ServerboundCustomQueryAnswerPacket.java": {
    "Payload may not be larger than ": "负载不能大于：",
    "Payload may not be larger than 1048576 bytes": "负载不能大于 1048576 字节",
},
# ===== ServerStatus.java =====
"net/minecraft/network/protocol/status/ServerStatus.java": {
    "Unknown format": "未知格式",
    "Malformed base64 server icon": "base64 服务端图标格式错误",
},
# ===== EntityDataAccessor.java =====
"net/minecraft/network/syncher/EntityDataAccessor.java": {
    "<entity data: ": "<实体数据：",
},
# ===== SynchedEntityData.java =====
"net/minecraft/network/syncher/SynchedEntityData.java": {
    "defineId called for: {} from {}": "defineId 被调用：{} 来自 {}",
    "Data value id is too big with ": "数据值 id 过大：",
    "! (Max is 254)": "！（最大 254）",
    "Invalid entity data item type for field %d on entity %s: old=%s(%s), new=%s(%s)": "实体 %s 的字段 %d 实体数据项类型无效：old=%s(%s)，new=%s(%s)",
    "! (Max is ": "！（最大 ",
    "Duplicate id value for ": "id 值重复：",
    "Unregistered serializer ": "未注册的序列化器：",
    " has not defined synched data value ": " 尚未定义已同步数据值：",
    "Unknown serializer type ": "未知的序列化器类型：",
},
}

def main():
    modified = 0
    translated_count = 0
    skipped = 0
    failed = []
    for rel, mapping in T.items():
        abs_path = os.path.join(BASE, rel.replace('/', os.sep))
        if not os.path.isfile(abs_path):
            print(f"NOT FOUND: {rel}")
            skipped += 1
            continue
        stdin_data = json.dumps(mapping, ensure_ascii=False)
        proc = subprocess.run(
            [sys.executable, TRANSLATOR, "apply", abs_path],
            input=stdin_data, capture_output=True, text=True, encoding='utf-8', timeout=60
        )
        if proc.returncode != 0:
            print(f"FAILED: {rel}")
            print(proc.stderr)
            failed.append(rel)
            continue
        print(f"OK: {rel} -> {proc.stdout.strip()}")
        modified += 1
        translated_count += len(mapping)
    print(f"\n=== SUMMARY ===")
    print(f"Files modified: {modified}")
    print(f"Translation entries applied (approx): {translated_count}")
    print(f"Failed: {len(failed)}")
    for f in failed:
        print(f"  - {f}")

if __name__ == '__main__':
    main()
