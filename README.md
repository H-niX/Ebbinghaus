# 艾宾浩斯单词复习系统

基于艾宾浩斯遗忘曲线的智能英语单词复习计划系统，支持新学单词、标熟单词和阅读记录的复习管理。

## ✨ 核心特性

- **🧠 艾宾浩斯遗忘曲线**: 基于科学的记忆遗忘规律进行复习调度
- **📚 多类型学习**: 支持新学单词、标熟单词和阅读记录三种类型
- **🔄 智能标熟**: 标熟操作不会凭空增加单词，而是从现有新学单词中转换
- **📅 动态时间**: 显示相对时间（今天、昨天、前天等）
- **📊 一周概览**: 快速查看未来一周的复习计划
- **💾 Excel存储**: 使用Excel文件进行数据持久化存储

## 🚀 快速开始

### 安装依赖
```bash
pip install -r requirements.txt
```

### 启动方式

1. **Web界面（推荐）**:
   ```bash
   python app.py
   ```
   然后访问: http://127.0.0.1:5000

2. **命令行模式**:
   ```bash
   python ebbinghaus.py
   ```

## 📖 使用说明

### 新学单词
- 记录每天新学习的单词数量
- 按照艾宾浩斯间隔进行复习：1, 2, 4, 7, 15, 30天

### 标熟单词
- **重要**: 标熟操作不会增加新单词，而是将现有的新学单词转换为标熟状态
- 转换优先级：已掌握的单词 > 高复习阶段 > 低复习阶段
- 标熟单词复习间隔：7, 30, 90, 180天

### 阅读记录
- 支持三种阅读类型：段落、文章、长篇
- 记录阅读时长（分钟）
- 不同类型有不同的复习间隔：
  - 段落阅读：1, 3, 7天
  - 文章阅读：2, 5, 10天
  - 长篇阅读：3, 7, 14天

## 📁 项目结构

```
艾宾浩斯单词/
├── app.py                 # Web应用主文件
├── ebbinghaus.py         # 核心算法实现
├── config.py             # 配置文件
├── vocabulary.xlsx       # 数据存储文件
├── requirements.txt      # 依赖包列表
├── static/              # 静态资源
│   └── app.js
├── templates/           # HTML模板
│   ├── index.html      # 主界面
│   └── guide.html      # 使用指南
└── README.md           # 项目说明
```

## 🎯 复习逻辑

### 艾宾浩斯间隔设置
- **新学单词**: [1, 2, 4, 7, 15, 30] 天
- **标熟单词**: [7, 30, 90, 180] 天
- **阅读复习**: 根据类型有不同间隔

### 标熟转换逻辑
1. 从现有新学单词中选择转换对象
2. 优先转换已完成复习的单词
3. 重置为标熟类型的复习周期
4. 如果可转换数量不足，给出提示

### 复习状态管理
- **pending**: 等待复习
- **reviewed**: 已复习
- **mastered**: 已掌握

## 📊 数据存储

系统使用Excel文件(`vocabulary.xlsx`)存储数据，包含以下字段：
- `date`: 学习日期
- `word_count`: 单词数量
- `word_type`: 类型(new/marked_familiar/reading_*)
- `stage`: 复习阶段
- `next_review_date`: 下次复习日期
- `status`: 状态
- `duration`: 阅读时长

## 🔧 开发者说明

### 核心类
- `SimpleEbbinghausSystem`: 主系统类
- `add_learning_session()`: 添加学习会话
- `_convert_to_marked_familiar()`: 标熟转换逻辑
- `get_today_plan()`: 获取今日复习计划
- `get_weekly_overview()`: 获取一周概览

### API接口
- `POST /api/add_learning`: 添加学习记录
- `POST /api/add_reading`: 添加阅读记录
- `GET /api/today_plan`: 获取今日计划
- `GET /api/weekly_overview`: 获取一周概览
- `POST /api/complete_review`: 完成复习

## 📝 更新日志

### v2.0.0 (2025-08-20)
- ✅ 修正标熟单词逻辑，不再凭空创建单词
- ✅ 将'familiar'改为'marked_familiar'，更准确表达含义
- ✅ 清理项目文件，移除所有冗余和测试文件
- ✅ 优化项目结构，保留核心功能文件
- ✅ 更新文档和说明

### v1.x.x
- 基础功能实现
- Web界面开发
- Excel数据存储
- 艾宾浩斯算法实现

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request来帮助改进项目！
