"""
图片预览区域组件
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from PyQt6.QtGui import QPixmap, QPainter, QColor, QPen, QBrush, QCursor
from PyQt6.QtCore import Qt, QPoint, pyqtSignal

from PIL import Image
from PIL.ImageQt import ImageQt

from core.watermark_processor import WatermarkProcessor


class PreviewArea(QWidget):
    """图片预览区域组件"""

    def __init__(self):
        super().__init__()
        self.current_image = None
        self.watermark_image = None
        self.watermark_position = 'center'
        self.watermark_params = None
        self.dragging = False
        self.drag_start = None
        self.watermark_processor = WatermarkProcessor()

        # 设置布局
        self.layout = QVBoxLayout(self)

        # 预览标签
        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setMinimumSize(400, 400)
        self.preview_label.setStyleSheet("border: 1px solid #ccc; background-color: #f5f5f5;")
        self.layout.addWidget(self.preview_label)

        # 启用鼠标事件
        self.setMouseTracking(True)
        self.preview_label.setMouseTracking(True)

    def update_preview(self, image, watermark_params=None):
        """更新预览"""
        if image is None:
            self.preview_label.clear()
            return

        try:
            # 保存当前图像和参数
            self.current_image = image
            self.watermark_params = watermark_params

            # 创建预览图像副本
            preview_image = image.copy()

            # 如果有水印参数，应用水印
            if watermark_params:
                # 应用水印
                preview_image = self.watermark_processor.apply_watermark(
                    preview_image,
                    watermark_params
                )

            # 转换为QPixmap并显示
            qimage = ImageQt(preview_image)
            pixmap = QPixmap.fromImage(qimage)

            # 显示预览
            self.preview_label.setPixmap(pixmap)
            self.preview_label.setScaledContents(True)
        except Exception as e:
            print(f"预览更新失败: {str(e)}")
            # 如果水印应用失败，至少显示原始图片
            if image:
                try:
                    qimage = ImageQt(image)
                    pixmap = QPixmap.fromImage(qimage)
                    self.preview_label.setPixmap(pixmap)
                    self.preview_label.setScaledContents(True)
                except:
                    # 如果连原始图片都无法显示，清空预览
                    self.preview_label.clear()

    def mousePressEvent(self, event):
        """处理鼠标按下事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            # 检查是否点击在水印上
            if self.is_watermark_clicked(event.pos()):
                self.dragging = True
                self.drag_start = event.pos()
                self.setCursor(Qt.CursorShape.ClosedHandCursor)

    def mouseReleaseEvent(self, event):
        """处理鼠标释放事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            self.drag_start = None
            self.setCursor(Qt.CursorShape.ArrowCursor)

    def mouseMoveEvent(self, event):
        """处理鼠标移动事件"""
        if self.dragging and self.drag_start:
            # 计算移动距离
            delta = event.pos() - self.drag_start

            # 更新水印位置
            if self.watermark_params:
                # 获取图片和水印的实际尺寸
                img_width, img_height = self.current_image.size
                wm_width, wm_height = self.get_watermark_size()

                # 计算新位置
                current_pos = self.get_watermark_position()
                new_x = current_pos[0] + delta.x()
                new_y = current_pos[1] + delta.y()

                # 限制在图片范围内
                new_x = max(0, min(new_x, img_width - wm_width))
                new_y = max(0, min(new_y, img_height - wm_height))

                # 更新水印位置参数
                self.watermark_params['position'] = (new_x, new_y)

                # 更新预览
                self.update_preview(self.current_image, self.watermark_params)

                # 更新起始点
                self.drag_start = event.pos()

    def is_watermark_clicked(self, pos):
        """检查点击位置是否在水印上"""
        if not self.watermark_params or not self.current_image:
            return False

        # 获取图片和水印的实际尺寸
        img_width, img_height = self.current_image.size
        wm_width, wm_height = self.get_watermark_size()

        # 获取水印位置
        pos_x, pos_y = self.get_watermark_position()

        # 检查点击位置是否在水印范围内
        return (pos_x <= pos.x() <= pos_x + wm_width and
                pos_y <= pos.y() <= pos_y + wm_height)

    def get_watermark_size(self):
        """获取水印尺寸"""
        if not self.watermark_params:
            return 0, 0

        if self.watermark_params['type'] == 'text':
            # 对于文本水印，需要根据文本内容计算尺寸
            text = self.watermark_params['text']
            font_size = self.watermark_params['font_size']
            # 这里简化处理，实际应该根据字体计算文本尺寸
            return font_size * len(text), font_size
        else:
            # 对于图片水印，使用设置的大小
            return self.watermark_params['width'], self.watermark_params['height']

    def get_watermark_position(self):
        """获取水印位置"""
        if not self.watermark_params:
            return (0, 0)

        position = self.watermark_params['position']
        if isinstance(position, str):
            # 如果是预设位置，计算实际坐标
            img_width, img_height = self.current_image.size
            wm_width, wm_height = self.get_watermark_size()

            if position == 'top-left':
                return (10, 10)
            elif position == 'top-right':
                return (img_width - wm_width - 10, 10)
            elif position == 'bottom-left':
                return (10, img_height - wm_height - 10)
            elif position == 'bottom-right':
                return (img_width - wm_width - 10, img_height - wm_height - 10)
            elif position == 'center':
                return ((img_width - wm_width) // 2, (img_height - wm_height) // 2)
            else:
                return (0, 0)
        else:
            # 如果是自定义位置，直接返回
            return position
