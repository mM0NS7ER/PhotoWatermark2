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
        watermark = None
        try:
            if watermark_params['type'] == 'text':
                watermark = self.create_text_watermark(watermark_params)
            else:  # image watermark
                watermark = self.create_image_watermark(watermark_params)
        except Exception as e:
            print(f"水印创建失败: {str(e)}")
            return result_image  # 返回原始图片副本

        # 应用水印到图片
        if watermark:
            try:
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
            except Exception as e:
                print(f"水印应用失败: {str(e)}")
                return result_image  # 返回原始图片副本

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
            font_size = params.get('font_size', 240)
            color = params.get('color', (0, 0, 0))  # RGB颜色
            opacity = params.get('opacity', 0.7)
            effects = params.get('effects', {})

            # 检查文本内容
            if not text or not text.strip():
                print("警告: 文本水印内容为空，使用默认文本")
                text = "水印"

            # 创建透明背景图像
            dummy_image = Image.new('RGBA', (1, 1))
            draw = ImageDraw.Draw(dummy_image)

            # 获取字体
            try:
                # 检查是否包含中文字符
                has_chinese = any('一' <= char <= '鿿' for char in text)

                if has_chinese:
                    # 如果包含中文字符，必须使用支持中文的字体
                    # 在Windows系统中，尝试查找常见的中文字体
                    import platform
                    system = platform.system()

                    if system == "Windows":
                        # Windows系统中常见的中文字体路径
                        chinese_fonts = {
                            "宋体": "C:/Windows/Fonts/simsun.ttc",
                            "黑体": "C:/Windows/Fonts/simhei.ttf",
                            "楷体": "C:/Windows/Fonts/simkai.ttf",
                            "微软雅黑": "C:/Windows/Fonts/msyh.ttc",
                            "微软雅黑黑体": "C:/Windows/Fonts/msyhbd.ttc",
                            "微软雅轻黑": "C:/Windows/Fonts/msyhlt.ttc"
                        }

                        if font_path in chinese_fonts:
                            font_path = chinese_fonts[font_path]
                        else:
                            # 默认使用宋体
                            font_path = "C:/Windows/Fonts/simsun.ttc"
                    else:
                        # 其他系统尝试使用字体名称
                        pass

                    # 尝试加载中文字体
                    font = ImageFont.truetype(font_path, font_size)
                else:
                    # 如果不包含中文字符，可以使用普通字体
                    if font_path in ["Arial", "Times New Roman", "Helvetica", "Courier"]:
                        # 使用Pillow内置字体名称
                        font = ImageFont.truetype(font_path, font_size)
                    else:
                        # 尝试直接使用字体名称
                        font = ImageFont.truetype(font_path, font_size)

            except Exception as font_error:
                print(f"警告: 无法加载字体 {font_path}，使用默认字体: {str(font_error)}")
                # 尝试加载系统中可能存在的其他中文字体
                try:
                    # 尝试使用系统中可能存在的其他中文字体
                    fallback_fonts = [
                        "C:/Windows/Fonts/simsun.ttc",  # Windows宋体
                        "C:/Windows/Fonts/simhei.ttf",  # Windows黑体
                        "/System/Library/Fonts/PingFang.ttc",  # macOS
                        "/System/Library/Fonts/Arial Unicode.ttf",  # macOS
                        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
                        "/System/Library/Fonts/STHeiti Light.ttc",  # macOS黑体
                        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"  # Linux
                    ]

                    for fallback_font in fallback_fonts:
                        try:
                            font = ImageFont.truetype(fallback_font, font_size)
                            print(f"成功使用备用字体: {fallback_font}")
                            break
                        except:
                            continue
                    else:
                        font = ImageFont.load_default()
                except:
                    font = ImageFont.load_default()

            # 获取文本尺寸 (使用新版本Pillow API)
            try:
                # 使用textlength获取文本宽度，更准确
                text_width = int(draw.textlength(text, font=font))
                # 使用字体大小作为高度，更可靠
                text_height = font_size
            except Exception as bbox_error:
                print(f"警告: 无法计算文本尺寸，使用默认尺寸: {str(bbox_error)}")
                text_width = font_size * len(text)
                text_height = font_size

            # 确保文本尺寸不为0
            if text_width <= 0 or text_height <= 0:
                print("警告: 文本尺寸无效，使用默认尺寸")
                text_width = font_size * len(text)
                text_height = font_size

            # 创建实际大小的图像
            watermark = Image.new('RGBA', (text_width, text_height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(watermark)

            # 应用文本效果
            if effects:
                try:
                    # 确保特效是字典类型
                    if isinstance(effects, dict):
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
                except Exception as effects_error:
                    print(f"警告: 应用文本特效失败: {str(effects_error)}")

            # 绘制文本
            try:
                draw.text((0, 0), text, font=font, fill=color + (int(opacity * 255),))
            except Exception as text_error:
                print(f"警告: 绘制文本失败: {str(text_error)}")
                # 尝试使用默认颜色和透明度
                draw.text((0, 0), text, font=font, fill=(0, 0, 0, 128))

            return watermark

        except Exception as e:
            print(f"创建文本水印失败: {str(e)}")
            # 创建一个简单的默认水印
            try:
                default_watermark = Image.new('RGBA', (100, 30), (0, 0, 0, 128))
                default_draw = ImageDraw.Draw(default_watermark)
                default_font = ImageFont.load_default()
                default_draw.text((0, 0), "水印", font=default_font, fill=(255, 255, 255, 128))
                return default_watermark
            except:
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
