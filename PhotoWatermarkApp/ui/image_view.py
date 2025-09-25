"""
图片列表视图组件
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QLabel,
    QPushButton, QScrollArea, QFileDialog, QMessageBox
)
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt, pyqtSignal, QSize

from data.image_storage import ImageStorage


class ImageView(QWidget):
    """图片列表视图组件"""

    # 自定义信号：当图片被选中时发出
    image_selected = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.image_storage = None  # 将在主窗口中设置
        self.current_image = None
        self.init_ui()
        
    def set_image_storage(self, storage):
        """设置图片存储实例"""
        self.image_storage = storage

    def init_ui(self):
        """初始化用户界面"""
        # 主布局
        layout = QVBoxLayout(self)

        # 顶部工具栏
        toolbar_layout = QHBoxLayout()

        # 导入按钮
        import_btn = QPushButton("导入图片")
        import_btn.setIcon(QIcon("resources/icons/import.png"))
        import_btn.setToolTip("导入一张或多张图片")
        import_btn.clicked.connect(self.import_images)
        toolbar_layout.addWidget(import_btn)

        # 清空按钮
        clear_btn = QPushButton("清空列表")
        clear_btn.setIcon(QIcon("resources/icons/clear.png"))
        clear_btn.setToolTip("清空当前图片列表")
        clear_btn.clicked.connect(self.clear_list)
        toolbar_layout.addWidget(clear_btn)

        toolbar_layout.addStretch()

        layout.addLayout(toolbar_layout)

        # 图片列表区域
        self.image_list = QListWidget()
        self.image_list.setIconSize(QSize(100, 100))
        self.image_list.setViewMode(QListWidget.ViewMode.IconMode)
        self.image_list.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.image_list.setGridSize(QSize(120, 140))
        self.image_list.setSpacing(10)

        # 连接选择信号
        self.image_list.itemClicked.connect(self.on_image_selected)

        # 添加到布局
        layout.addWidget(self.image_list)

    def import_images(self):
        """导入图片"""
        # 打开文件选择对话框
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setNameFilter("图片文件 (*.jpg *.jpeg *.png *.bmp *.tiff)")

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                # 加载选中的图片
                loaded_count = 0
                for file_path in selected_files:
                    if self.image_storage.load_image(file_path):
                        # 添加到列表
                        item = QListWidgetItem(QIcon(file_path), file_path)
                        self.image_list.addItem(item)
                        loaded_count += 1

                # 显示结果信息
                if loaded_count > 0:
                    self.show_status_message(f"成功导入 {loaded_count} 张图片")
                else:
                    QMessageBox.warning(self, "导入失败", "没有成功导入任何图片")

    def clear_list(self):
        """清空图片列表"""
        reply = QMessageBox.question(
            self, "确认清空",
            "确定要清空当前图片列表吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.image_list.clear()
            self.image_storage.clear()
            self.current_image = None
            self.image_selected.emit(None)
            self.show_status_message("图片列表已清空")

    def on_image_selected(self, item):
        """处理图片选择事件"""
        if item:
            file_path = item.text()
            image = self.image_storage.get_image(file_path)

            if image:
                self.current_image = image
                self.image_selected.emit(image)
                self.show_status_message(f"已选择: {file_path}")
            else:
                QMessageBox.warning(self, "加载失败", f"无法加载图片: {file_path}")

    def get_selected_image(self):
        """获取当前选中的图片"""
        return self.current_image

    def get_selected_image_path(self):
        """获取当前选中图片的路径"""
        if self.current_image:
            # 获取当前选中的列表项
            selected_items = self.image_list.selectedItems()
            if selected_items:
                return selected_items[0].text()
        return None

    def show_status_message(self, message):
        """显示状态消息"""
        # 尝试获取主窗口并显示状态消息
        main_window = self
        while main_window.parent():
            main_window = main_window.parent()

        # 尝试查找状态栏
        if hasattr(main_window, 'status_bar'):
            main_window.status_bar.showMessage(message)