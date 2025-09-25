"""
主窗口UI组件
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QMenuBar, 
    QMenu, QStatusBar, QMessageBox
)
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt

from .image_view import ImageView
from .preview_area import PreviewArea
from .watermark_panel import WatermarkPanel
from .export_panel import ExportPanel


class MainWindow(QMainWindow):
    """主窗口类"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """初始化用户界面"""
        # 设置窗口属性
        self.setWindowTitle("照片水印应用")
        self.setMinimumSize(1024, 768)

        # 创建菜单栏
        self.create_menu_bar()

        # 创建主界面布局
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # 主布局：水平分为三部分
        main_layout = QHBoxLayout(main_widget)

        # 左侧：图片列表
        self.image_view = ImageView()
        main_layout.addWidget(self.image_view, 1)

        # 中间：预览区域
        self.preview_area = PreviewArea()
        main_layout.addWidget(self.preview_area, 2)

        # 右侧：控制面板（垂直分为水印设置和导出设置）
        control_panel = QWidget()
        control_layout = QVBoxLayout(control_panel)

        # 水印设置面板
        self.watermark_panel = WatermarkPanel()
        control_layout.addWidget(self.watermark_panel, 1)

        # 导出设置面板
        self.export_panel = ExportPanel()
        control_layout.addWidget(self.export_panel, 1)

        main_layout.addWidget(control_panel, 1)

        # 创建状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪")

        # 连接信号
        self.connect_signals()

    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()

        # 文件菜单
        file_menu = menubar.addMenu("文件(&F)")

        # 导入图片
        import_action = QAction(QIcon("resources/icons/import.png"), "导入图片(&I)", self)
        import_action.setShortcut("Ctrl+I")
        import_action.setStatusTip("导入一张或多张图片")
        import_action.triggered.connect(self.import_images)
        file_menu.addAction(import_action)

        # 导出图片
        export_action = QAction(QIcon("resources/icons/export.png"), "导出图片(&E)", self)
        export_action.setShortcut("Ctrl+E")
        export_action.setStatusTip("导出处理后的图片")
        export_action.triggered.connect(self.export_images)
        file_menu.addAction(export_action)

        file_menu.addSeparator()

        # 退出
        exit_action = QAction(QIcon("resources/icons/exit.png"), "退出(&X)", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("退出应用程序")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # 编辑菜单
        edit_menu = menubar.addMenu("编辑(&E)")

        # 撤销
        undo_action = QAction(QIcon("resources/icons/undo.png"), "撤销(&U)", self)
        undo_action.setShortcut("Ctrl+Z")
        undo_action.setStatusTip("撤销上一步操作")
        undo_action.triggered.connect(self.undo_action)
        edit_menu.addAction(undo_action)

        edit_menu.addSeparator()

        # 偏好设置
        preferences_action = QAction(QIcon("resources/icons/preferences.png"), "偏好设置(&P)", self)
        preferences_action.setShortcut("Ctrl+,")
        preferences_action.setStatusTip("设置应用程序偏好")
        preferences_action.triggered.connect(self.show_preferences)
        edit_menu.addAction(preferences_action)

        # 水印菜单
        watermark_menu = menubar.addMenu("水印(&W)")

        # 文本水印
        text_watermark_action = QAction(QIcon("resources/icons/text_watermark.png"), "文本水印(&T)", self)
        text_watermark_action.setShortcut("Ctrl+T")
        text_watermark_action.setStatusTip("添加文本水印")
        text_watermark_action.triggered.connect(self.add_text_watermark)
        watermark_menu.addAction(text_watermark_action)

        # 图片水印
        image_watermark_action = QAction(QIcon("resources/icons/image_watermark.png"), "图片水印(&I)", self)
        image_watermark_action.setShortcut("Ctrl+Shift+I")
        image_watermark_action.setStatusTip("添加图片水印")
        image_watermark_action.triggered.connect(self.add_image_watermark)
        watermark_menu.addAction(image_watermark_action)

        # 模板菜单
        template_menu = menubar.addMenu("模板(&T)")

        # 保存模板
        save_template_action = QAction(QIcon("resources/icons/save_template.png"), "保存模板(&S)", self)
        save_template_action.setShortcut("Ctrl+S")
        save_template_action.setStatusTip("保存当前水印设置为一个模板")
        save_template_action.triggered.connect(self.save_template)
        template_menu.addAction(save_template_action)

        # 加载模板
        load_template_action = QAction(QIcon("resources/icons/load_template.png"), "加载模板(&L)", self)
        load_template_action.setShortcut("Ctrl+O")
        load_template_action.setStatusTip("加载已保存的水印模板")
        load_template_action.triggered.connect(self.load_template)
        template_menu.addAction(load_template_action)

        # 帮助菜单
        help_menu = menubar.addMenu("帮助(&H)")

        # 用户手册
        manual_action = QAction(QIcon("resources/icons/manual.png"), "用户手册(&M)", self)
        manual_action.setShortcut("F1")
        manual_action.setStatusTip("查看用户手册")
        manual_action.triggered.connect(self.show_manual)
        help_menu.addAction(manual_action)

        help_menu.addSeparator()

        # 关于
        about_action = QAction(QIcon("resources/icons/about.png"), "关于(&A)", self)
        about_action.setStatusTip("关于本应用程序")
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def connect_signals(self):
        """连接组件信号"""
        # 图片选择信号
        self.image_view.image_selected.connect(self.preview_area.update_preview)

        # 水印参数变化信号
        self.watermark_panel.watermark_params_changed.connect(self.preview_area.update_preview)

    def import_images(self):
        """导入图片"""
        # 实现图片导入逻辑
        self.status_bar.showMessage("导入图片功能待实现")
        QMessageBox.information(self, "提示", "图片导入功能待实现")

    def export_images(self):
        """导出图片"""
        # 实现图片导出逻辑
        self.status_bar.showMessage("导出图片功能待实现")
        QMessageBox.information(self, "提示", "图片导出功能待实现")

    def undo_action(self):
        """撤销操作"""
        self.status_bar.showMessage("撤销功能待实现")
        QMessageBox.information(self, "提示", "撤销功能待实现")

    def show_preferences(self):
        """显示偏好设置"""
        self.status_bar.showMessage("偏好设置功能待实现")
        QMessageBox.information(self, "提示", "偏好设置功能待实现")

    def add_text_watermark(self):
        """添加文本水印"""
        self.status_bar.showMessage("文本水印功能待实现")
        QMessageBox.information(self, "提示", "文本水印功能待实现")

    def add_image_watermark(self):
        """添加图片水印"""
        self.status_bar.showMessage("图片水印功能待实现")
        QMessageBox.information(self, "提示", "图片水印功能待实现")

    def save_template(self):
        """保存模板"""
        self.status_bar.showMessage("保存模板功能待实现")
        QMessageBox.information(self, "提示", "保存模板功能待实现")

    def load_template(self):
        """加载模板"""
        self.status_bar.showMessage("加载模板功能待实现")
        QMessageBox.information(self, "提示", "加载模板功能待实现")

    def show_manual(self):
        """显示用户手册"""
        self.status_bar.showMessage("用户手册功能待实现")
        QMessageBox.information(self, "提示", "用户手册功能待实现")

    def show_about(self):
        """显示关于对话框"""
        QMessageBox.about(self, "关于照片水印应用", 
                         "照片水印应用 v1.0\n\n"
                         "一款简单易用的照片水印添加工具\n\n"
                         "© 2023 版权所有")
