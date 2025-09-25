"""
配置存储模块
"""

import os
import json
from typing import Dict, Any, Optional


class ConfigStorage:
    """配置存储模块，负责应用配置的保存和加载"""

    def __init__(self, config_file: str = 'config.json'):
        self.config_file = config_file
        self.config = self.load_default_config()
        self.load_config()

    def load_default_config(self) -> Dict[str, Any]:
        """加载默认配置"""
        return {
            'app': {
                'name': '照片水印应用',
                'version': '1.0',
                'window_size': (1024, 768),
                'last_output_folder': '',
                'language': 'zh_CN'
            },
            'watermark': {
                'default_type': 'text',
                'default_text': '水印',
                'default_font': 'Arial',
                'default_font_size': 24,
                'default_color': [0, 0, 0],
                'default_opacity': 0.7,
                'default_position': 'center'
            },
            'export': {
                'default_format': 'JPEG',
                'default_quality': 90,
                'default_filename_pattern': '{original_name}_watermarked'
            }
        }

    def load_config(self) -> bool:
        """从文件加载配置"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    file_config = json.load(f)

                # 合并配置，保留默认值
                self.merge_config(self.config, file_config)
                return True
            except Exception as e:
                print(f"加载配置文件失败: {str(e)}")
                return False
        return False

    def save_config(self) -> bool:
        """保存配置到文件"""
        try:
            # 确保配置目录存在
            config_dir = os.path.dirname(self.config_file)
            if config_dir and not os.path.exists(config_dir):
                os.makedirs(config_dir)

            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"保存配置文件失败: {str(e)}")
            return False

    def get(self, section: str, key: str, default: Any = None) -> Any:
        """
        获取配置值

        Args:
            section: 配置节名称
            key: 配置键名
            default: 默认值

        Returns:
            配置值
        """
        try:
            return self.config[section][key]
        except KeyError:
            return default

    def set(self, section: str, key: str, value: Any) -> bool:
        """
        设置配置值

        Args:
            section: 配置节名称
            key: 配置键名
            value: 配置值

        Returns:
            是否设置成功
        """
        try:
            if section not in self.config:
                self.config[section] = {}

            self.config[section][key] = value
            return True
        except Exception as e:
            print(f"设置配置值失败: {str(e)}")
            return False

    def merge_config(self, base: Dict, update: Dict) -> None:
        """
        递归合并配置字典

        Args:
            base: 基础配置字典
            update: 更新配置字典
        """
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self.merge_config(base[key], value)
            else:
                base[key] = value

    def reset_to_default(self) -> bool:
        """重置为默认配置"""
        self.config = self.load_default_config()
        return self.save_config()

    def export_config(self, export_file: str) -> bool:
        """
        导出配置到文件

        Args:
            export_file: 导出文件路径

        Returns:
            是否导出成功
        """
        try:
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"导出配置失败: {str(e)}")
            return False

    def import_config(self, import_file: str) -> bool:
        """
        从文件导入配置

        Args:
            import_file: 导入文件路径

        Returns:
            是否导入成功
        """
        if not os.path.exists(import_file):
            return False

        try:
            with open(import_file, 'r', encoding='utf-8') as f:
                imported_config = json.load(f)

            # 合并配置
            self.merge_config(self.config, imported_config)
            return self.save_config()
        except Exception as e:
            print(f"导入配置失败: {str(e)}")
            return False
