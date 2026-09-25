#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply hand-reviewed translations per file, using file_translator's own
exact-position replacement + verification. No bulk regex."""
import sys, os, json

sys.path.insert(0, r"E:\编程\项目\Paper-main\.mc_translation")
import file_translator as ft

BASE = r"E:\编程\项目\Paper-main\paper-server\src\minecraft\java"

# rel_path -> {original_literal: translation}
T = {
 "net/minecraft/world/level/block/Block.java": {
   "Block classes should end with Block and {} doesn't.": "方块类应以 Block 结尾，但 {} 不符合。",
 },
 "net/minecraft/world/level/block/CandleCakeBlock.java": {
   "Expected block to be of ": "期望方块为 ",
 },
 "net/minecraft/world/level/block/CommandBlock.java": {
   "Command Block chain tried to execute more than {} steps!": "命令方块链尝试执行超过 {} 个步骤！",
 },
 "net/minecraft/world/level/block/DispenserBlock.java": {
   "Ignoring dispensing attempt for Dispenser without matching block entity at {}": "忽略发射器的分发尝试：在 {} 处没有匹配的方块实体",
 },
 "net/minecraft/world/level/block/DropperBlock.java": {
   "Ignoring dispensing attempt for Dropper without matching block entity at {}": "忽略投掷器的投放尝试：在 {} 处没有匹配的方块实体",
 },
 "net/minecraft/world/level/block/LiquidBlock.java": {
   "Not a flowing fluid: ": "不是流动流体：",
 },
 "net/minecraft/world/level/block/SignBlock.java": {
   "Expected to only call this on server": "只应在服务端调用此方法",
 },
 "net/minecraft/world/level/block/TorchBlock.java": {
   "Not a SimpleParticleType: ": "不是 SimpleParticleType：",
 },
 "net/minecraft/world/level/block/entity/BannerPatternLayers.java": {
   "Unable to find banner pattern with id: '{}'": "找不到 id 为 '{}' 的旗帜图案",
 },
 "net/minecraft/world/level/block/entity/BlockEntity.java": {
   "Invalid block entity ": "无效的方块实体 ",
   " state at ": "，位于 ",
   ", got ": "，实际为 ",
   "Block entity {} found in a wrong chunk, expected position from chunk {}": "方块实体 {} 位于错误的区块中，期望位置来自区块 {}",
   "Skipping block entity with invalid type: {}": "跳过类型无效的方块实体：{}",
   "Failed to create block entity {} for block {} at position {} ": "创建方块实体 {} 失败（对应方块 {}，位于位置 {}）",
   "Failed to load data for block entity {} for block {} at position {}": "加载方块实体 {} 数据失败（对应方块 {}，位于位置 {}）",
   "Cached block": "缓存的方块",
   "Block location": "方块位置",
   " (world missing)": "（世界缺失）",
   "Actual block": "实际方块",
 },
 "net/minecraft/world/level/block/entity/BlockEntityTypes.java": {
   "Block entity type {} requires at least one valid block to be defined!": "方块实体类型 {} 至少需要定义一个有效方块！",
 },
 "net/minecraft/world/level/block/entity/BrushableBlockEntity.java": {
   "Expected max 1 loot from loot table {}, but got {}": "战利品表 {} 最多应产出 1 件战利品，实际产出 {} 件",
 },
 "net/minecraft/world/level/block/entity/ChiseledBookShelfBlockEntity.java": {
   "Expected slot 0-5, got {}": "期望槽位 0-5，实际为 {}",
 },
 "net/minecraft/world/level/block/entity/SignBlockEntity.java": {
   "Player {} just tried to change non-editable sign": "玩家 {} 试图修改不可编辑的告示牌",
   "{} issued server command: {}": "{} 执行了服务端命令：{}",
 },
 "net/minecraft/world/level/block/entity/TestBlockEntity.java": {
   "Test {} (at {}): {}": "测试 {}（位于 {}）：{}",
 },
 "net/minecraft/world/level/block/entity/TestInstanceBlockEntity.java": {
   "Test structure exporting is disabled": "测试结构导出已禁用",
   "Could not find structure ": "找不到结构 ",
   "Failed to save structure file {} to {}": "未能将结构文件 {} 保存到 {}",
   "Failed to save structure file ": "未能保存结构文件 ",
 },
 "net/minecraft/world/level/block/entity/TheEndGatewayBlockEntity.java": {
   "Creating portal at {}": "正在 {} 创建传送门",
   "Best exit position for portal at {} is {}": "位于 {} 的传送门的最佳出口位置为 {}",
   "Failed to find a suitable block to teleport to, spawning an island on {}": "未找到合适的传送目标方块，将在 {} 生成一座岛屿",
   "Found suitable block to teleport to: {}": "找到合适的传送目标方块：{}",
   "Skipping backwards past nonempty chunk at {}": "向后跳过位于 {} 的非空区块",
   "Skipping forward past empty chunk at {}": "向前跳过位于 {} 的空区块",
   "Found chunk at {}": "在 {} 找到区块",
 },
 "net/minecraft/world/level/block/entity/TrialSpawnerBlockEntity.java": {
   "Expected non-null level": "期望 level 非空",
 },
 "net/minecraft/world/level/block/entity/trialspawner/TrialSpawnerStateData.java": {
   "Trial Spawner at ": "试炼刷怪笼位于 ",
   " has no detected players": "，未检测到任何玩家",
 },
 "net/minecraft/world/level/block/entity/vault/VaultConfig.java": {
   "Activation range must (": "激活范围必须（",
   ") be less or equal to deactivation range (": "）小于等于停用范围（",
 },
 "net/minecraft/world/level/block/grower/TreeGrower.java": {
   "Unknown tree generator ": "未知的树木生成器 ",
 },
 "net/minecraft/world/level/block/state/BlockBehaviour.java": {
   "block onPlace": "方块放置",
   "%s has a collision shape and an offset type, but is not marked as dynamicShape in its properties.": "%s 具有碰撞形状和偏移类型，但在其属性中未标记为 dynamicShape。",
   "Block id not set": "方块 id 未设置",
 },
 "net/minecraft/world/level/block/state/StateDefinition.java": {
   " has invalidly named property: ": " 存在命名无效的属性：",
   " attempted use property ": " 尝试使用属性 ",
   " with <= 1 possible values": "，但其可能取值不超过 1 个",
   " has property: ": " 的属性：",
   " with invalidly named value: ": " 存在命名无效的值：",
   " has duplicate property: ": " 重复的属性：",
 },
 "net/minecraft/world/level/block/state/StateHolder.java": {
   "Cannot get property ": "无法获取属性 ",
   " as it does not exist in ": "，因为它不存在于 ",
   "Cannot set property ": "无法设置属性 ",
   ", it is not an allowed value": "，它不是允许的值",
 },
 "net/minecraft/world/level/block/state/pattern/BlockPattern.java": {
   "Invalid forwards & up combination": "forward 与 up 的组合无效",
 },
 "net/minecraft/world/level/block/state/pattern/BlockPatternBuilder.java": {
   "Expected aisle with height of ": "期望通道高度为 ",
   ", but was given one with a height of ": "，但实际给定的通道高度为 ",
   "Not all rows in the given aisle are the correct width (expected ": "给定通道中并非所有行的宽度都正确（期望 ",
   ", found one with ": "，但发现某行为 ",
   "Empty pattern for aisle": "通道模式为空",
   "Predicates for character(s) ": "缺少字符（",
   " are missing": "）的谓词",
 },
 "net/minecraft/world/level/block/state/predicate/BlockStatePredicate.java": {
   " cannot support property ": " 不支持属性 ",
 },
 "net/minecraft/world/level/block/state/properties/EnumProperty.java": {
   "Trying to make empty EnumProperty '": "试图创建空的 EnumProperty '",
 },
 "net/minecraft/world/level/block/state/properties/IntegerProperty.java": {
   "Min value of ": "最小值 ",
   " must be 0 or greater": " 必须大于等于 0",
   "Max value of ": "最大值 ",
   " must be greater than min (": " 必须大于最小值（",
 },
 "net/minecraft/world/level/block/state/properties/Property.java": {
   "Unable to read property: ": "无法读取属性：",
   " with value: ": "，其值为：",
   " does not belong to property ": " 不属于属性 ",
 },
 "net/minecraft/world/level/levelgen/BelowZeroRetrogen.java": {
   "target_status cannot be empty": "target_status 不能为空",
 },
 "net/minecraft/world/level/levelgen/BitRandomSource.java": {
   "Bound must be positive": "上界必须为正数",
 },
 "net/minecraft/world/level/levelgen/Column.java": {
   "Column of negative height: ": "高度为负的柱状结构：",
 },
 "net/minecraft/world/level/levelgen/DensityFunctions.java": {
   "Calling .codec() on HolderHolder": "在 HolderHolder 上调用 .codec()",
   "Expected ": "期望 ",
   " thresholds for ": " 个阈值，对应 ",
   " functions, but got ": " 个函数，但实际得到 ",
   "Threshold values must be ordered from smallest to largest": "阈值必须按从小到大的顺序排列",
   "Creating a {} function between two non-overlapping inputs: {} and {}": "在两个不重叠的输入之间创建 {} 函数：{} 和 {}",
 },
 "net/minecraft/world/level/levelgen/Heightmap.java": {
   "Ignoring heightmap data for chunk {}, size does not match; expected: {}, got: {}": "忽略区块 {} 的高度图数据，大小不匹配；期望：{}，实际：{}",
 },
 "net/minecraft/world/level/levelgen/NoiseChunk.java": {
   "Staring interpolation twice": "重复启动插值",
   "Trying to sample interpolator outside the interpolation loop": "试图在插值循环之外采样插值器",
 },
 "net/minecraft/world/level/levelgen/NoiseSettings.java": {
   "min_y + height cannot be higher than: ": "min_y + height 不能高于：",
   "height has to be a multiple of 16": "height 必须为 16 的倍数",
   "min_y has to be a multiple of 16": "min_y 必须为 16 的倍数",
 },
 "net/minecraft/world/level/levelgen/SurfaceRules.java": {
   "Need at least 1 rule for a sequence": "序列至少需要 1 条规则",
   "Update triggered but the result is null": "触发了更新，但结果为 null",
 },
 "net/minecraft/world/level/levelgen/WorldDimensions.java": {
   "Overworld settings missing": "主世界设置缺失",
 },
 "net/minecraft/world/level/levelgen/WorldGenerationContext.java": {
   "WorldGenerationContext was initialized without a Level, but WorldGenerationContext#level was called": "WorldGenerationContext 在初始化时未提供 Level，但调用了 WorldGenerationContext#level",
 },
 "net/minecraft/world/level/levelgen/XoroshiroRandomSource.java": {
   "Bound must be positive": "上界必须为正数",
 },
 "net/minecraft/world/level/levelgen/blending/BlendingData.java": {
   "heights has to be of length ": "heights 的长度必须为 ",
 },
 "net/minecraft/world/level/levelgen/feature/FeatureCountTracker.java": {
   "Failed to increment chunk count": "递增区块计数失败",
   "Failed to increment feature count": "递增特性计数失败",
   "Cleared feature counts": "已清除特性计数",
   "Logging feature counts:": "正在记录特性计数：",
   "{} total_chunks: {}": "{} total_chunks：{}",
 },
 "net/minecraft/world/level/levelgen/feature/FossilFeatureConfiguration.java": {
   "Fossil structure lists need at least one entry": "化石结构列表至少需要一个条目",
   "Fossil structure lists must be equal lengths": "化石结构列表长度必须相等",
 },
 "net/minecraft/world/level/levelgen/feature/MonsterRoomFeature.java": {
   "Failed to fetch mob spawner entity at ({}, {}, {})": "在 ({}, {}, {}) 处获取生物刷怪笼实体失败",
 },
 "net/minecraft/world/level/levelgen/feature/configurations/MultifaceGrowthConfiguration.java": {
   "Growth block should be a multiface spreadeable block": "生长方块必须是可多方附着蔓延的方块",
 },
 "net/minecraft/world/level/levelgen/feature/stateproviders/RandomizedIntStateProvider.java": {
   "Property value out of range: ": "属性值超出范围：",
 },
 "net/minecraft/world/level/levelgen/feature/stateproviders/WeightedStateProvider.java": {
   "Weighted list must have at least one entry": "加权列表至少需要一个条目",
 },
 "net/minecraft/world/level/levelgen/feature/trunkplacers/CherryTrunkPlacer.java": {
   "Need at least 2 blocks variation for the branch starts to fit both branches": "分支起点至少需要 2 个方块的变化范围，才能容纳两个分支",
 },
 "net/minecraft/world/level/levelgen/flat/FlatLevelGeneratorSettings.java": {
   "Sum of layer heights is > ": "各层高度之和大于 ",
   "Unknown biome, defaulting to plains": "未知生物群系，默认使用平原",
 },
 "net/minecraft/world/level/levelgen/heightproviders/BiasedToBottomHeight.java": {
   "Empty height range: {}": "高度范围为空：{}",
 },
 "net/minecraft/world/level/levelgen/heightproviders/TrapezoidHeight.java": {
   "Empty height range: {}": "高度范围为空：{}",
 },
 "net/minecraft/world/level/levelgen/heightproviders/UniformHeight.java": {
   "Empty height range: {}": "高度范围为空：{}",
 },
 "net/minecraft/world/level/levelgen/heightproviders/VeryBiasedToBottomHeight.java": {
   "Empty height range: {}": "高度范围为空：{}",
 },
 "net/minecraft/world/level/levelgen/placement/BiomeFilter.java": {
   "Tried to biome check an unregistered feature, or a feature that should not restrict the biome": "试图对未注册的特性，或不应限制生物群系的特性进行生物群系检查",
 },
 "net/minecraft/world/level/levelgen/presets/WorldPreset.java": {
   "Missing overworld dimension": "缺少主世界维度",
 },
 "net/minecraft/world/level/levelgen/structure/BoundingBox.java": {
   "Invalid bounding box data, inverted bounds for: ": "无效的边界框数据，边界反转，对象：",
 },
 "net/minecraft/world/level/levelgen/structure/PoolElementStructurePiece.java": {
   "Invalid pool element found": "发现无效的池元素",
 },
 "net/minecraft/world/level/levelgen/structure/StructureCheck.java": {
   "Failed to read chunk {}": "读取区块 {} 失败",
   "Failed to partially datafix chunk {}": "对区块 {} 进行部分数据修复失败",
 },
 "net/minecraft/world/level/levelgen/structure/StructurePiece.java": {
   "Unable to calculate boundingbox without pieces": "在没有部件的情况下无法计算边界框",
 },
 "net/minecraft/world/level/levelgen/structure/StructureStart.java": {
   "Unknown stucture id: {}": "未知的结构 id：{}",
   "Failed Start with id {}": "启动 id 为 {} 的结构失败",
 },
 "net/minecraft/world/level/levelgen/structure/TemplateStructurePiece.java": {
   "Error while parsing blockstate {} in jigsaw block @ {}": "解析 @ {} 处拼图方块中的方块状态 {} 时出错",
 },
 "net/minecraft/world/level/levelgen/structure/pieces/PiecesContainer.java": {
   "Unknown structure piece id: {}": "未知的结构部件 id：{}",
   "Exception loading structure piece with id {}": "加载 id 为 {} 的结构部件时发生异常",
 },
 "net/minecraft/world/level/levelgen/structure/placement/RandomSpreadStructurePlacement.java": {
   "Spacing has to be larger than separation": "间距必须大于间隔",
 },
 "net/minecraft/world/level/levelgen/structure/pools/EmptyPoolElement.java": {
   "Invalid call to EmptyPoolElement.getBoundingBox, filter me!": "错误调用 EmptyPoolElement.getBoundingBox，请先过滤！",
 },
 "net/minecraft/world/level/levelgen/structure/pools/JigsawPlacement.java": {
   "No starting jigsaw {} found in start pool {}": "未找到起始拼图块 {}（位于起始池 {} 中）",
   "Center piece {} with bounding box {} does not fit dimension padding {}": "中心部件 {}（边界框 {}）不适应维度边距 {}",
   "Empty or non-existent pool: {}": "池为空或不存在：{}",
   "Empty or non-existent fallback pool: {}": "回退池为空或不存在：{}",
 },
 "net/minecraft/world/level/levelgen/structure/pools/ListPoolElement.java": {
   "Elements are empty": "元素列表为空",
   "Unable to calculate boundingbox for ListPoolElement": "无法计算 ListPoolElement 的边界框",
 },
 "net/minecraft/world/level/levelgen/structure/pools/SinglePoolElement.java": {
   "Can not serialize a runtime pool element": "无法序列化运行时池元素",
 },
 "net/minecraft/world/level/levelgen/structure/pools/alias/PoolAliasLookup.java": {
   " was mapped to null value": " 被映射为 null 值",
 },
 "net/minecraft/world/level/levelgen/structure/structures/JigsawStructure.java": {
   "Horizontal structure size including terrain adaptation must not exceed 128": "包含地形适配在内的结构水平尺寸不得超过 128",
 },
 "net/minecraft/world/level/levelgen/structure/templatesystem/AxisAlignedLinearPosTest.java": {
   "Invalid range: [": "无效范围：[",
 },
 "net/minecraft/world/level/levelgen/structure/templatesystem/CappedProcessor.java": {
   "Original block info list not in sync with processed list, skipping processing. Original size: ": "原始方块信息列表与已处理列表不同步，跳过处理。原始大小：",
   ", Processed size: ": "，已处理大小：",
 },
 "net/minecraft/world/level/levelgen/structure/templatesystem/JigsawReplacementProcessor.java": {
   "Jigsaw block at {} is missing nbt, will not replace": "位于 {} 的拼图块缺少 NBT，将不进行替换",
   "Failed to parse jigsaw replacement state '{}' at {}: {}": "解析拼图替换状态 '{}'（位于 {}）失败：{}",
 },
 "net/minecraft/world/level/levelgen/structure/templatesystem/LinearPosTest.java": {
   "Invalid range: [": "无效范围：[",
 },
 "net/minecraft/world/level/levelgen/structure/templatesystem/StructurePlaceSettings.java": {
   "No palettes": "没有调色板",
   "Palette index out of bounds. Got ": "调色板索引越界，得到 ",
   " where there are only ": "，但仅有 ",
   " palettes available.": " 个可用调色板。",
 },
 "net/minecraft/world/level/levelgen/structure/templatesystem/StructureTemplate.java": {
   " nbt was null": " nbt 为 null",
 },
 "net/minecraft/world/level/levelgen/structure/templatesystem/StructureTemplateManager.java": {
   "Failed to save structure file {} to {}": "未能将结构文件 {} 保存到 {}",
 },
 "net/minecraft/world/level/levelgen/structure/templatesystem/loader/DirectoryTemplateSource.java": {
   "Couldn't load structure from {}:{}": "无法从 {}:{} 加载结构",
 },
 "net/minecraft/world/level/levelgen/structure/templatesystem/loader/ResourceManagerTemplateSource.java": {
   "Couldn't load structure {}": "无法加载结构 {}",
 },
 "net/minecraft/world/level/levelgen/structure/templatesystem/loader/TemplatePathFactory.java": {
   "Invalid file path '": "无效的文件路径：'",
   "Resource path '": "资源路径：'",
   "' is not portable": "' 不可移植",
 },
 "net/minecraft/world/level/levelgen/synth/PerlinNoise.java": {
   "Need some octaves!": "需要至少一个八度！",
   "Total number of octaves needs to be >= 1": "八度总数必须 >= 1",
   "Failed to create correct number of noise levels for given non-zero amplitudes": "无法为给定的非零振幅创建正确数量的噪声层",
   "Positive octaves are temporarily disabled": "正八度暂时被禁用",
 },
 "net/minecraft/world/level/levelgen/synth/PerlinSimplexNoise.java": {
   "Need some octaves!": "需要至少一个八度！",
   "Total number of octaves needs to be >= 1": "八度总数必须 >= 1",
 },
}

def apply_one(rel, tmap):
    fp = os.path.join(BASE, rel.replace('/', os.sep))
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    strings = ft.find_strings_with_positions(content)
    replacements = []
    for start, end, str_content, is_tb in strings:
        if str_content in tmap:
            trans = tmap[str_content]
            if trans != str_content:
                replacements.append((start, end, str_content, trans, is_tb))
    replacements.sort(key=lambda x: x[0], reverse=True)
    modified = content
    applied = 0
    for start, end, orig, trans, is_tb in replacements:
        actual = modified[start+1:end-1] if not is_tb else modified[start+3:end-3]
        if actual != orig:
            print(f"  WARN mismatch @{start} in {rel}", file=sys.stderr)
            continue
        if is_tb:
            modified = modified[:start+3] + trans + modified[end-3:]
        else:
            modified = modified[:start+1] + trans + modified[end-1:]
        applied += 1
    issues = ft.verify_file(modified)
    if issues:
        print(f"VERIFY_FAIL {rel}: {issues}", file=sys.stderr)
        return applied, issues
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(modified)
    return applied, []

total_applied = 0
changed_files = 0
failures = []
for rel, tmap in T.items():
    applied, issues = apply_one(rel, tmap)
    if issues:
        failures.append((rel, issues))
    else:
        changed_files += 1
        total_applied += applied
        print(f"OK  {applied:3d}  {rel}")

print("=" * 50)
print(f"changed_files={changed_files}")
print(f"total_string_replacements={total_applied}")
print(f"failures={len(failures)}")
for rel, iss in failures:
    print("FAIL:", rel, iss)
