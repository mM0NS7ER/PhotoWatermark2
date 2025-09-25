"""
导出设置面板组件
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, 
    QPushButton, QSpinBox, QDoubleSpinBox, QLineEdit,
    QGroupBox, QCheckBox, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon


class ExportPanel(QWidget):
    """导出设置面板组件"""

    # 自定义信号：当导出参数变化时发出
    export_params_changed = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.export_params = {
            'output_folder': '',
            'file_format': 'JPEG',
            'quality': 90,
            'resize_width': 0,
            'resize_height': 0,
            'keep_aspect_ratio': True,
            'filename_pattern': '{original_name}_watermarked',
            'overwrite_existing': False
        }
        self.init_ui()

    def init_ui(self):
        """初始化用户界面"""
        # 主布局
        layout = QVBoxLayout(self)

        # 输出设置
        output_group = QGroupBox("输出设置")
        output_layout = QVBoxLayout()

        # 输出文件夹
        folder_layout = QHBoxLayout()
        folder_label = QLabel("输出文件夹:")
        self.folder_path = QLineEdit(self.export_params['output_folder'])
        self.folder_path.setReadOnly(True)

        browse_btn = QPushButton("浏览...")
        browse_btn.clicked.connect(self.browse_folder)

        folder_layout.addWidget(folder_label)
        folder_layout.addWidget(self.folder_path)
        folder_layout.addWidget(browse_btn)

        output_layout.addLayout(folder_layout)

        # 文件格式
        format_layout = QHBoxLayout()
        format_label = QLabel("文件格式:")
        self.format_combo = QComboBox()
        self.format_combo.addItems(["JPEG", "PNG", "BMP", "TIFF"])
        self.format_combo.setCurrentText(self.export_params['file_format'])
        self.format_combo.currentTextChanged.connect(self.on_format_changed)

        format_layout.addWidget(format_label)
        format_layout.addWidget(self.format_combo)

        output_layout.addLayout(format_layout)

        # JPEG质量
        quality_layout = QHBoxLayout()
        quality_label = QLabel("JPEG质量:")
        self.quality_spin = QSpinBox()
        self.quality_spin.setRange(1, 100)
        self.quality_spin.setValue(self.export_params['quality'])
        self.quality_spin.valueChanged.connect(self.on_quality_changed)

        quality_layout.addWidget(quality_label)
        quality_layout.addWidget(self.quality_spin)

        output_layout.addLayout(quality_layout)

        output_group.setLayout(output_layout)
        layout.addWidget(output_group)

        # 尺寸设置
        size_group = QGroupBox("尺寸设置")
        size_layout = QVBoxLayout()

        # 缩放选项
        resize_layout = QHBoxLayout()
        resize_label = QLabel("缩放:")
        self.width_spin = QSpinBox()
        self.width_spin.setRange(1, 10000)
        self.width_spin.setValue(self.export_params['resize_width'])
        self.width_spin.valueChanged.connect(self.on_size_changed)

        size_label = QLabel("×")

        self.height_spin = QSpinBox()
        self.height_spin.setRange(1, 10000)
        self.height_spin.setValue(self.export_params['resize_height'])
        self.height_spin.valueChanged.connect(self.on_size_changed)

        self.aspect_check = QCheckBox("保持宽高比")
        self.aspect_check.setChecked(self.export_params['keep_aspect_ratio'])
        self.aspect_check.stateChanged.connect(self.on_aspect_ratio_changed)

        resize_layout.addWidget(resize_label)
        resize_layout.addWidget(self.width_spin)
        resize_layout.addWidget(size_label)
        resize_layout.addWidget(self.height_spin)
        resize_layout.addWidget(self.aspect_check)

        size_layout.addLayout(resize_layout)

        size_group.setLayout(size_layout)
        layout.addWidget(size_group)

        # 文件名设置
        filename_group = QGroupBox("文件名设置")
        filename_layout = QVBoxLayout()

        # 文件名模式
        pattern_layout = QHBoxLayout()
        pattern_label = QLabel("文件名模式:")
        self.pattern_input = QLineEdit(self.export_params['filename_pattern'])
        self.pattern_input.textChanged.connect(self.on_pattern_changed)

        pattern_layout.addWidget(pattern_label)
        pattern_layout.addWidget(self.pattern_input)

        filename_layout.addLayout(pattern_layout)

        # 可用变量提示
        variables_label = QLabel("可用变量: {original_name}, {index}, {date}")
        filename_layout.addWidget(variables_label)

        # 覆盖选项
        self.overwrite_check = QCheckBox("覆盖已存在的文件")
        self.overwrite_check.setChecked(self.export_params['overwrite_existing'])
        self.overwrite_check.stateChanged.connect(self.on_overwrite_changed)

        filename_layout.addWidget(self.overwrite_check)

        filename_group.setLayout(filename_layout)
        layout.addWidget(filename_group)

        # 导出按钮
        export_btn = QPushButton("导出图片")
        export_btn.setIcon(QIcon("resources/icons/export.png"))
        export_btn.clicked.connect(self.export_images)
        export_btn.setStyleSheet("QPushButton { font-weight: bold; }")

        layout.addWidget(export_btn)

        # 添加弹性空间
        layout.addStretch()

        # 初始化参数更新
        self.update_export_params()

    def browse_folder(self):
        """浏览输出文件夹"""
        folder = QFileDialog.getExistingDirectory(
            self, "选择输出文件夹", 
            self.export_params['output_folder'] or "."
        )

        if folder:
            self.folder_path.setText(folder)
            self.export_params['output_folder'] = folder
            self.update_export_params()

    def on_format_changed(self, format):
        """处理文件格式变更"""
        self.export_params['file_format'] = format
        self.update_export_params()

    def on_quality_changed(self, quality):
        """处理JPEG质量变更"""
        self.export_params['quality'] = quality
        self.update_export_params()

    def on_size_changed(self):
        """处理尺寸变更"""
        self.export_params['resize_width'] = self.width_spin.value()
        self.export_params['resize_height'] = self.height_spin.value()

        # 如果保持宽高比被选中，自动调整另一个尺寸
        if self.export_params['keep_aspect_ratio'] and self.sender() == self.width_spin:
            # 根据宽度调整高度，保持宽高比
            original_width = self.export_params['resize_width']
            original_height = self.export_params['resize_height']

            if original_width > 0:
                ratio = original_height / original_width
                new_height = int(self.width_spin.value() * ratio)
                self.height_spin.setValue(new_height)
                self.export_params['resize_height'] = new_height
        elif self.export_params['keep_aspect_ratio'] and self.sender() == self.height_spin:
            # 根据高度调整宽度，保持宽高比
            original_width = self.export_params['resize_width']
            original_height = self.export_params['resize_height']

            if original_height > 0:
                ratio = original_width / original_height
                new_width = int(self.height_spin.value() * ratio)
                self.width_spin.setValue(new_width)
                self.export_params['resize_width'] = new_width

        self.update_export_params()

    def on_aspect_ratio_changed(self, state):
        """处理宽高比选项变更"""
        self.export_params['keep_aspect_ratio'] = bool(state)
        self.update_export_params()

    def on_pattern_changed(self, pattern):
        """处理文件名模式变更"""
        self.export_params['filename_pattern'] = pattern
        self.update_export_params()

    def on_overwrite_changed(self, state):
        """处理覆盖选项变更"""
        self.export_params['overwrite_existing'] = bool(state)
        self.update_export_params()

    def update_export_params(self):
        """更新导出参数并发出信号"""
        self.export_params_changed.emit(self.export_params)

    def export_images(self):
        """导出图片"""
        # 这里应该实现实际的图片导出逻辑
        # 简化处理，只显示提示信息
        if not self.export_params['output_folder']:
            # 这里应该显示错误提示
            QMessageBox.warning(self, "警告", "请先选择输出文件夹")
            return

        # 触发主窗口的导出功能
        # 通过查找主窗口对象来调用export_images方法
        main_window = None
        parent = self.parent()
        while parent is not None:
            if hasattr(parent, "export_images"):
                main_window = parent
                break
            parent = parent.parent()
            
        if main_window:
            main_window.export_images()
        else:
            QMessageBox.warning(self, "错误", "无法找到主窗口对象")
