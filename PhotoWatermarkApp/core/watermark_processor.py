"""
水印处理模块
"""

from typing import Dict, Optional, Tuple, Union
from PIL import Image, ImageDraw, ImageFont, ImageColor

import os


class WatermarkProcessor:
    """水印处理模块，负责文本和图片水印的生成和应用"""

    def __init__(self):
        pass

    def apply_watermark(self, image: Image.Image, watermark_params: Dict) -> Image.Image:
        """
        应用水印到图片

        Args:
            image: PIL图片对象
            watermark_params: 水印参数字典

        Returns:
            应用水印后的图片对象
        """
        # 创建图片副本
        result_image = image.copy()

        # 根据水印类型创建水印
        if watermark_params['type'] == 'text':
            watermark = self.create_text_watermark(watermark_params)
        else:  # image watermark
            watermark = self.create_image_watermark(watermark_params)

        # 应用水印到图片
        if watermark:
            # 获取水印位置
            position = watermark_params['position']

            # 计算实际位置
            img_width, img_height = image.size
            wm_width, wm_height = watermark.size

            if isinstance(position, str):
                # 预设位置
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
            else:
                # 自定义位置
                pos_x, pos_y = position

            # 合并图像
            result_image.paste(watermark, (pos_x, pos_y), watermark)

        return result_image

    def create_text_watermark(self, params: Dict) -> Optional[Image.Image]:
        """
        创建文本水印

        Args:
            params: 文本水印参数

        Returns:
            文本水印图片对象
        """
        try:
            # 获取参数
            text = params.get('text', '水印')
            font_path = params.get('font', 'Arial')
            font_size = params.get('font_size', 24)
            color = params.get('color', (0, 0, 0))  # RGB颜色
            opacity = params.get('opacity', 0.7)
            effects = params.get('effects', {})

            # 创建透明背景图像
            dummy_image = Image.new('RGBA', (1, 1))
            draw = ImageDraw.Draw(dummy_image)

            # 获取字体
            try:
                if os.path.exists(font_path):
                    font = ImageFont.truetype(font_path, font_size)
                else:
                    font = ImageFont.load_default()
            except:
                font = ImageFont.load_default()

            # 获取文本尺寸 (使用新版本Pillow API)
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

            # 创建实际大小的图像
            watermark = Image.new('RGBA', (text_width, text_height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(watermark)

            # 应用文本效果
            if effects:
                if 'shadow' in effects and effects['shadow']:
                    # 添加阴影效果
                    shadow_offset = effects['shadow'].get('offset', (2, 2))
                    shadow_color = effects['shadow'].get('color', (128, 128, 128))
                    shadow_opacity = int(opacity * effects['shadow'].get('opacity', 0.5))

                    # 绘制阴影
                    draw.text(
                        (shadow_offset[0], shadow_offset[1]),
                        text,
                        font=font,
                        fill=shadow_color + (shadow_opacity,)
                    )

                if 'outline' in effects and effects['outline']:
                    # 添加描边效果
                    outline_color = effects['outline'].get('color', (255, 255, 255))
                    outline_width = effects['outline'].get('width', 1)
                    outline_opacity = int(opacity * effects['outline'].get('opacity', 0.5))

                    # 绘制描边
                    for dx in range(-outline_width, outline_width + 1):
                        for dy in range(-outline_width, outline_width + 1):
                            if dx == 0 and dy == 0:
                                continue
                            draw.text(
                                (dx, dy),
                                text,
                                font=font,
                                fill=outline_color + (outline_opacity,)
                            )

            # 绘制文本
            draw.text((0, 0), text, font=font, fill=color + (int(opacity * 255),))

            return watermark

        except Exception as e:
            print(f"创建文本水印失败: {str(e)}")
            return None

    def create_image_watermark(self, params: Dict) -> Optional[Image.Image]:
        """
        创建图片水印

        Args:
            params: 图片水印参数

        Returns:
            图片水印图片对象
        """
        try:
            # 获取参数
            image_path = params.get('image')
            width = params.get('width', 200)
            height = params.get('height', 100)
            opacity = params.get('opacity', 0.7)

            if not image_path or not os.path.exists(image_path):
                print("图片水印路径无效")
                return None

            # 加载图片
            watermark = Image.open(image_path)

            # 调整大小
            watermark = watermark.resize((width, height), Image.Resampling.LANCZOS)

            # 转换为RGBA模式
            if watermark.mode != 'RGBA':
                watermark = watermark.convert('RGBA')

            # 调整透明度
            if opacity < 1.0:
                alpha = watermark.split()[3]
                alpha = alpha.point(lambda p: p * opacity)
                watermark.putalpha(alpha)

            return watermark

        except Exception as e:
            print(f"创建图片水印失败: {str(e)}")
            return None

    def create_template(self, params: Dict) -> Dict:
        """
        创建水印模板

        Args:
            params: 水印参数

        Returns:
            水印模板字典
        """
        # 创建模板的深拷贝，避免引用外部对象
        template = {}

        # 复制基本参数
        for key, value in params.items():
            if isinstance(value, dict):
                # 深拷贝字典
                template[key] = {}
                for k, v in value.items():
                    if isinstance(v, (list, tuple)):
                        template[key][k] = list(v)
                    else:
                        template[key][k] = v
            else:
                template[key] = value

        return template
