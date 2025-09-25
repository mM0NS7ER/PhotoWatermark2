"""
图片预览区域组件
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from PyQt6.QtGui import QPixmap, QPainter, QColor, QPen, QBrush, QCursor, QFont, QFontMetrics
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

        # 用于实时渲染的QPixmap
        self.preview_pixmap = None

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

            # 保存原始图像用于实时渲染
            self.original_image = image.copy()

            # 如果有水印参数，应用水印
            if watermark_params:
                # 应用水印
                preview_image = self.watermark_processor.apply_watermark(
                    preview_image,
                    watermark_params
                )

                # 保存处理后的图像
                self.processed_image = preview_image
            else:
                # 如果没有水印参数，清除处理后的图像
                self.processed_image = None

            # 转换为QPixmap并显示
            qimage = ImageQt(preview_image)
            self.preview_pixmap = QPixmap.fromImage(qimage)

            # 确保预览标签有内容
            if self.preview_pixmap.isNull():
                print("警告: 生成的预览图像为空")
                # 尝试直接使用原始图像
                qimage = ImageQt(image)
                self.preview_pixmap = QPixmap.fromImage(qimage)
                if self.preview_pixmap.isNull():
                    print("错误: 原始图像也无法转换为QPixmap")
                    return

            # 设置缩放模式以保持宽高比
            self.preview_label.setPixmap(self.preview_pixmap)
            self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.preview_label.setScaledContents(False)

            # 设置最小尺寸和最大尺寸
            self.preview_label.setMinimumSize(400, 400)

            # 如果图像比预览区域大，缩放图像以适应
            if self.preview_pixmap.width() > self.preview_label.width() or self.preview_pixmap.height() > self.preview_label.height():
                scaled_pixmap = self.preview_pixmap.scaled(
                    self.preview_label.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.preview_label.setPixmap(scaled_pixmap)
        except Exception as e:
            print(f"预览更新失败: {str(e)}")
            # 如果水印应用失败，至少显示原始图片
            if image:
                try:
                    qimage = ImageQt(image)
                    self.preview_pixmap = QPixmap.fromImage(qimage)
                    if not self.preview_pixmap.isNull():
                        self.preview_label.setPixmap(self.preview_pixmap)
                        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.preview_label.setScaledContents(False)
                    else:
                        # 如果连原始图片都无法显示，清空预览
                        self.preview_label.clear()
                except Exception as img_error:
                    print(f"显示原始图片失败: {str(img_error)}")
                    self.preview_label.clear()

    def mousePressEvent(self, event):
        """处理鼠标按下事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            # 检查是否点击在水印上
            if self.is_watermark_clicked(event.pos()):
                self.dragging = True
                self.drag_start = event.pos()
                self.setCursor(Qt.CursorShape.ClosedHandCursor)

                # 如果当前是预设位置，转换为自定义坐标
                if self.watermark_params and isinstance(self.watermark_params['position'], str):
                    img_width, img_height = self.current_image.size
                    wm_width, wm_height = self.get_watermark_size()

                    position = self.watermark_params['position']
                    if position == 'top-left':
                        pos_x, pos_y = 10, 10
                    elif position == 'top-right':
                        pos_x, pos_y = img_width - wm_width - 10, 10
                    elif position == 'bottom-left':
                        pos_x, pos_y = 10, img_height - wm_height - 10
                    elif position == 'bottom-right':
                        pos_x, pos_y = img_width - wm_width - 10, img_height - wm_height - 10
                    elif position == 'center':
                        pos_x, pos_y = (img_width - wm_width) // 2, (img_height - wm_height) // 2
                    else:
                        pos_x, pos_y = 10, 10

                    # 更新为自定义位置
                    self.watermark_params['position'] = (pos_x, pos_y)

    def mouseReleaseEvent(self, event):
        """处理鼠标释放事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            self.drag_start = None
            self.setCursor(Qt.CursorShape.ArrowCursor)

            # 重新应用最终水印
            if self.watermark_params and hasattr(self, 'processed_image'):
                self.update_preview(self.original_image, self.watermark_params)

    def mouseMoveEvent(self, event):
        """处理鼠标移动事件"""
        # 确保当前图像存在
        if not self.current_image:
            return

        if self.dragging and self.drag_start:
            # 计算移动距离
            delta = event.pos() - self.drag_start

            # 更新水印位置
            if self.watermark_params:
                try:
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

                    # 实时更新预览
                    self.update_preview(self.current_image, self.watermark_params)

                    # 更新起始点
                    self.drag_start = event.pos()
                except Exception as e:
                    print(f"鼠标移动事件处理失败: {str(e)}")
                    self.dragging = False
                    self.drag_start = None
                    self.setCursor(Qt.CursorShape.ArrowCursor)
        else:
            # 如果没有拖动，但鼠标在水印上，改变光标形状
            if self.watermark_params and self.is_watermark_clicked(event.pos()):
                self.setCursor(Qt.CursorShape.OpenHandCursor)
            else:
                self.setCursor(Qt.CursorShape.ArrowCursor)

    def is_watermark_clicked(self, pos):
        """检查点击位置是否在水印上"""
        if not self.watermark_params or not self.current_image:
            return False

        # 获取图片和水印的实际尺寸
        img_width, img_height = self.current_image.size
        wm_width, wm_height = self.get_watermark_size()

        # 获取水印位置
        pos_x, pos_y = self.get_watermark_position()

        # 获取缩放后的实际位置
        scaled_pos = self.get_scaled_position(pos)
        scaled_pos_x, scaled_pos_y = scaled_pos

        # 检查点击位置是否在水印范围内
        return (pos_x <= scaled_pos_x <= pos_x + wm_width and
                pos_y <= scaled_pos_y <= pos_y + wm_height)

    def get_watermark_size(self):
        """获取水印尺寸"""
        if not self.watermark_params:
            return 0, 0

        if self.watermark_params['type'] == 'text':
            # 对于文本水印，需要根据文本内容计算尺寸
            text = self.watermark_params['text']
            font_size = self.watermark_params['font_size']

            # 使用QFontMetrics更准确地计算文本尺寸
            font = QFont(self.watermark_params['font'], font_size)
            font_metrics = QFontMetrics(font)
            # 在PyQt6中，width方法已被替换为horizontalAdvance
            text_width = font_metrics.horizontalAdvance(text)
            text_height = font_metrics.height()

            return text_width, text_height
        else:
            # 对于图片水印，使用设置的大小
            return self.watermark_params['width'], self.watermark_params['height']

    def get_watermark_position(self):
        """获取水印位置"""
        if not self.watermark_params or not self.current_image:
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

    def get_scaled_position(self, pos):
        """获取在预览图上缩放后的实际位置"""
        if not self.preview_pixmap or not self.current_image:
            return pos

        # 计算缩放比例
        preview_width = self.preview_pixmap.width()
        preview_height = self.preview_pixmap.height()

        img_width, img_height = self.current_image.size

        # 计算实际显示尺寸（保持宽高比）
        display_width = self.preview_label.width()
        display_height = self.preview_label.height()

        if display_width == 0 or display_height == 0:
            return pos

        # 计算实际显示的图片尺寸
        if preview_width / preview_height > display_width / display_height:
            # 以宽度为准
            scale = display_width / preview_width
            actual_display_height = int(preview_height * scale)
            y_offset = (display_height - actual_display_height) // 2
            x_offset = 0
        else:
            # 以高度为准
            scale = display_height / preview_height
            actual_display_width = int(preview_width * scale)
            x_offset = (display_width - actual_display_width) // 2
            y_offset = 0

        # 转换鼠标坐标到实际图片坐标
        if x_offset > 0:
            scaled_x = int((pos.x() - x_offset) / scale)
        else:
            scaled_x = int(pos.x() / scale)

        if y_offset > 0:
            scaled_y = int((pos.y() - y_offset) / scale)
        else:
            scaled_y = int(pos.y() / scale)

        return (scaled_x, scaled_y)
