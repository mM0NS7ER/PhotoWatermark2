"""
UI工具函数模块
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFileDialog, QMessageBox, QProgressBar, QStatusBar
)
from PyQt6.QtGui import QPixmap, QIcon, QFont
from PyQt6.QtCore import Qt, QThread, pyqtSignal


def center_window(window):
    """
    将窗口居中显示

    Args:
        window: 要居中的窗口
    """
    from PyQt6.QtWidgets import QApplication

    # 获取屏幕几何信息
    screen_geometry = QApplication.primaryScreen().availableGeometry()

    # 计算窗口居中位置
    x = (screen_geometry.width() - window.width()) // 2
    y = (screen_geometry.height() - window.height()) // 2

    # 移动窗口到居中位置
    window.move(x, y)


def show_error_message(parent, title, message):
    """
    显示错误消息对话框

    Args:
        parent: 父窗口
        title: 对话框标题
        message: 错误消息
    """
    QMessageBox.critical(parent, title, message)


def show_info_message(parent, title, message):
    """
    显示信息消息对话框

    Args:
        parent: 父窗口
        title: 对话框标题
        message: 信息消息
    """
    QMessageBox.information(parent, title, message)


def show_question_message(parent, title, message):
    """
    显示问题消息对话框

    Args:
        parent: 父窗口
        title: 对话框标题
        message: 问题消息

    Returns:
        用户点击的按钮（QMessageBox.StandardButton）
    """
    return QMessageBox.question(
        parent, 
        title, 
        message,
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        QMessageBox.StandardButton.No
    )


def show_warning_message(parent, title, message):
    """
    显示警告消息对话框

    Args:
        parent: 父窗口
        title: 对话框标题
        message: 警告消息
    """
    QMessageBox.warning(parent, title, message)


def create_icon_button(icon_path, tooltip="", size=(24, 24)):
    """
    创建带图标的按钮

    Args:
        icon_path: 图标路径
        tooltip: 按钮提示
        size: 图标大小

    Returns:
        创建的按钮
    """
    button = QPushButton()
    button.setIcon(QIcon(icon_path))
    button.setIconSize(Qt.Size(*size))
    button.setToolTip(tooltip)
    return button


def create_label_with_font(text, font_size=10, bold=False):
    """
    创建带字体设置的标签

    Args:
        text: 标签文本
        font_size: 字体大小
        bold: 是否加粗

    Returns:
        创建的标签
    """
    label = QLabel(text)
    font = QFont()
    font.setPointSize(font_size)
    font.setBold(bold)
    label.setFont(font)
    return label


def create_progress_bar(parent=None, minimum=0, maximum=100):
    """
    创建进度条

    Args:
        parent: 父窗口
        minimum: 最小值
        maximum: 最大值

    Returns:
        创建的进度条
    """
    progress_bar = QProgressBar(parent)
    progress_bar.setMinimum(minimum)
    progress_bar.setMaximum(maximum)
    progress_bar.setValue(0)
    return progress_bar


def create_status_bar_message(status_bar, message, timeout=3000):
    """
    在状态栏显示消息

    Args:
        status_bar: 状态栏对象
        message: 要显示的消息
        timeout: 消息显示时间（毫秒）
    """
    status_bar.showMessage(message, timeout)


class WorkerThread(QThread):
    """
    工作线程，用于执行耗时任务而不阻塞UI
    """

    # 定义信号
    finished = pyqtSignal()
    error = pyqtSignal(str)
    progress = pyqtSignal(int)

    def __init__(self, task, *args, **kwargs):
        """
        初始化工作线程

        Args:
            task: 要执行的任务函数
            *args: 任务函数的位置参数
            **kwargs: 任务函数的关键字参数
        """
        super().__init__()
        self.task = task
        self.args = args
        self.kwargs = kwargs

    def run(self):
        """
        运行任务
        """
        try:
            # 执行任务
            result = self.task(*self.args, **self.kwargs)

            # 任务完成信号
            self.finished.emit()

            # 如果任务有返回结果，可以在这里处理
            if result is not None:
                pass  # 可以根据需要处理结果

        except Exception as e:
            # 错误信号
            self.error.emit(str(e))


def run_in_background(task, *args, **kwargs):
    """
    在后台线程中运行任务

    Args:
        task: 要执行的任务函数
        *args: 任务函数的位置参数
        **kwargs: 任务函数的关键字参数

    Returns:
        WorkerThread实例
    """
    worker = WorkerThread(task, *args, **kwargs)
    worker.start()
    return worker


def update_progress_bar(progress_bar, value):
    """
    更新进度条值

    Args:
        progress_bar: 进度条对象
        value: 新的进度值
    """
    progress_bar.setValue(value)


def enable_widgets(widgets, enable=True):
    """
    启用或禁用一组控件

    Args:
        widgets: 控件列表
        enable: 是否启用
    """
    for widget in widgets:
        widget.setEnabled(enable)


def set_widgets_visible(widgets, visible=True):
    """
    设置一组控件的可见性

    Args:
        widgets: 控件列表
        visible: 是否可见
    """
    for widget in widgets:
        widget.setVisible(visible)


def get_file_dialog_filter(supported_formats):
    """
    获取文件对话框过滤器字符串

    Args:
        supported_formats: 支持的文件格式列表，如 ["JPEG", "PNG", "BMP"]

    Returns:
        过滤器字符串
    """
    filter_parts = []

    # 添加所有支持的格式
    for format_name in supported_formats:
        filter_parts.append(f"{format_name}文件 (*.{format_name.lower()} *.{format_name.lower()[0]}*)")

    # 添加"所有文件"选项
    filter_parts.append("所有文件 (*.*)")

    # 组合过滤器字符串
    return ";;".join(filter_parts)


def get_save_file_dialog(
    parent=None, 
    title="保存文件", 
    initial_filter="JPEG", 
    supported_formats=None,
    default_name=""
):
    """
    获取保存文件对话框

    Args:
        parent: 父窗口
        title: 对话框标题
        initial_filter: 初始选择的过滤器
        supported_formats: 支持的文件格式列表
        default_name: 默认文件名

    Returns:
        选择的文件路径，如果取消则返回空字符串
    """
    if supported_formats is None:
        supported_formats = ["JPEG", "PNG", "BMP"]

    # 创建文件对话框
    file_dialog = QFileDialog(parent, title, default_name)

    # 设置文件模式
    file_dialog.setFileMode(QFileDialog.FileMode.AnyFile)

    # 设置过滤器
    filter_str = get_file_dialog_filter(supported_formats)
    file_dialog.setNameFilter(filter_str)

    # 设置初始选择的过滤器
    for i, format_name in enumerate(supported_formats):
        if format_name == initial_filter:
            file_dialog.selectFilter(filter_str.split(";;")[i])
            break

    # 显示对话框
    if file_dialog.exec():
        selected_files = file_dialog.selectedFiles()
        if selected_files:
            return selected_files[0]

    return ""


def get_open_file_dialog(
    parent=None, 
    title="打开文件", 
    initial_filter="JPEG", 
    supported_formats=None,
    multi_select=False
):
    """
    获取打开文件对话框

    Args:
        parent: 父窗口
        title: 对话框标题
        initial_filter: 初始选择的过滤器
        supported_formats: 支持的文件格式列表
        multi_select: 是否允许多选

    Returns:
        选择的文件路径列表，如果取消则返回空列表
    """
    if supported_formats is None:
        supported_formats = ["JPEG", "PNG", "BMP"]

    # 创建文件对话框
    file_dialog = QFileDialog(parent, title)

    # 设置文件模式
    if multi_select:
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
    else:
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)

    # 设置过滤器
    filter_str = get_file_dialog_filter(supported_formats)
    file_dialog.setNameFilter(filter_str)

    # 设置初始选择的过滤器
    for i, format_name in enumerate(supported_formats):
        if format_name == initial_filter:
            file_dialog.selectFilter(filter_str.split(";;")[i])
            break

    # 显示对话框
    if file_dialog.exec():
        return file_dialog.selectedFiles()

    return []


def get_open_directory_dialog(parent=None, title="选择目录", initial_dir=""):
    """
    获取打开目录对话框

    Args:
        parent: 父窗口
        title: 对话框标题
        initial_dir: 初始目录

    Returns:
        选择的目录路径，如果取消则返回空字符串
    """
    file_dialog = QFileDialog(parent, title, initial_dir)
    file_dialog.setFileMode(QFileDialog.FileMode.Directory)

    if file_dialog.exec():
        selected_dirs = file_dialog.selectedFiles()
        if selected_dirs:
            return selected_dirs[0]

    return ""


def create_separator():
    """
    创建水平分隔线

    Returns:
        分隔线控件
    """
    from PyQt6.QtWidgets import QFrame
    separator = QFrame()
    separator.setFrameShape(QFrame.Shape.HLine)
    separator.setFrameShadow(QFrame.Shadow.Sunken)
    return separator


def create_spacer():
    """
    创建弹性空间

    Returns:
        弹性空间控件
    """
    from PyQt6.QtWidgets import QSpacerItem, QSizePolicy
    return QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
