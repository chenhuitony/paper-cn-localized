# Paper 26.2 全量汉化版（简体中文）

基于 [PaperMC/Paper](https://github.com/PaperMC/Paper) 26.2 的全量简体中文化服务端。日志、命令、异常提示、配置说明等**用户可见字符串**全部汉化，并可脱离原汉化工作区、从补丁一键重建源码。

> 英文说明见上游 `README.md`；本文件为汉化项目的完整介绍。

## 汉化内容

| 范围 | 数量 | 说明 |
|------|------|------|
| Paper 自研代码（`paper-server/src/main/java` + `paper-api`） | 1156 个文件 | 日志、命令、异常、配置说明等全部用户可见字符串 |
| Vanilla 原版源码 | 701 个文件含中文 | 世界生成、实体、网络、命令等全模块 |
| 补丁固化 | `0035`/`0036` 两个汉化补丁（2797 行） | `applyPatches` 可从补丁完整重建汉化工作树 |

**汉化原则**：只翻译用户可见字符串；注释、翻译键、注册键、序列化/行为关键字符串、占位符一律保留原文，保证编译与运行时行为与官方一致。

## 目录结构

```
├── paper-server/
│   ├── src/main/java/          # Paper 自研源码（已汉化，已入库）
│   ├── patches/
│   │   ├── features/           # 功能补丁（0035/0036 为汉化补丁）
│   │   └── sources/            # vanilla 源码补丁（934 个英文基线）
│   └── src/minecraft/java/     # vanilla 汉化工作树（不入库，由补丁重建）
├── .mc_translation/            # 翻译母本：提取/回写脚本 + 键值映射数据
├── paper-api/                  # Paper API（汉化 + javadoc 构建修复）
└── gradlew                     # 构建入口（需 JDK 25）
```

> vanilla 源码采用 Paper 官方"补丁模式"：源码本体不入库，任何人克隆本仓库后运行 `gradlew applyPatches` 即可从补丁重建出完整的 701 文件汉化源码。

## 构建与启动

```bash
# 前置：JDK 25（Paper 26.x 要求）

# 1. 从补丁重建汉化工作树（含全部 vanilla 汉化源码）
gradlew applyPatches

# 2. 构建可运行服务端 jar
gradlew createPaperclipJar createBundlerJar

# 3. 启动
java -jar paper-server/build/libs/paper-paperclip-26.2.local-SNAPSHOT.jar
```

首次启动会自动下载原版服务端并应用汉化补丁，控制台、崩溃报告、踢出提示等均为简体中文。

## 翻译母本（.mc_translation）

汉化的"母本"数据与自动化脚本，用于：

- `file_translator.py`：提取 / 回写 / 校验翻译
- `restore_translations2.py`：全局 / 文件级映射回写（曾用于在 `rebuildSourcePatches` 意外回滚后无损恢复 701 文件汉化）
- `shard*.json`：各模块的翻译键值映射

**工作流建议**：只维护 `.mc_translation/` 数据文件；拉取上游新代码后在干净环境跑回写脚本并立即提交，不要把回写后的工作树当成唯一真相来源（一次 `rebuild` 即可将其抹除，而补丁与母本不会丢）。

## 许可

本项目以 MIT 协议发布（见 LICENSE）。注意：本项目是 Paper（GPL）的派生汉化作品，引用或再分发时请同时遵守上游 PaperMC/Paper 的许可证要求，并在项目中保留上游版权声明。
