#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply curated Simplified-Chinese translations for shard 02, then verify."""
import sys, os, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import file_translator as ft

BASE = r"E:\编程\项目\Paper-main\paper-server\src\minecraft\java"

# relpath -> { original_string_content : translated_string_content }
T = {
 "net/minecraft/world/attribute/AttributeRange.java": {
  " is not in range [": " 不在范围 [",
 },
 "net/minecraft/world/attribute/AttributeType.java": {
  " is not valid for ": " 对以下属性无效：",
  " cannot be represented as a float": " 无法表示为 float",
 },
 "net/minecraft/world/attribute/EnvironmentAttribute.java": {
  "Missing default value": "缺少默认值",
 },
 "net/minecraft/world/attribute/EnvironmentAttributeMap.java": {
  "The following attributes cannot be positional: ": "以下属性不能为位置型：",
 },
 "net/minecraft/world/attribute/EnvironmentAttributeSystem.java": {
  "Position must always be provided for positional attribute ": "位置型属性必须始终提供位置：",
  "Missing attribute ": "缺少属性：",
 },
 "net/minecraft/world/clock/ServerClockManager.java": {
  "No clock initialized for definition: ": "未为定义初始化时钟：",
 },
 "net/minecraft/world/damagesource/DamageSource.java": {
  "Cannot set an event damager when another direct entity is already set (report a bug to Paper)": "当已设置另一个直接实体伤害者时，无法再设置事件伤害者（请向 Paper 报告此 bug）",
  "Cannot set a block snapshot when an event block damager is already set (report a bug to Paper)": "当已设置事件方块伤害者时，无法再设置方块快照（请向 Paper 报告此 bug）",
 },
 "net/minecraft/world/effect/MobEffectInstance.java": {
  "This method should only be called for matching effects!": "此方法仅应在匹配的效果上调用！",
 },
 "net/minecraft/world/entity/ContainerUser.java": {
  "A container user must be a LivingEntity": "容器使用者必须是 LivingEntity",
 },
 "net/minecraft/world/entity/Display.java": {
  "Failed to parse display entity text {}": "解析展示实体文本失败：{}",
 },
 "net/minecraft/world/entity/DropChances.java": {
  "Tried to set invalid equipment chance ": "试图设置无效的装备掉落概率：",
 },
 "net/minecraft/world/entity/Entity.java": {
  "Ignoring setSeed on Entity.SHARED_RANDOM": "正在忽略对 Entity.SHARED_RANDOM 的 setSeed 调用",
  "Tried to access entity ID before ID assignment": "在分配实体 ID 之前试图访问实体 ID",
  " was caught trying to crash the server with an invalid yaw": " 因试图用非法偏航角崩溃服务器而被拦截",
  "Infinite yaw (Hacking?)": "偏航角为无穷大（疑似作弊？）",
  " was caught trying to crash the server with an invalid pitch": " 因试图用非法俯仰角崩溃服务器而被拦截",
  "Infinite pitch (Hacking?)": "俯仰角为无穷大（疑似作弊？）",
  "Cannot move an entity off-main": "无法在主线程之外移动实体",
  "Colliding entity with block": "实体与方块碰撞时出错",
  "Block being collided with": "被碰撞的方块",
  "Entity being checked for collision": "正在检查碰撞的实体",
  "Saving entity NBT": "保存实体 NBT 时出错",
  "Entity being saved": "正在保存的实体",
  "Entity has invalid position": "实体位置非法",
  "Unknown fire override {} for {}": "未知的火焰覆盖规则 {}，用于 {}",
  "Entity has invalid rotation": "实体旋转角度非法",
  "Unknown SpawnReason ": "未知的生成原因：",
  "Loading entity NBT": "加载实体 NBT 时出错",
  "Entity being loaded": "正在加载的实体",
  "Unregistered entity": "未注册的实体",
  "Use x.startRiding(y), not y.addPassenger(x)": "请使用 x.startRiding(y)，而不是 y.addPassenger(x)",
  "Use x.stopRiding(y), not y.removePassenger(x)": "请使用 x.stopRiding(y)，而不是 y.removePassenger(x)",
  "Illegal Entity Teleport {} to {}:{}": "非法的实体传送：{} 传送到 {}:{}",
  "Entity Type": "实体类型",
  "Entity ID": "实体 ID",
  "Entity Name": "实体名称",
  "Entity's Exact location": "实体精确位置",
  "Entity's Block location": "实体所在方块位置",
  "Entity's Momentum": "实体动量",
  "Entity's Passengers": "实体的乘客",
  "Entity's Vehicle": "实体的载具",
  "[Entity info unavailable] ": "（实体信息不可用） ",
  "New entity position is invalid! Tried to set invalid position ({},{},{}) for entity {} located at {}, entity info: {}": "新实体位置非法！试图为位于 {} 的实体 {} 设置非法位置 ({},{},{})，实体信息：{}",
  "Refusing to update position for entity ": "拒绝更新实体 ",
  " to position ": " 的位置，目标为 ",
  " since it is processing a section status update": "，因为它正在处理区块段状态更新",
  "Invalid entity rotation: ": "非法的实体旋转角度：",
  ", discarding.": "，已丢弃。",
  " is currently prevented from being removed from the world since it is processing section status updates": " 目前被阻止从世界中移除，因为它正在处理区块段状态更新",
 },
 "net/minecraft/world/entity/EntityAttachments.java": {
  "Had no attachment point of type: ": "没有该类型的附着点：",
  " for index: ": "，索引：",
  "No attachment points of type: PASSENGER": "没有 PASSENGER 类型的附着点",
  "Had no attachment points of type: ": "没有该类型的附着点：",
 },
 "net/minecraft/world/entity/EntityType.java": {
  "Error loading spawn egg NBT": "读取刷怪蛋 NBT 时出错",
  "Skipping Entity with id {}": "跳过实体，其 id 为 {}",
  "Skipped entity tag: {}": "已跳过实体标签：{}",
  "Exception loading entity: ": "加载实体时发生异常：",
 },
 "net/minecraft/world/entity/EquipmentSlot.java": {
  "Invalid slot '": "非法槽位：'",
 },
 "net/minecraft/world/entity/ExperienceOrb.java": {
  "Invalid spawnReason set for experience orb: ": "为经验球设置了非法的 spawnReason：",
 },
 "net/minecraft/world/entity/Leashable.java": {
  "Invalid LeashData had no attachment": "非法的 LeashData：没有附着点",
 },
 "net/minecraft/world/entity/LivingEntity.java": {
  "Unknown friction state {} for {}": "未知的摩擦状态 {}，用于 {}",
  "Unable to add mob to team \\\"{}\\\" (that team probably doesn't exist)": "无法将生物添加到团队 \\\"{}\\\"（该团队可能不存在）",
  " had NaN health set": " 的生命值被设置为 NaN",
  "Named entity {} died: {}": "命名实体 {} 死亡：{}",
  "Invalid hand ": "非法的手臂：",
  "maxDistance must be between 1-120": "maxDistance 必须在 1-120 之间",
 },
 "net/minecraft/world/entity/Marker.java": {
  "Markers should never be sent": "标记实体绝不应被发送",
  "Should never addPassenger without checking couldAcceptPassenger()": "在未检查 couldAcceptPassenger() 的情况下绝不应调用 addPassenger",
 },
 "net/minecraft/world/entity/Mob.java": {
  "Unknown target reason, please report on the issue tracker": "未知的目标原因，请在 issue 跟踪器上报告",
 },
 "net/minecraft/world/entity/OminousItemSpawner.java": {
  "Should never addPassenger without checking couldAcceptPassenger()": "在未检查 couldAcceptPassenger() 的情况下绝不应调用 addPassenger",
 },
 "net/minecraft/world/entity/SpawnPlacements.java": {
  "Duplicate registration for type ": "重复注册类型：",
 },
 "net/minecraft/world/entity/ai/Brain.java": {
  "Unregistered memory fetched: ": "获取了未注册的记忆：",
 },
 "net/minecraft/world/entity/ai/attributes/AttributeInstance.java": {
  "Modifier is already applied on this attribute!": "该修饰符已应用于此属性！",
 },
 "net/minecraft/world/entity/ai/attributes/AttributeSupplier.java": {
  "Can't find attribute ": "找不到属性：",
  "Can't find modifier ": "找不到修饰符：",
  " on attribute ": "，位于属性：",
  "Tried to change value for default attribute instance: ": "试图修改默认属性实例的值：",
 },
 "net/minecraft/world/entity/ai/attributes/DefaultAttributes.java": {
  " has no attributes": " 没有属性",
 },
 "net/minecraft/world/entity/ai/attributes/RangedAttribute.java": {
  "Minimum value cannot be bigger than maximum value!": "最小值不能大于最大值！",
  "Default value cannot be lower than minimum value!": "默认值不能小于最小值！",
  "Default value cannot be bigger than maximum value!": "默认值不能大于最大值！",
 },
 "net/minecraft/world/entity/ai/behavior/RandomLookAround.java": {
  "Minimum pitch is larger than maximum pitch! ": "最小俯仰角大于最大俯仰角！",
 },
 "net/minecraft/world/entity/ai/goal/DoorInteractGoal.java": {
  "Unsupported mob type for DoorInteractGoal": "DoorInteractGoal 不支持的生物类型",
 },
 "net/minecraft/world/entity/ai/goal/FollowMobGoal.java": {
  "Unsupported mob type for FollowMobGoal": "FollowMobGoal 不支持的生物类型",
 },
 "net/minecraft/world/entity/ai/goal/FollowOwnerGoal.java": {
  "Unsupported mob type for FollowOwnerGoal": "FollowOwnerGoal 不支持的生物类型",
 },
 "net/minecraft/world/entity/ai/goal/MoveThroughVillageGoal.java": {
  "Unsupported mob for MoveThroughVillageGoal": "MoveThroughVillageGoal 不支持的生物",
 },
 "net/minecraft/world/entity/ai/goal/RangedAttackGoal.java": {
  "ArrowAttackGoal requires Mob implements RangedAttackMob": "ArrowAttackGoal 要求 Mob 实现 RangedAttackMob",
 },
 "net/minecraft/world/entity/ai/memory/MemoryMap.java": {
  "Memory module ": "记忆模块 ",
  " cannot be encoded": " 无法编码",
 },
 "net/minecraft/world/entity/ai/util/RandomPos.java": {
  "aboveSolidAmount was ": "aboveSolidAmount 为 ",
  ", expected >= 0": "，期望值 >= 0",
 },
 "net/minecraft/world/entity/ai/village/VillageSiege.java": {
  "Failed to create zombie for village siege at {}": "在 {} 处为村庄袭击生成僵尸失败",
 },
 "net/minecraft/world/entity/ai/village/poi/PoiManager.java": {
  "Accessing poi chunk off-main": "正在主线程之外访问 POI 区块",
  "Unloading poi chunk off-main": "正在主线程之外卸载 POI 区块",
  "Loading poi chunk off-main": "正在主线程之外加载 POI 区块",
  "POI never registered at ": "POI 从未在以下位置注册：",
 },
 "net/minecraft/world/entity/ai/village/poi/PoiSection.java": {
  "Added POI of type {} @ {}": "已添加类型为 {} 的 POI，位于 {}",
  "POI data mismatch: already registered at ": "POI 数据不匹配：已在以下位置注册：",
  "POI data mismatch: never registered at {}": "POI 数据不匹配：从未在 {} 处注册",
  "Removed POI of type {} @ {}": "已移除类型为 {} 的 POI，位于 {}",
  "POI never registered at ": "POI 从未在以下位置注册：",
 },
 "net/minecraft/world/entity/ai/village/poi/PoiTypes.java": {
  "%s is defined in more than one PoI type": "%s 被定义于多个 PoI 类型中",
 },
 "net/minecraft/world/entity/animal/equine/AbstractHorse.java": {
  "Incorrect range for an attribute": "属性范围不正确",
 },
 "net/minecraft/world/entity/animal/sheep/SheepColorSpawnRules.java": {
  "List must be non-empty": "列表不能为空",
 },
 "net/minecraft/world/entity/boss/enderdragon/EnderDragon.java": {
  "Failed to find path from {} to {}": "找不到从 {} 到 {} 的路径",
 },
 "net/minecraft/world/entity/boss/enderdragon/phases/DragonChargePlayerPhase.java": {
  "Aborting charge player as no target was set.": "未设置目标，正在放弃对玩家的冲锋。",
 },
 "net/minecraft/world/entity/boss/enderdragon/phases/DragonStrafePlayerPhase.java": {
  "Skipping player strafe phase because no player was found": "未找到玩家，跳过玩家环绕阶段",
 },
 "net/minecraft/world/entity/boss/enderdragon/phases/EnderDragonPhaseManager.java": {
  "Dragon is now in phase {} on the {}": "末影龙现在处于阶段 {}，位于 {}",
 },
 "net/minecraft/world/entity/decoration/BlockAttachedEntity.java": {
  "Block-attached entity at invalid position: {}": "附着于方块的实体位置非法：{}",
 },
 "net/minecraft/world/entity/decoration/Mannequin.java": {
  "Invalid pose: ": "非法的姿势：",
 },
 "net/minecraft/world/entity/item/FallingBlockEntity.java": {
  "Failed to load block entity from falling block": "从下落方块加载方块实体失败",
  "Immitating BlockState": "模拟的 BlockState",
 },
 "net/minecraft/world/entity/item/ItemEntity.java": {
  "Unknown friction state {} for {}": "未知的摩擦状态 {}，用于 {}",
 },
 "net/minecraft/world/entity/npc/villager/AbstractVillager.java": {
  "Cannot load Villager offers on the client": "无法在客户端加载村民交易选项",
  "Missing expected trade set {}": "缺少预期的交易集：{}",
 },
 "net/minecraft/world/entity/npc/villager/Villager.java": {
  "Villager {} died, message: '{}'": "村民 {} 死亡，死亡消息：'{}'",
  "Villager {} was struck by lightning {}.": "村民 {} 被闪电 {} 击中。",
 },
 "net/minecraft/world/entity/player/Inventory.java": {
  "Invalid selected slot": "选中的槽位非法",
  "Adding item to inventory": "向物品栏添加物品时出错",
  "Item being added": "正在添加的物品",
  "Item ID": "物品 ID",
  "Item data": "物品数据",
  "Item name": "物品名称",
 },
 "net/minecraft/world/entity/player/StackedContents.java": {
  " items, but only had ": " 个物品，但实际只有 ",
 },
 "net/minecraft/world/entity/projectile/FishingHook.java": {
  "Failed to recreate fishing hook on client. {} (id: {}) is not a valid owner.": "在客户端重建钓鱼钩失败。{}（id: {}）不是有效的拥有者。",
 },
 "net/minecraft/world/entity/projectile/arrow/AbstractArrow.java": {
  "Invalid weapon firing an arrow": "发射箭的武器非法",
 },
 "net/minecraft/world/entity/raid/Raid.java": {
  "Raiders alive: ": "存活的袭击者：",
  " Is bonus? ": " 是否为奖励袭击？ ",
 },
 "net/minecraft/world/entity/vehicle/ContainerEntity.java": {
  "Implement this method": "请重写此方法",
 },
 "net/minecraft/world/entity/vehicle/minecart/AbstractMinecart.java": {
  "Unknown friction state {} for {}": "未知的摩擦状态 {}，用于 {}",
 },
 "net/minecraft/world/flag/FeatureFlagRegistry.java": {
  "Unknown feature flag: {}": "未知的特性标志：{}",
  "Unknown feature ids: ": "未知的特性 id：",
  "Too many feature flags": "特性标志过多",
  "Duplicate feature flag ": "重复的特性标志：",
 },
 "net/minecraft/world/flag/FeatureFlagSet.java": {
  "Mismatched feature universe, expected '": "特性 universe 不匹配，期望为 '",
  "', but got '": "'，但实际为 '",
  "Mismatched set elements: '": "集合元素不匹配：'",
 },
 "net/minecraft/world/inventory/AbstractContainerMenu.java": {
  "Title already set": "标题已设置",
  "Unable to construct this menu by type": "无法按类型构造此菜单",
  "Container size ": "容器大小 ",
  " is smaller than expected ": " 小于预期值 ",
  "Container data count ": "容器数据计数 ",
  "Incorrect slot index: {} available slots: {}": "槽位索引不正确：{}，可用槽位数：{}",
  "Container click": "容器点击时出错",
  "Click info": "点击信息",
  "Menu Type": "菜单类型",
  "<no type>": "<无类型>",
  "Menu Class": "菜单类",
  "Slot Count": "槽位数量",
  "context was null": "context 为 null",
 },
 "net/minecraft/world/inventory/ContainerLevelAccess.java": {
  "Not supported yet.": "尚未支持。",
 },
 "net/minecraft/world/inventory/EnchantmentMenu.java": {
  " pressed invalid button id: ": " 按下了非法的按钮 id：",
 },
 "net/minecraft/world/inventory/ItemCombinerMenuSlotDefinition.java": {
  "Need to define both inputSlots and resultSlot": "必须同时定义 inputSlots 和 resultSlot",
  "Expected input slots to have continous indexes": "输入槽位的索引应连续",
  "Expected result slot index to follow last input slot": "结果槽位索引应紧随最后一个输入槽位之后",
 },
 "net/minecraft/world/inventory/LoomMenu.java": {
  "selectedPattern was null, this is unexpected": "selectedPattern 为 null，这不应该发生",
 },
 "net/minecraft/world/phys/AABB.java": {
  "Cannot build an undefined AABB. Include at least one point.": "无法构建未定义的 AABB。请至少包含一个点。",
 },
 "net/minecraft/world/phys/shapes/ArrayVoxelShape.java": {
  "Lengths of point arrays must be consistent with the size of the VoxelShape.": "点数组的长度必须与 VoxelShape 的大小一致。",
 },
 "net/minecraft/world/phys/shapes/CubePointRange.java": {
  "Need at least 1 part": "至少需要 1 个部分",
 },
 "net/minecraft/world/phys/shapes/DiscreteVoxelShape.java": {
  "Need all positive sizes: x: ": "所有尺寸必须为正数：x: ",
 },
 "net/minecraft/world/phys/shapes/Shapes.java": {
  "The min values need to be smaller or equals to the max values": "最小值必须小于或等于最大值",
 },
 "net/minecraft/world/phys/shapes/VoxelShape.java": {
  "No bounds for empty shape.": "空形状没有边界。",
  "Unknown axis: ": "未知的坐标轴：",
 },
 "net/minecraft/world/scores/PlayerTeam.java": {
  "Name cannot be null": "名称不能为空",
 },
 "net/minecraft/world/scores/Scoreboard.java": {
  "An objective with the name '": "名为 '",
  "' already exists!": "' 的计分目标已存在！",
  "Cannot modify read-only score": "无法修改只读分数",
  "Requested creation of existing team '{}'": "试图创建已存在的团队 '{}'",
  "Player is either on another team or not on any team. Cannot remove from team '": "玩家要么在另一个团队，要么不在任何团队中。无法从团队 '",
  "Unknown objective {} for name {}, ignoring": "名称 {} 对应的未知计分目标 {}，已忽略",
 },
 "net/minecraft/world/scores/criteria/ObjectiveCriteria.java": {
  "No scoreboard criteria with name: ": "没有名为以下名称的计分板判定标准：",
 },
 "net/minecraft/world/ticks/LevelTicks.java": {
  "Trying to schedule tick in not loaded position ": "试图在未加载的位置调度刻更新：",
 },
 "net/minecraft/world/timeline/Timeline.java": {
  " was defined multiple times in ": " 在以下时间线中被重复定义：",
  "Time Marker ": "时间标记 ",
  " must be in range [0; ": " 必须在范围 [0; ",
  "Timeline has no track for ": "时间线没有对应以下属性的轨道：",
 },
 "net/minecraft/world/waypoints/TrackedWaypoint.java": {
  "Unsupported Waypoint update operation: {}": "不支持的路径点更新操作：{}",
 },
}

def main():
    applied_files = 0
    applied_strings = 0
    failures = []
    skipped_unmatched = []

    for rel, mapping in T.items():
        fp = os.path.join(BASE, rel.replace('/', os.sep))
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()
        strings = ft.find_strings_with_positions(content)

        replacements = []
        seen = set()
        for start, end, str_content, is_tb in strings:
            if str_content in mapping and mapping[str_content] != str_content:
                replacements.append((start, end, str_content, mapping[str_content], is_tb))

        # report any keys in mapping that never matched
        matched_keys = {r[2] for r in replacements}
        for k in mapping:
            if k not in matched_keys:
                skipped_unmatched.append((rel, k))

        replacements.sort(key=lambda x: x[0], reverse=True)
        modified = content
        applied = 0
        for start, end, orig, trans, is_tb in replacements:
            actual = modified[start+1:end-1] if not is_tb else modified[start+3:end-3]
            if actual != orig:
                continue
            if is_tb:
                modified = modified[:start+3] + trans + modified[end-3:]
            else:
                modified = modified[:start+1] + trans + modified[end-1:]
            applied += 1

        issues = ft.verify_file(modified)
        if issues:
            failures.append((rel, issues))
            print(f"VERIFY FAILED {rel}: {issues}", file=sys.stderr)
            continue

        with open(fp, 'w', encoding='utf-8') as f:
            f.write(modified)
        applied_files += 1
        applied_strings += applied
        print(f"OK [{applied:3d}] {rel}")

    print("=" * 50)
    print(f"files modified: {applied_files}")
    print(f"string replacements applied: {applied_strings}")
    print(f"verify failures: {len(failures)}")
    if skipped_unmatched:
        print("UNMATCHED KEYS (not found in file):")
        for rel, k in skipped_unmatched:
            print(f"  {rel}: {k!r}")

if __name__ == '__main__':
    main()
