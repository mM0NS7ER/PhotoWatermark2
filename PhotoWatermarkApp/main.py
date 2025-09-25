#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
照片水印应用 - 主程序入口
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

# 添加项目根目录到系统路径，以便导入其他模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.main_window import MainWindow

def main():
    """应用程序主函数"""
    # 创建应用程序实例
    app = QApplication(sys.argv)

    # 设置应用程序图标
    app.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), 'resources', 'icons', 'app_icon.png')))

    # 创建并显示主窗口
    window = MainWindow()
    window.show()

    # 进入应用程序主循环
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
