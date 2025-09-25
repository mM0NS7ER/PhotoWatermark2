"""
图片处理工具模块
"""

import os
from typing import Tuple, List, Optional, Union
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import numpy as np


def resize_image(
    image: Image.Image, 
    size: Tuple[int, int], 
    maintain_aspect: bool = True, 
    resample: int = Image.Resampling.LANCZOS
) -> Image.Image:
    """
    调整图片尺寸

    Args:
        image: PIL图片对象
        size: 目标尺寸 (width, height)
        maintain_aspect: 是否保持宽高比
        resample: 重采样方法

    Returns:
        调整后的图片对象
    """
    if not maintain_aspect:
        return image.resize(size, resample)

    # 计算保持宽高比的尺寸
    img_width, img_height = image.size
    target_width, target_height = size

    # 计算缩放比例
    ratio = min(target_width / img_width, target_height / img_height)

    # 计算新尺寸
    new_width = int(img_width * ratio)
    new_height = int(img_height * ratio)

    # 调整尺寸
    return image.resize((new_width, new_height), resample)


def crop_image(
    image: Image.Image, 
    box: Tuple[int, int, int, int] = None, 
    center: bool = True
) -> Image.Image:
    """
    裁剪图片

    Args:
        image: PIL图片对象
        box: 裁剪区域 (left, top, right, bottom)
        center: 是否以中心为基准裁剪

    Returns:
        裁剪后的图片对象
    """
    if box is None:
        # 如果没有指定裁剪区域，则根据center参数进行裁剪
        img_width, img_height = image.size

        if center:
            # 以中心为基准裁剪，保持正方形
            min_size = min(img_width, img_height)
            left = (img_width - min_size) // 2
            top = (img_height - min_size) // 2
            right = left + min_size
            bottom = top + min_size
            box = (left, top, right, bottom)
        else:
            # 从左上角裁剪，保持正方形
            min_size = min(img_width, img_height)
            box = (0, 0, min_size, min_size)

    return image.crop(box)


def rotate_image(
    image: Image.Image, 
    angle: float, 
    expand: bool = True, 
    fillcolor: Union[int, Tuple[int, ...]] = None
) -> Image.Image:
    """
    旋转图片

    Args:
        image: PIL图片对象
        angle: 旋转角度（度）
        expand: 是否扩展图片以包含整个旋转后的图像
        fillcolor: 填充颜色

    Returns:
        旋转后的图片对象
    """
    return image.rotate(angle, expand=expand, fillcolor=fillcolor)


def adjust_brightness(
    image: Image.Image, 
    factor: float
) -> Image.Image:
    """
    调整图片亮度

    Args:
        image: PIL图片对象
        factor: 亮度因子，1.0表示原始亮度，小于1.0变暗，大于1.0变亮

    Returns:
        调整后的图片对象
    """
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)


def adjust_contrast(
    image: Image.Image, 
    factor: float
) -> Image.Image:
    """
    调整图片对比度

    Args:
        image: PIL图片对象
        factor: 对比度因子，1.0表示原始对比度，小于1.0降低对比度，大于1.0提高对比度

    Returns:
        调整后的图片对象
    """
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)


def adjust_saturation(
    image: Image.Image, 
    factor: float
) -> Image.Image:
    """
    调整图片饱和度

    Args:
        image: PIL图片对象
        factor: 饱和度因子，1.0表示原始饱和度，0.0表示灰度图，大于1.0增加饱和度

    Returns:
        调整后的图片对象
    """
    enhancer = ImageEnhance.Color(image)
    return enhancer.enhance(factor)


def sharpen_image(image: Image.Image, factor: float = 1.0) -> Image.Image:
    """
    锐化图片

    Args:
        image: PIL图片对象
        factor: 锐化因子，1.0表示原始锐度

    Returns:
        锐化后的图片对象
    """
    enhancer = ImageEnhance.Sharpness(image)
    return enhancer.enhance(factor)


def blur_image(image: Image.Image, radius: float = 1.0) -> Image.Image:
    """
    模糊图片

    Args:
        image: PIL图片对象
        radius: 模糊半径

    Returns:
        模糊后的图片对象
    """
    return image.filter(ImageFilter.GaussianBlur(radius))


def auto_contrast(image: Image.Image, cutoff: float = 0.1) -> Image.Image:
    """
    自动调整图片对比度

    Args:
        image: PIL图片对象
        cutoff: 裁剪比例，用于自动对比度调整

    Returns:
        调整后的图片对象
    """
    return ImageOps.autocontrast(image, cutoff=cutoff)


def auto_equalize(image: Image.Image) -> Image.Image:
    """
    自动均衡化图片直方图

    Args:
        image: PIL图片对象

    Returns:
        均衡化后的图片对象
    """
    return ImageOps.equalize(image)


def invert_image(image: Image.Image) -> Image.Image:
    """
    反转图片颜色

    Args:
        image: PIL图片对象

    Returns:
        反转后的图片对象
    """
    return ImageOps.invert(image.convert('RGB'))


def grayscale_image(image: Image.Image) -> Image.Image:
    """
    将图片转换为灰度图

    Args:
        image: PIL图片对象

    Returns:
        灰度图片对象
    """
    return image.convert('L')


def get_dominant_colors(image: Image.Image, num_colors: int = 5) -> List[Tuple[int, int, int]]:
    """
    获取图片中的主要颜色

    Args:
        image: PIL图片对象
        num_colors: 要提取的主要颜色数量

    Returns:
        主要颜色列表，每个颜色表示为RGB元组
    """
    # 缩小图片以提高处理速度
    small_image = image.resize((150, 150))

    # 转换为RGB模式
    rgb_image = small_image.convert('RGB')

    # 将图片转换为像素数组
    pixels = np.array(rgb_image)

    # 使用k-means聚类算法找出主要颜色
    from sklearn.cluster import MiniBatchKMeans

    # 重塑像素数组
    pixels = pixels.reshape(-1, 3)

    # 应用k-means聚类
    kmeans = MiniBatchKMeans(n_clusters=num_colors)
    kmeans.fit(pixels)

    # 获取聚类中心（主要颜色）
    colors = kmeans.cluster_centers_.astype(int)

    # 转换为RGB元组列表
    return [tuple(color) for color in colors]


def create_thumbnail(image: Image.Image, size: Tuple[int, int] = (128, 128)) -> Image.Image:
    """
    创建图片缩略图

    Args:
        image: PIL图片对象
        size: 缩略图尺寸

    Returns:
        缩略图对象
    """
    thumbnail = image.copy()
    thumbnail.thumbnail(size, Image.Resampling.LANCZOS)
    return thumbnail


def is_valid_image(file_path: str) -> bool:
    """
    检查文件是否为有效图片

    Args:
        file_path: 文件路径

    Returns:
        是否为有效图片
    """
    try:
        with Image.open(file_path) as img:
            img.verify()
        return True
    except:
        return False


def get_image_info(file_path: str) -> Optional[dict]:
    """
    获取图片信息

    Args:
        file_path: 图片文件路径

    Returns:
        图片信息字典，如果无效则返回None
    """
    try:
        with Image.open(file_path) as img:
            return {
                'format': img.format,
                'mode': img.mode,
                'size': img.size,
                'width': img.width,
                'height': img.height,
                'file_size': os.path.getsize(file_path)
            }
    except:
        return None
