"""
文件处理模块
"""

import os
import shutil
from datetime import datetime
from typing import List, Dict, Optional, Union

from PIL import Image
from data.image_storage import ImageStorage
from core.watermark_processor import WatermarkProcessor


class FileProcessor:
    """文件处理模块，负责图片的导入、导出和格式转换"""

    def __init__(self):
        self.image_storage = ImageStorage()
        self.watermark_processor = WatermarkProcessor()
        self.supported_formats = {
            'JPEG': ['.jpg', '.jpeg'],
            'PNG': ['.png'],
            'BMP': ['.bmp'],
            'TIFF': ['.tiff', '.tif']
        }

    def import_images(self, file_paths: List[str]) -> Dict[str, bool]:
        """
        导入图片文件

        Args:
            file_paths: 图片文件路径列表

        Returns:
            字典，键为文件路径，值为是否成功导入
        """
        results = {}

        for file_path in file_paths:
            if os.path.isfile(file_path):
                # 检查文件格式是否支持
                file_ext = os.path.splitext(file_path)[1].lower()
                format_found = False

                for format_name, extensions in self.supported_formats.items():
                    if file_ext in extensions:
                        format_found = True
                        break

                if format_found:
                    # 尝试加载图片
                    if self.image_storage.load_image(file_path):
                        results[file_path] = True
                    else:
                        results[file_path] = False
                else:
                    results[file_path] = False
            else:
                results[file_path] = False

        return results

    def export_images(
        self, 
        output_folder: str, 
        watermark_params: Optional[Dict] = None,
        file_format: str = 'JPEG',
        quality: int = 90,
        resize_size: Optional[tuple] = None,
        filename_pattern: str = '{original_name}_watermarked',
        overwrite_existing: bool = False
    ) -> Dict[str, bool]:
        """
        导出图片

        Args:
            output_folder: 输出文件夹路径
            watermark_params: 水印参数
            file_format: 输出文件格式
            quality: JPEG质量 (1-100)
            resize_size: 调整后的尺寸 (width, height)
            filename_pattern: 文件名模式
            overwrite_existing: 是否覆盖已存在的文件

        Returns:
            字典，键为原始文件路径，值为是否成功导出
        """
        # 确保输出文件夹存在
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        results = {}

        # 获取所有已加载的图片
        image_paths = self.image_storage.get_all_image_paths()

        for i, image_path in enumerate(image_paths):
            try:
                # 获取图片对象
                image = self.image_storage.get_image(image_path)
                if image is None:
                    results[image_path] = False
                    continue

                # 应用水印（如果需要）
                if watermark_params:
                    image = self.watermark_processor.apply_watermark(
                        image, 
                        watermark_params
                    )

                # 调整尺寸（如果需要）
                if resize_size:
                    image = self.resize_image(image, resize_size)

                # 生成文件名
                original_name = os.path.splitext(os.path.basename(image_path))[0]
                date_str = datetime.now().strftime("%Y%m%d_%H%M%S")

                # 替换文件名模式中的变量
                filename = filename_pattern.format(
                    original_name=original_name,
                    index=i + 1,
                    date=date_str
                )

                # 确保文件名有正确的扩展名
                if file_format.upper() in self.supported_formats:
                    ext = self.supported_formats[file_format.upper()][0]
                    if not filename.lower().endswith(ext.lower()):
                        filename += ext
                else:
                    filename += os.path.splitext(image_path)[1]

                # 构建输出路径
                output_path = os.path.join(output_folder, filename)

                # 检查文件是否已存在
                if os.path.exists(output_path) and not overwrite_existing:
                    # 添加序号避免覆盖
                    counter = 1
                    base, ext = os.path.splitext(filename)
                    while os.path.exists(os.path.join(output_folder, f"{base}_{counter}{ext}")):
                        counter += 1
                    filename = f"{base}_{counter}{ext}"
                    output_path = os.path.join(output_folder, filename)

                # 保存图片
                save_kwargs = {}
                if file_format.upper() == 'JPEG':
                    save_kwargs['quality'] = quality
                    save_kwargs['optimize'] = True

                image.save(output_path, **save_kwargs)
                results[image_path] = True

            except Exception as e:
                print(f"导出图片失败: {image_path}, 错误: {str(e)}")
                results[image_path] = False

        return results

    def resize_image(self, image: Image.Image, size: tuple) -> Image.Image:
        """
        调整图片尺寸

        Args:
            image: PIL图片对象
            size: 目标尺寸 (width, height)

        Returns:
            调整后的图片对象
        """
        return image.resize(size, Image.Resampling.LANCZOS)

    def validate_format(self, file_path: str) -> bool:
        """
        验证文件格式是否支持

        Args:
            file_path: 文件路径

        Returns:
            是否支持该文件格式
        """
        if not os.path.isfile(file_path):
            return False

        file_ext = os.path.splitext(file_path)[1].lower()

        for extensions in self.supported_formats.values():
            if file_ext in extensions:
                return True

        return False
