"""
图片存储模块
"""

import os
from typing import Dict, List, Optional
from PIL import Image, ImageFile

# 允许加载截断的图像文件
ImageFile.LOAD_TRUNCATED_IMAGES = True


class ImageStorage:
    """图片存储模块，负责图片文件的加载和管理"""

    def __init__(self):
        self.images = {}  # 存储图片路径和图片对象的映射
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']

    def load_image(self, file_path: str) -> bool:
        """
        加载图片文件

        Args:
            file_path: 图片文件路径

        Returns:
            是否成功加载
        """
        try:
            # 检查文件是否存在
            if not os.path.isfile(file_path):
                return False

            # 检查文件格式是否支持
            file_ext = os.path.splitext(file_path)[1].lower()
            if file_ext not in self.supported_formats:
                return False

            # 加载图片
            with Image.open(file_path) as img:
                # 转换为RGB模式（如果不是）
                if img.mode != 'RGB':
                    img = img.convert('RGB')

                # 保存到内存
                self.images[file_path] = img.copy()
                return True

        except Exception as e:
            print(f"加载图片失败: {file_path}, 错误: {str(e)}")
            return False

    def get_image(self, file_path: str) -> Optional[Image.Image]:
        """
        获取已加载的图片

        Args:
            file_path: 图片文件路径

        Returns:
            PIL图片对象，如果不存在则返回None
        """
        return self.images.get(file_path)

    def get_all_image_paths(self) -> List[str]:
        """
        获取所有已加载图片的路径

        Returns:
            图片路径列表
        """
        return list(self.images.keys())

    def remove_image(self, file_path: str) -> bool:
        """
        移除已加载的图片

        Args:
            file_path: 图片文件路径

        Returns:
            是否成功移除
        """
        if file_path in self.images:
            del self.images[file_path]
            return True
        return False

    def clear(self) -> None:
        """清空所有已加载的图片"""
        self.images.clear()

    def get_image_info(self, file_path: str) -> Optional[Dict]:
        """
        获取图片信息

        Args:
            file_path: 图片文件路径

        Returns:
            图片信息字典，如果不存在则返回None
        """
        if file_path not in self.images:
            return None

        image = self.images[file_path]
        return {
            'path': file_path,
            'format': image.format,
            'mode': image.mode,
            'size': image.size,
            'width': image.width,
            'height': image.height
        }
