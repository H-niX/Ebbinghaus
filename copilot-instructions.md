<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# 艾宾浩斯单词复习计划项目 - Copilot 指令

## 项目概述
这是一个基于艾宾浩斯遗忘曲线的智能英语单词复习计划系统。项目使用Python开发，采用Excel作为数据持久化存储，实现了动态复习调度和负载平衡功能。

## 核心特性
- **艾宾浩斯遗忘曲线**: 基于科学的记忆保持公式 R(t) = e^(-t/S) 进行复习调度
- **双模式调度**: 支持固定间隔表和自适应连续曲线两种模式
- **动态负载平衡**: 通过允许延迟(slack)算法避免复习积压
- **Excel数据存储**: 使用多工作表结构存储配置、单词、计划、日志等数据
- **断点续跑**: 支持中途断更和补记功能

## 代码风格指南
- 使用类型提示(type hints)
- 函数和类都要有详细的docstring
- 错误处理使用try-catch块并记录日志
- 变量命名采用snake_case风格
- 常量使用UPPER_CASE

## 核心算法说明
1. **记忆保持率公式**: R(t) = e^(-t/S)，其中t为天数，S为记忆稳定度
2. **下次复习时间**: t_next = -S × ln(p)，其中p为目标保持率
3. **允许延迟计算**: slack = max(0, t_max - I)，用于负载平衡

## Excel文件结构
- **Config**: 系统配置参数
- **Words**: 单词主档(word_id, learn_date, stage, stability等)
- **Schedule**: 复习计划表(date, word_id, status, allowed_slack等)
- **Log**: 复习历史记录
- **Agenda**: 每日复习清单概览

## 主要类和方法
- `EbbinghausScheduler`: 核心调度器类
  - `add_learning_session()`: 添加学习会话
  - `record_review()`: 记录复习结果
  - `get_daily_agenda()`: 获取每日计划
  - `_apply_load_balancing()`: 应用负载平衡
- `EbbinghausUtils`: 实用工具类，包含可视化和导入导出功能

## 开发注意事项
- 所有日期处理统一使用date对象，避免时区问题
- Excel读写操作要包含错误处理和备份机制
- 配置参数要有合理的默认值和边界检查
- 复习质量评分范围为0-5，需要验证输入
- 文件路径使用pathlib.Path处理跨平台兼容性

## 测试和示例
- examples.py 包含完整的使用示例
- 支持命令行和交互式两种使用方式
- 提供可视化分析功能(需要matplotlib)

在开发新功能或修复bug时，请遵循上述指南并确保与现有代码风格保持一致。
