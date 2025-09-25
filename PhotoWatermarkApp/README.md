
# 照片水印应用 - README

## 项目简介

照片水印应用是一款本地桌面应用程序，旨在为用户提供简单易用的照片水印添加功能。支持文本水印和图片水印，可自定义水印的位置、大小、颜色、透明度等属性，支持批量处理和多种导出选项。

## 功能特点

- **图片导入**：支持单张或批量导入图片
- **文本水印**：添加自定义文本水印，支持字体、大小、颜色和透明度调整
- **图片水印**：添加自定义图片作为水印，支持缩放和透明度调整
- **水印布局**：提供多种预设位置和自定义位置功能
- **实时预览**：实时显示水印效果
- **批量处理**：支持批量处理多张图片
- **导出设置**：支持多种导出格式、质量和尺寸调整
- **模板管理**：保存和加载水印设置模板
- **用户友好界面**：直观易用的操作界面

## 技术架构

本项目采用分层架构设计，分为表现层、业务逻辑层和数据访问层：

- **表现层**：基于PyQt6实现用户界面
- **业务逻辑层**：处理图片导入、导出和水印生成等核心业务
- **数据访问层**：负责图片、配置和模板的存储和管理

## 系统要求

- 操作系统：Windows 10/11
- Python 3.8或更高版本
- 内存：至少4GB RAM
- 硬盘空间：至少100MB可用空间

## 安装指南

### 1. 环境准备

确保您的系统已安装Python 3.8或更高版本。如果没有安装，请从[Python官网](https://www.python.org/downloads/)下载并安装。

### 2. 克隆项目

```bash
git clone <项目仓库地址>
cd PhotoWatermark2
```

### 3. 创建虚拟环境（推荐）

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# 或
source venv/bin/activate  # macOS/Linux
```

### 4. 安装依赖

```bash
pip install -r requirements.txt
```

### 5. 创建必要目录

```bash
mkdir -p PhotoWatermarkApp/resources/icons
mkdir -p PhotoWatermarkApp/resources/styles
mkdir -p PhotoWatermarkApp/templates
```

## 使用说明

### 启动应用

```bash
python PhotoWatermarkApp/main.py
```

### 基本操作流程

1. **导入图片**
   - 点击"文件"菜单 > "导入图片"，或使用快捷键Ctrl+I
   - 选择一张或多张图片导入

2. **添加水印**
   - 在右侧控制面板选择水印类型（文本或图片）
   - 调整水印参数（文本内容、字体、大小、颜色、透明度等）
   - 选择水印位置（预设位置或自定义拖拽）
   - 实时预览效果

3. **导出图片**
   - 设置输出文件夹
   - 选择导出格式和质量
   - 设置文件命名规则
   - 点击"导出图片"按钮

### 高级功能

- **模板管理**：保存当前水印设置为模板，方便以后重复使用
- **批量处理**：同时处理多张图片，应用相同的水印设置
- **图片调整**：在导出时调整图片尺寸和质量

## 项目结构

```
PhotoWatermarkApp/
├── main.py              # 应用入口
├── ui/                  # UI层代码
│   ├── __init__.py
│   ├── main_window.py   # 主窗口
│   ├── image_view.py    # 图片列表视图
│   ├── preview_area.py  # 图片预览区
│   ├── watermark_panel.py # 水印控制面板
│   └── export_panel.py  # 导出设置面板
├── core/                # 业务逻辑层代码
│   ├── __init__.py
│   ├── file_processor.py # 文件处理模块
│   ├── watermark_processor.py # 水印处理模块
│   └── config_manager.py # 配置管理模块
├── data/                # 数据访问层代码
│   ├── __init__.py
│   ├── image_storage.py  # 图片存储
│   ├── template_storage.py # 模板存储
│   └── config_storage.py # 配置存储
└── utils/               # 工具类
    ├── __init__.py
    ├── image_utils.py   # 图片处理工具
    └── ui_utils.py      # UI工具函数
```

## 开发指南

### 环境配置

1. 安装开发依赖：
   ```bash
   pip install pylint pytest black
   ```

2. 代码格式化：
   ```bash
   black .
   ```

3. 代码检查：
   ```bash
   pylint PhotoWatermarkApp/
   ```

### 架构说明

项目采用分层架构，各层职责如下：

- **UI层**：负责用户界面展示和交互
- **业务逻辑层**：处理核心业务逻辑，如水印生成和应用
- **数据访问层**：负责数据持久化和访问
- **工具类**：提供通用工具函数

### 扩展开发

如需扩展功能，建议按照以下步骤：

1. 确定功能属于哪一层
2. 在相应层创建新的模块或类
3. 实现功能逻辑
4. 更新UI以展示新功能
5. 编写测试用例

## 常见问题

### Q: 应用启动失败，提示缺少模块
A: 请确保已安装所有依赖包：
```bash
pip install -r requirements.txt
```

### Q: 图片导入失败
A: 请确认图片格式受支持（JPEG、PNG、BMP、TIFF），并且图片文件未损坏。

### Q: 水印显示不正确
A: 请检查水印设置，确保参数值在合理范围内。如问题持续，请尝试重置应用设置。

### Q: 导出失败
A: 请确认输出文件夹有写入权限，并且磁盘有足够空间。

## 贡献指南

我们欢迎社区贡献！请遵循以下步骤：

1. Fork项目
2. 创建功能分支：`git checkout -b feature/AmazingFeature`
3. 提交更改：`git commit -m 'Add some AmazingFeature'`
4. 推送到分支：`git push origin feature/AmazingFeature`
5. 提交Pull Request

## 版本历史

- **v1.0.0** - 初始版本，包含基本的水印添加功能

## 许可证

本项目采用MIT许可证。详情请参阅[LICENSE](LICENSE)文件。

## 联系方式

如有问题或建议，请通过以下方式联系我们：

- 项目主页：[GitHub项目地址]
- 问题反馈：[GitHub Issues]
- 电子邮件：[项目邮箱]

## 致谢

感谢所有为项目做出贡献的开发者和测试人员。