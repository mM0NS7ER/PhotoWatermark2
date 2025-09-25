"""
水印控制面板组件
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, 
    QPushButton, QSpinBox, QDoubleSpinBox, QColorDialog,
    QGroupBox, QTabWidget, QRadioButton, QButtonGroup,
    QLineEdit, QCheckBox, QSlider
)
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtCore import Qt, pyqtSignal

from data.template_storage import TemplateStorage


class WatermarkPanel(QWidget):
    """水印控制面板组件"""

    # 自定义信号：当水印参数变化时发出
    watermark_params_changed = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.watermark_type = 'text'  # 默认为文本水印
        self.watermark_params = {
            'type': 'text',
            'text': '水印',
            'font': 'Arial',
            'font_size': 24,
            'color': (0, 0, 0),  # RGB颜色
            'opacity': 0.7,
            'position': 'center',
            'effects': {
                'shadow': False,
                'outline': False
            }
        }
        self.template_storage = TemplateStorage()
        self.init_ui()

    def init_ui(self):
        """初始化用户界面"""
        # 主布局
        layout = QVBoxLayout(self)

        # 水印类型选择
        type_layout = QHBoxLayout()
        type_label = QLabel("水印类型:")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["文本水印", "图片水印"])
        self.type_combo.currentIndexChanged.connect(self.on_type_changed)
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.type_combo)
        layout.addLayout(type_layout)

        # 创建选项卡
        tabs = QTabWidget()

        # 文本水印选项卡
        text_tab = QWidget()
        text_layout = QVBoxLayout(text_tab)

        # 文本内容
        text_group = QGroupBox("文本设置")
        text_group_layout = QVBoxLayout()

        text_content_layout = QHBoxLayout()
        text_content_label = QLabel("内容:")
        self.text_input = QLineEdit(self.watermark_params['text'])
        self.text_input.textChanged.connect(self.on_text_changed)
        text_content_layout.addWidget(text_content_label)
        text_content_layout.addWidget(self.text_input)
        text_group_layout.addLayout(text_content_layout)

        # 字体设置
        font_layout = QHBoxLayout()
        font_label = QLabel("字体:")
        self.font_combo = QComboBox()
        self.font_combo.addItems(["Arial", "Times New Roman", "宋体", "黑体", "楷体"])
        # 确保当前字体在列表中
        fonts = [self.font_combo.itemText(i) for i in range(self.font_combo.count())]
        if self.watermark_params['font'] in fonts:
            self.font_combo.setCurrentText(self.watermark_params['font'])
        else:
            self.font_combo.setCurrentText("Arial")  # 默认字体
        self.font_combo.currentTextChanged.connect(self.on_font_changed)

        font_size_layout = QHBoxLayout()
        font_size_label = QLabel("大小:")
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 200)
        self.font_size_spin.setValue(self.watermark_params['font_size'])
        self.font_size_spin.valueChanged.connect(self.on_font_size_changed)

        font_layout.addWidget(font_label)
        font_layout.addWidget(self.font_combo)
        font_size_layout.addWidget(font_size_label)
        font_size_layout.addWidget(self.font_size_spin)

        text_group_layout.addLayout(font_layout)
        text_group_layout.addLayout(font_size_layout)

        # 颜色设置
        color_layout = QHBoxLayout()
        color_label = QLabel("颜色:")
        self.color_button = QPushButton()
        self.color_button.setStyleSheet(f"background-color: rgb({self.watermark_params['color'][0]}, {self.watermark_params['color'][1]}, {self.watermark_params['color'][2]});")
        self.color_button.clicked.connect(self.on_color_changed)
        color_layout.addWidget(color_label)
        color_layout.addWidget(self.color_button)
        text_group_layout.addLayout(color_layout)

        # 透明度设置
        opacity_layout = QHBoxLayout()
        opacity_label = QLabel("透明度:")
        self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.opacity_slider.setRange(0, 100)
        self.opacity_slider.setValue(int(self.watermark_params['opacity'] * 100))
        self.opacity_slider.valueChanged.connect(self.on_opacity_changed)
        
        self.opacity_value = QLabel(f"{int(self.watermark_params['opacity'] * 100)}%")
        
        opacity_layout.addWidget(opacity_label)
        opacity_layout.addWidget(self.opacity_slider)
        opacity_layout.addWidget(self.opacity_value)
        text_group_layout.addLayout(opacity_layout)

        # 设置组的布局并添加到文本布局
        text_group.setLayout(text_group_layout)
        text_layout.addWidget(text_group)

        # 特效设置
        effects_group = QGroupBox("特效设置")
        effects_layout = QVBoxLayout()

        # 创建水平布局来放置特效选项
        effects_check_layout = QHBoxLayout()
        
        self.shadow_check = QCheckBox("阴影")
        self.shadow_check.stateChanged.connect(self.on_effects_changed)
        
        self.outline_check = QCheckBox("描边")
        self.outline_check.stateChanged.connect(self.on_effects_changed)
        
        # 将特效选项添加到水平布局
        effects_check_layout.addWidget(self.shadow_check)
        effects_check_layout.addWidget(self.outline_check)

        # 将水平布局添加到主布局
        effects_layout.addLayout(effects_check_layout)

        effects_group.setLayout(effects_layout)
        text_layout.addWidget(effects_group)

        # 位置设置
        position_group = QGroupBox("位置设置")
        position_layout = QVBoxLayout()

        position_options = [
            ("左上角", "top-left"),
            ("右上角", "top-right")
        ]
        
        self.position_group = QButtonGroup()
        self.position_buttons = []
        
        # 第一行：两个选项
        row1_layout = QHBoxLayout()
        for text, value in position_options:
            radio = QRadioButton(text)
            self.position_group.addButton(radio)
            self.position_buttons.append((radio, value))
            row1_layout.addWidget(radio)
        position_layout.addLayout(row1_layout)
        
        # 第二行：两个选项
        position_options = [
            ("左下角", "bottom-left"),
            ("右下角", "bottom-right")
        ]
        row2_layout = QHBoxLayout()
        for text, value in position_options:
            radio = QRadioButton(text)
            self.position_group.addButton(radio)
            self.position_buttons.append((radio, value))
            row2_layout.addWidget(radio)
        position_layout.addLayout(row2_layout)
        
        # 第三行：一个选项（居中）
        position_options = [
            ("居中", "center")
        ]
        row3_layout = QHBoxLayout()
        for text, value in position_options:
            radio = QRadioButton(text)
            self.position_group.addButton(radio)
            self.position_buttons.append((radio, value))
            row3_layout.addWidget(radio)
        position_layout.addLayout(row3_layout)

        # 设置默认选中
        for radio, value in self.position_buttons:
            if value == self.watermark_params['position']:
                radio.setChecked(True)
                break

        self.position_group.buttonClicked.connect(self.on_position_changed)

        position_group.setLayout(position_layout)
        text_layout.addWidget(position_group)

        # 添加文本选项卡
        tabs.addTab(text_tab, "文本水印")

        # 图片水印选项卡
        image_tab = QWidget()
        image_layout = QVBoxLayout(image_tab)

        # 图片选择
        image_select_layout = QHBoxLayout()
        image_select_label = QLabel("图片:")
        self.image_path_label = QLabel("未选择")
        self.image_select_btn = QPushButton("选择图片")
        self.image_select_btn.clicked.connect(self.on_image_selected)
        image_select_layout.addWidget(image_select_label)
        image_select_layout.addWidget(self.image_path_label)
        image_select_layout.addWidget(self.image_select_btn)
        image_layout.addLayout(image_select_layout)

        # 图片尺寸
        image_size_layout = QHBoxLayout()
        image_size_label = QLabel("尺寸:")
        self.image_width_spin = QSpinBox()
        self.image_width_spin.setRange(10, 2000)
        self.image_width_spin.setValue(200)
        self.image_width_spin.valueChanged.connect(self.on_image_size_changed)

        size_label = QLabel("×")

        self.image_height_spin = QSpinBox()
        self.image_height_spin.setRange(10, 2000)
        self.image_height_spin.setValue(100)
        self.image_height_spin.valueChanged.connect(self.on_image_size_changed)

        image_size_layout.addWidget(image_size_label)
        image_size_layout.addWidget(self.image_width_spin)
        image_size_layout.addWidget(size_label)
        image_size_layout.addWidget(self.image_height_spin)
        image_layout.addLayout(image_size_layout)

        # 透明度设置（创建新的透明度布局）
        image_opacity_layout = QHBoxLayout()
        image_opacity_label = QLabel("透明度:")
        self.image_opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.image_opacity_slider.setRange(0, 100)
        self.image_opacity_slider.setValue(int(self.watermark_params['opacity'] * 100))
        self.image_opacity_slider.valueChanged.connect(self.on_opacity_changed)
        
        self.image_opacity_value = QLabel(f"{int(self.watermark_params['opacity'] * 100)}%")
        
        image_opacity_layout.addWidget(image_opacity_label)
        image_opacity_layout.addWidget(self.image_opacity_slider)
        image_opacity_layout.addWidget(self.image_opacity_value)
        image_layout.addLayout(image_opacity_layout)

        # 位置设置（创建新的位置设置组）
        image_position_group = QGroupBox("位置设置")
        image_position_layout = QVBoxLayout()
        
        position_options = [
            ("左上角", "top-left"),
            ("右上角", "top-right"),
            ("左下角", "bottom-left"),
            ("右下角", "bottom-right"),
            ("居中", "center")
        ]
        
        self.image_position_group = QButtonGroup()
        self.image_position_buttons = []
        
        for text, value in position_options:
            radio = QRadioButton(text)
            self.image_position_group.addButton(radio)
            self.image_position_buttons.append((radio, value))
            image_position_layout.addWidget(radio)
        
        # 设置默认选中
        for radio, value in self.image_position_buttons:
            if value == self.watermark_params['position']:
                radio.setChecked(True)
                break
        
        self.image_position_group.buttonClicked.connect(self.on_position_changed)
        
        image_position_group.setLayout(image_position_layout)
        image_layout.addWidget(image_position_group)

        # 添加图片选项卡
        tabs.addTab(image_tab, "图片水印")

        layout.addWidget(tabs)

        # 模板操作
        template_layout = QHBoxLayout()

        save_template_btn = QPushButton("保存模板")
        save_template_btn.clicked.connect(self.save_template)

        load_template_btn = QPushButton("加载模板")
        load_template_btn.clicked.connect(self.load_template)

        template_layout.addWidget(save_template_btn)
        template_layout.addWidget(load_template_btn)

        layout.addLayout(template_layout)

        # 添加弹性空间
        layout.addStretch()

        # 初始化参数更新
        self.update_watermark_params()

    def on_type_changed(self, index):
        """处理水印类型变更"""
        self.watermark_type = 'text' if index == 0 else 'image'
        self.watermark_params['type'] = self.watermark_type
        self.update_watermark_params()

    def on_text_changed(self, text):
        """处理文本内容变更"""
        self.watermark_params['text'] = text
        self.update_watermark_params()

    def on_font_changed(self, font):
        """处理字体变更"""
        self.watermark_params['font'] = font
        self.update_watermark_params()

    def on_font_size_changed(self, size):
        """处理字体大小变更"""
        self.watermark_params['font_size'] = size
        self.update_watermark_params()

    def on_color_changed(self):
        """处理颜色变更"""
        color = QColorDialog.getColor()
        if color.isValid():
            self.watermark_params['color'] = (color.red(), color.green(), color.blue())
            self.color_button.setStyleSheet(f"background-color: {color.name()};")
            self.update_watermark_params()

    def on_opacity_changed(self, value):
        """处理透明度变更"""
        opacity = value / 100.0
        self.watermark_params['opacity'] = opacity
        self.opacity_value.setText(f"{value}%")
        
        # 同时更新图片水印的透明度值显示
        if hasattr(self, 'image_opacity_value'):
            self.image_opacity_value.setText(f"{value}%")
            
        self.update_watermark_params()

    def on_effects_changed(self, state):
        """处理特效变更"""
        self.watermark_params['effects']['shadow'] = self.shadow_check.isChecked()
        self.watermark_params['effects']['outline'] = self.outline_check.isChecked()
        self.update_watermark_params()

    def on_position_changed(self, button):
        """处理位置变更"""
        for radio, value in self.position_buttons:
            if radio == button:
                self.watermark_params['position'] = value
                break
        self.update_watermark_params()

    def on_image_selected(self):
        """处理图片选择"""
        # 这里应该实现图片选择逻辑
        # 简化处理，直接设置一个示例图片路径
        self.watermark_params['image'] = "example_watermark.png"
        self.image_path_label.setText("已选择图片")
        self.update_watermark_params()

    def on_image_size_changed(self):
        """处理图片尺寸变更"""
        self.watermark_params['width'] = self.image_width_spin.value()
        self.watermark_params['height'] = self.image_height_spin.value()
        self.update_watermark_params()

    def update_watermark_params(self):
        """更新水印参数并发出信号"""
        self.watermark_params_changed.emit(self.watermark_params)

    def save_template(self):
        """保存水印模板"""
        name, ok = self.template_storage.get_template_name()
        if ok and name:
            self.template_storage.save_template(name, self.watermark_params)
            self.show_status_message(f"模板 '{name}' 已保存")

    def load_template(self):
        """加载水印模板"""
        templates = self.template_storage.list_templates()
        if not templates:
            self.show_status_message("没有可用的模板")
            return

        name, ok = self.template_storage.select_template(templates)
        if ok and name:
            template = self.template_storage.load_template(name)
            if template:
                self.watermark_params = template
                self.apply_template_to_ui()
                self.update_watermark_params()
                self.show_status_message(f"已加载模板: {name}")

    def apply_template_to_ui(self):
        """将模板参数应用到UI控件"""
        # 设置水印类型
        self.type_combo.setCurrentIndex(0 if self.watermark_params['type'] == 'text' else 1)

        if self.watermark_params['type'] == 'text':
            # 设置文本相关参数
            self.text_input.setText(self.watermark_params['text'])
            self.font_combo.setCurrentText(self.watermark_params['font'])
            self.font_size_spin.setValue(self.watermark_params['font_size'])

            # 设置颜色
            r, g, b = self.watermark_params['color']
            color = QColor(r, g, b)
            self.color_button.setStyleSheet(f"background-color: {color.name()};")

            # 设置透明度
            opacity_value = int(self.watermark_params['opacity'] * 100)
            self.opacity_slider.setValue(opacity_value)
            self.opacity_value.setText(f"{opacity_value}%")

            # 设置特效
            self.shadow_check.setChecked(self.watermark_params['effects']['shadow'])
            self.outline_check.setChecked(self.watermark_params['effects']['outline'])

            # 设置位置
            for radio, value in self.position_buttons:
                if value == self.watermark_params['position']:
                    radio.setChecked(True)
                    break
        else:
            # 设置图片水印参数
            self.image_path_label.setText("已选择图片")
            self.image_width_spin.setValue(self.watermark_params['width'])
            self.image_height_spin.setValue(self.watermark_params['height'])

            # 设置透明度
            opacity_value = int(self.watermark_params['opacity'] * 100)
            # 同时更新文本水印和图片水印的透明度滑块
            self.opacity_slider.setValue(opacity_value)
            self.opacity_value.setText(f"{opacity_value}%")
            
            # 如果有图片水印的透明度滑块，也更新它
            if hasattr(self, 'image_opacity_slider'):
                self.image_opacity_slider.setValue(opacity_value)
                self.image_opacity_value.setText(f"{opacity_value}%")

            # 设置位置
            for radio, value in self.position_buttons:
                if value == self.watermark_params['position']:
                    radio.setChecked(True)
                    break
                    
            # 同时更新图片水印的位置选择
            if hasattr(self, 'image_position_buttons'):
                for radio, value in self.image_position_buttons:
                    if value == self.watermark_params['position']:
                        radio.setChecked(True)
                        break

    def get_watermark_params(self):
        """获取当前水印参数"""
        return self.watermark_params

    def show_status_message(self, message):
        """显示状态消息"""
        if self.parent():
            parent_window = self.parent()
            while parent_window.parent():
                parent_window = parent_window.parent()

            if hasattr(parent_window, 'status_bar'):
                parent_window.status_bar.showMessage(message)
