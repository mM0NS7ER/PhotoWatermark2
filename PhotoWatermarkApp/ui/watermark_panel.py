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

        # 确保初始参数变化信号能够触发
        self.update_watermark_params()

    def init_ui(self):
        """初始化用户界面"""
        # 主布局
        layout = QVBoxLayout(self)

        # 初始化完成后，确保水印参数变化信号能够触发
        self.update_watermark_params()

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
        self.tabs = QTabWidget()

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

        # 特效选项卡
        effects_tab = QWidget()
        effects_layout = QVBoxLayout(effects_tab)

        # 特效选择
        effects_check_layout = QHBoxLayout()
        self.shadow_check = QCheckBox("阴影")
        self.shadow_check.stateChanged.connect(self.on_effects_changed)

        self.outline_check = QCheckBox("描边")
        self.outline_check.stateChanged.connect(self.on_effects_changed)

        effects_check_layout.addWidget(self.shadow_check)
        effects_check_layout.addWidget(self.outline_check)
        effects_layout.addLayout(effects_check_layout)

        # 特效参数选项卡
        self.effects_params_tabs = QTabWidget()

        # 阴影参数选项卡
        shadow_tab = QWidget()
        shadow_layout = QVBoxLayout(shadow_tab)

        # 阴影偏移
        shadow_offset_layout = QHBoxLayout()
        shadow_offset_label = QLabel("偏移:")
        self.shadow_offset_x = QSpinBox()
        self.shadow_offset_x.setRange(-20, 20)
        self.shadow_offset_x.setValue(2)
        self.shadow_offset_x.valueChanged.connect(self.on_shadow_offset_changed)

        shadow_offset_y_label = QLabel(", ")
        self.shadow_offset_y = QSpinBox()
        self.shadow_offset_y.setRange(-20, 20)
        self.shadow_offset_y.setValue(2)
        self.shadow_offset_y.valueChanged.connect(self.on_shadow_offset_changed)

        shadow_offset_layout.addWidget(shadow_offset_label)
        shadow_offset_layout.addWidget(self.shadow_offset_x)
        shadow_offset_layout.addWidget(shadow_offset_y_label)
        shadow_offset_layout.addWidget(self.shadow_offset_y)
        shadow_layout.addLayout(shadow_offset_layout)

        # 阴影颜色
        shadow_color_layout = QHBoxLayout()
        shadow_color_label = QLabel("颜色:")
        self.shadow_color_button = QPushButton()
        self.shadow_color_button.setStyleSheet("background-color: rgb(128, 128, 128);")
        self.shadow_color_button.clicked.connect(self.on_shadow_color_changed)
        shadow_color_layout.addWidget(shadow_color_label)
        shadow_color_layout.addWidget(self.shadow_color_button)
        shadow_layout.addLayout(shadow_color_layout)

        # 阴影透明度
        shadow_opacity_layout = QHBoxLayout()
        shadow_opacity_label = QLabel("透明度:")
        self.shadow_opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.shadow_opacity_slider.setRange(0, 100)
        self.shadow_opacity_slider.setValue(50)  # 默认50%
        self.shadow_opacity_slider.valueChanged.connect(self.on_shadow_opacity_changed)

        self.shadow_opacity_value = QLabel("50%")
        shadow_opacity_layout.addWidget(shadow_opacity_label)
        shadow_opacity_layout.addWidget(self.shadow_opacity_slider)
        shadow_opacity_layout.addWidget(self.shadow_opacity_value)
        shadow_layout.addLayout(shadow_opacity_layout)

        self.effects_params_tabs.addTab(shadow_tab, "阴影")

        # 描边参数选项卡
        outline_tab = QWidget()
        outline_layout = QVBoxLayout(outline_tab)

        # 描边宽度
        outline_width_layout = QHBoxLayout()
        outline_width_label = QLabel("宽度:")
        self.outline_width_spin = QSpinBox()
        self.outline_width_spin.setRange(1, 10)
        self.outline_width_spin.setValue(1)
        self.outline_width_spin.valueChanged.connect(self.on_outline_width_changed)
        outline_width_layout.addWidget(outline_width_label)
        outline_width_layout.addWidget(self.outline_width_spin)
        outline_layout.addLayout(outline_width_layout)

        # 描边颜色
        outline_color_layout = QHBoxLayout()
        outline_color_label = QLabel("颜色:")
        self.outline_color_button = QPushButton()
        self.outline_color_button.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.outline_color_button.clicked.connect(self.on_outline_color_changed)
        outline_color_layout.addWidget(outline_color_label)
        outline_color_layout.addWidget(self.outline_color_button)
        outline_layout.addLayout(outline_color_layout)

        # 描边透明度
        outline_opacity_layout = QHBoxLayout()
        outline_opacity_label = QLabel("透明度:")
        self.outline_opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.outline_opacity_slider.setRange(0, 100)
        self.outline_opacity_slider.setValue(50)  # 默认50%
        self.outline_opacity_slider.valueChanged.connect(self.on_outline_opacity_changed)

        self.outline_opacity_value = QLabel("50%")
        outline_opacity_layout.addWidget(outline_opacity_label)
        outline_opacity_layout.addWidget(self.outline_opacity_slider)
        outline_opacity_layout.addWidget(self.outline_opacity_value)
        outline_layout.addLayout(outline_opacity_layout)

        self.effects_params_tabs.addTab(outline_tab, "描边")

        # 只有至少启用一个特效时才显示特效参数选项卡
        self.effects_params_tabs.setEnabled(False)
        effects_layout.addWidget(self.effects_params_tabs)

        # 连接特效复选框状态改变事件
        self.shadow_check.stateChanged.connect(self.update_effects_tabs_state)
        self.outline_check.stateChanged.connect(self.update_effects_tabs_state)

        # 添加文本和特效选项卡到主选项卡 - 注意顺序已调整
        self.tabs.addTab(text_tab, "文本水印")
        self.tabs.addTab(effects_tab, "特效设置")

        layout.addWidget(self.tabs)

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

        # 添加图片选项卡到主选项卡
        self.tabs.addTab(image_tab, "图片水印")

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
        # 确保effects字典存在
        if 'effects' not in self.watermark_params:
            self.watermark_params['effects'] = {
                'shadow': False,
                'outline': False
            }

        # 更新特效状态
        shadow_enabled = self.shadow_check.isChecked()
        outline_enabled = self.outline_check.isChecked()

        # 如果启用阴影，确保它是一个字典而不是布尔值
        if shadow_enabled:
            if isinstance(self.watermark_params['effects']['shadow'], bool):
                self.watermark_params['effects']['shadow'] = {
                    'offset': (2, 2),
                    'color': (128, 128, 128),
                    'opacity': 0.5
                }
            # 更新UI控件值到参数字典
            self.watermark_params['effects']['shadow']['offset'] = (
                self.shadow_offset_x.value(),
                self.shadow_offset_y.value()
            )
            # 获取颜色按钮的背景色
            style = self.shadow_color_button.styleSheet()
            # 从样式表中提取RGB值
            if "rgb(" in style:
                rgb_str = style.split("rgb(")[1].split(");")[0]
                r, g, b = map(int, rgb_str.split(", "))
                self.watermark_params['effects']['shadow']['color'] = (r, g, b)
            self.watermark_params['effects']['shadow']['opacity'] = self.shadow_opacity_slider.value() / 100.0
        else:
            self.watermark_params['effects']['shadow'] = False

        # 如果启用描边，确保它是一个字典而不是布尔值
        if outline_enabled:
            if isinstance(self.watermark_params['effects']['outline'], bool):
                self.watermark_params['effects']['outline'] = {
                    'color': (255, 255, 255),
                    'width': 1,
                    'opacity': 0.5
                }
            # 更新UI控件值到参数字典
            self.watermark_params['effects']['outline']['width'] = self.outline_width_spin.value()
            # 获取颜色按钮的背景色
            style = self.outline_color_button.styleSheet()
            # 从样式表中提取RGB值
            if "rgb(" in style:
                rgb_str = style.split("rgb(")[1].split(");")[0]
                r, g, b = map(int, rgb_str.split(", "))
                self.watermark_params['effects']['outline']['color'] = (r, g, b)
            self.watermark_params['effects']['outline']['opacity'] = self.outline_opacity_slider.value() / 100.0
        else:
            self.watermark_params['effects']['outline'] = False

        self.update_watermark_params()
        self.update_effects_tabs_state()

    def update_effects_tabs_state(self):
        """更新特效选项卡的启用状态"""
        # 只有至少启用一个特效时才显示特效参数选项卡
        has_effects = self.shadow_check.isChecked() or self.outline_check.isChecked()
        self.effects_params_tabs.setEnabled(has_effects)

        # 如果启用了阴影，自动选择阴影选项卡
        if self.shadow_check.isChecked():
            self.effects_params_tabs.setCurrentIndex(0)  # 选择阴影选项卡
        # 如果没有启用阴影但启用了描边，选择描边选项卡
        elif self.outline_check.isChecked():
            self.effects_params_tabs.setCurrentIndex(1)  # 选择描边选项卡

    def on_position_changed(self, button):
        """处理位置变更"""
        for radio, value in self.position_buttons:
            if radio == button:
                self.watermark_params['position'] = value
                break
        self.update_watermark_params()

    def on_shadow_offset_changed(self):
        """处理阴影偏移变更"""
        if self.shadow_check.isChecked() and isinstance(self.watermark_params['effects']['shadow'], dict):
            self.watermark_params['effects']['shadow']['offset'] = (
                self.shadow_offset_x.value(),
                self.shadow_offset_y.value()
            )
            self.update_watermark_params()

    def on_shadow_color_changed(self):
        """处理阴影颜色变更"""
        color = QColorDialog.getColor()
        if color.isValid():
            self.shadow_color_button.setStyleSheet(f"background-color: {color.name()};")
            if self.shadow_check.isChecked() and isinstance(self.watermark_params['effects']['shadow'], dict):
                self.watermark_params['effects']['shadow']['color'] = (color.red(), color.green(), color.blue())
                self.update_watermark_params()

    def on_shadow_opacity_changed(self, value):
        """处理阴影透明度变更"""
        self.shadow_opacity_value.setText(f"{value}%")
        if self.shadow_check.isChecked() and isinstance(self.watermark_params['effects']['shadow'], dict):
            self.watermark_params['effects']['shadow']['opacity'] = value / 100.0
            self.update_watermark_params()

    def on_outline_width_changed(self):
        """处理描边宽度变更"""
        if self.outline_check.isChecked() and isinstance(self.watermark_params['effects']['outline'], dict):
            self.watermark_params['effects']['outline']['width'] = self.outline_width_spin.value()
            self.update_watermark_params()

    def on_outline_color_changed(self):
        """处理描边颜色变更"""
        color = QColorDialog.getColor()
        if color.isValid():
            self.outline_color_button.setStyleSheet(f"background-color: {color.name()};")
            if self.outline_check.isChecked() and isinstance(self.watermark_params['effects']['outline'], dict):
                self.watermark_params['effects']['outline']['color'] = (color.red(), color.green(), color.blue())
                self.update_watermark_params()

    def on_outline_opacity_changed(self, value):
        """处理描边透明度变更"""
        self.outline_opacity_value.setText(f"{value}%")
        if self.outline_check.isChecked() and isinstance(self.watermark_params['effects']['outline'], dict):
            self.watermark_params['effects']['outline']['opacity'] = value / 100.0
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

        # 如果当前是文本水印，确保特效参数正确设置
        if self.watermark_params['type'] == 'text':
            # 确保特效参数存在
            if 'effects' not in self.watermark_params:
                self.watermark_params['effects'] = {
                    'shadow': False,
                    'outline': False
                }

            # 确保阴影参数结构正确
            if self.watermark_params['effects'].get('shadow') is False:
                self.watermark_params['effects']['shadow'] = False
            elif isinstance(self.watermark_params['effects']['shadow'], dict):
                # 如果阴影特效启用但缺少参数，设置默认值
                if 'offset' not in self.watermark_params['effects']['shadow']:
                    self.watermark_params['effects']['shadow']['offset'] = (2, 2)
                if 'color' not in self.watermark_params['effects']['shadow']:
                    self.watermark_params['effects']['shadow']['color'] = (128, 128, 128)
                if 'opacity' not in self.watermark_params['effects']['shadow']:
                    self.watermark_params['effects']['shadow']['opacity'] = 0.5
            else:
                # 如果阴影是True但不是字典，创建默认字典
                self.watermark_params['effects']['shadow'] = {
                    'offset': (2, 2),
                    'color': (128, 128, 128),
                    'opacity': 0.5
                }

            # 确保描边参数结构正确
            if self.watermark_params['effects'].get('outline') is False:
                self.watermark_params['effects']['outline'] = False
            elif isinstance(self.watermark_params['effects']['outline'], dict):
                # 如果描边特效启用但缺少参数，设置默认值
                if 'color' not in self.watermark_params['effects']['outline']:
                    self.watermark_params['effects']['outline']['color'] = (255, 255, 255)
                if 'width' not in self.watermark_params['effects']['outline']:
                    self.watermark_params['effects']['outline']['width'] = 1
                if 'opacity' not in self.watermark_params['effects']['outline']:
                    self.watermark_params['effects']['outline']['opacity'] = 0.5
            else:
                # 如果描边是True但不是字典，创建默认字典
                self.watermark_params['effects']['outline'] = {
                    'color': (255, 255, 255),
                    'width': 1,
                    'opacity': 0.5
                }

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

            # 设置阴影参数
            if self.watermark_params['effects']['shadow'] and isinstance(self.watermark_params['effects']['shadow'], dict):
                # 设置阴影偏移
                offset = self.watermark_params['effects']['shadow'].get('offset', (2, 2))
                self.shadow_offset_x.setValue(offset[0])
                self.shadow_offset_y.setValue(offset[1])

                # 设置阴影颜色
                shadow_color = self.watermark_params['effects']['shadow'].get('color', (128, 128, 128))
                shadow_qcolor = QColor(shadow_color[0], shadow_color[1], shadow_color[2])
                self.shadow_color_button.setStyleSheet(f"background-color: {shadow_qcolor.name()};")

                # 设置阴影透明度
                shadow_opacity = int(self.watermark_params['effects']['shadow'].get('opacity', 0.5) * 100)
                self.shadow_opacity_slider.setValue(shadow_opacity)
                self.shadow_opacity_value.setText(f"{shadow_opacity}%")
            else:
                # 重置阴影参数为默认值
                self.shadow_offset_x.setValue(2)
                self.shadow_offset_y.setValue(2)
                self.shadow_color_button.setStyleSheet("background-color: rgb(128, 128, 128);")
                self.shadow_opacity_slider.setValue(50)
                self.shadow_opacity_value.setText("50%")

            # 设置描边参数
            if self.watermark_params['effects']['outline'] and isinstance(self.watermark_params['effects']['outline'], dict):
                # 设置描边宽度
                width = self.watermark_params['effects']['outline'].get('width', 1)
                self.outline_width_spin.setValue(width)

                # 设置描边颜色
                outline_color = self.watermark_params['effects']['outline'].get('color', (255, 255, 255))
                outline_qcolor = QColor(outline_color[0], outline_color[1], outline_color[2])
                self.outline_color_button.setStyleSheet(f"background-color: {outline_qcolor.name()};")

                # 设置描边透明度
                outline_opacity = int(self.watermark_params['effects']['outline'].get('opacity', 0.5) * 100)
                self.outline_opacity_slider.setValue(outline_opacity)
                self.outline_opacity_value.setText(f"{outline_opacity}%")
            else:
                # 重置描边参数为默认值
                self.outline_width_spin.setValue(1)
                self.outline_color_button.setStyleSheet("background-color: rgb(255, 255, 255);")
                self.outline_opacity_slider.setValue(50)
                self.outline_opacity_value.setText("50%")

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
