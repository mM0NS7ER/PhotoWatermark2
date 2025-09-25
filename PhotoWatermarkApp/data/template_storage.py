"""
模板存储模块
"""

import os
import json
from typing import Dict, List, Optional, Tuple

from PyQt6.QtWidgets import QInputDialog, QMessageBox


class TemplateStorage:
    """模板存储模块，负责水印模板的保存和加载"""

    def __init__(self, template_dir: str = 'templates'):
        self.template_dir = template_dir
        self.ensure_template_dir()

    def ensure_template_dir(self) -> None:
        """确保模板目录存在"""
        if not os.path.exists(self.template_dir):
            os.makedirs(self.template_dir)

    def save_template(self, name: str, template: Dict) -> bool:
        """
        保存水印模板

        Args:
            name: 模板名称
            template: 模板数据

        Returns:
            是否保存成功
        """
        try:
            # 确保模板名称有效
            if not name or not name.strip():
                return False

            # 构建模板文件路径
            template_file = os.path.join(self.template_dir, f"{name}.json")

            # 保存模板
            with open(template_file, 'w', encoding='utf-8') as f:
                json.dump(template, f, indent=4, ensure_ascii=False)

            return True

        except Exception as e:
            print(f"保存模板失败: {str(e)}")
            return False

    def load_template(self, name: str) -> Optional[Dict]:
        """
        加载水印模板

        Args:
            name: 模板名称

        Returns:
            模板数据，如果不存在则返回None
        """
        try:
            # 构建模板文件路径
            template_file = os.path.join(self.template_dir, f"{name}.json")

            # 检查文件是否存在
            if not os.path.exists(template_file):
                return None

            # 加载模板
            with open(template_file, 'r', encoding='utf-8') as f:
                template = json.load(f)

            return template

        except Exception as e:
            print(f"加载模板失败: {str(e)}")
            return None

    def list_templates(self) -> List[str]:
        """
        列出所有模板名称

        Returns:
            模板名称列表
        """
        templates = []

        try:
            # 遍历模板目录
            for filename in os.listdir(self.template_dir):
                if filename.endswith('.json'):
                    # 去掉扩展名
                    name = os.path.splitext(filename)[0]
                    templates.append(name)
        except Exception as e:
            print(f"列出模板失败: {str(e)}")

        return templates

    def delete_template(self, name: str) -> bool:
        """
        删除水印模板

        Args:
            name: 模板名称

        Returns:
            是否删除成功
        """
        try:
            # 构建模板文件路径
            template_file = os.path.join(self.template_dir, f"{name}.json")

            # 检查文件是否存在
            if not os.path.exists(template_file):
                return False

            # 删除模板文件
            os.remove(template_file)
            return True

        except Exception as e:
            print(f"删除模板失败: {str(e)}")
            return False

    def get_template_name(self, parent=None) -> Tuple[str, bool]:
        """
        获取模板名称（通过对话框）

        Args:
            parent: 父窗口

        Returns:
            模板名称和是否确认的元组
        """
        name, ok = QInputDialog.getText(
            parent, 
            "保存模板", 
            "请输入模板名称:", 
            text="默认模板"
        )

        return name, ok

    def select_template(self, templates: List[str], parent=None) -> Tuple[str, bool]:
        """
        选择模板（通过对话框）

        Args:
            templates: 可用模板列表
            parent: 父窗口

        Returns:
            模板名称和是否确认的元组
        """
        if not templates:
            return "", False

        # 使用QInputDialog选择模板
        name, ok = QInputDialog.getItem(
            parent,
            "选择模板",
            "请选择模板:",
            templates,
            0,
            False
        )

        return name, ok

    def import_template(self, template_file: str, parent=None) -> bool:
        """
        导入模板文件

        Args:
            template_file: 模板文件路径
            parent: 父窗口

        Returns:
            是否导入成功
        """
        try:
            # 检查文件是否存在
            if not os.path.exists(template_file):
                QMessageBox.warning(parent, "导入失败", "模板文件不存在")
                return False

            # 加载模板
            with open(template_file, 'r', encoding='utf-8') as f:
                template = json.load(f)

            # 获取模板名称
            name, ok = QInputDialog.getText(
                parent,
                "导入模板",
                "请输入模板名称:",
                text=os.path.splitext(os.path.basename(template_file))[0]
            )

            if not ok or not name or not name.strip():
                return False

            # 保存模板
            return self.save_template(name, template)

        except Exception as e:
            QMessageBox.warning(parent, "导入失败", f"导入模板失败: {str(e)}")
            return False

    def export_template(self, name: str, output_file: str, parent=None) -> bool:
        """
        导出模板文件

        Args:
            name: 模板名称
            output_file: 输出文件路径
            parent: 父窗口

        Returns:
            是否导出成功
        """
        try:
            # 加载模板
            template = self.load_template(name)
            if template is None:
                QMessageBox.warning(parent, "导出失败", f"模板 '{name}' 不存在")
                return False

            # 保存模板
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(template, f, indent=4, ensure_ascii=False)

            return True

        except Exception as e:
            QMessageBox.warning(parent, "导出失败", f"导出模板失败: {str(e)}")
            return False
