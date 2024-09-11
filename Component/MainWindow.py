import os
import tempfile

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QPushButton, QLineEdit, QHBoxLayout, \
    QWidget, QFileDialog, QMessageBox, QGroupBox, QSizePolicy, QSpacerItem

from Component.DetailWindow import DetailWindow
from LogType.log_handler import LogHandler


def save_last_opened_path(path):
    # 获取系统的临时目录
    temp_dir = tempfile.gettempdir()

    # 在临时目录中创建一个文件来保存最后打开的路径
    temp_file_path = os.path.join(temp_dir, "log_analysis_last_opened_path.txt")

    # 将路径写入临时文件
    with open(temp_file_path, "w") as temp_file:
        temp_file.write(path)


def check_log_path(log_path):
    if not log_path:
        return False
    if not os.path.exists(log_path):
        return False
    for root, dirs, files in os.walk(log_path):
        for dir_name in dirs:
            if dir_name.startswith("APLog_"):
                return True
    return False


def load_last_opened_path():
    # 获取系统的临时目录
    temp_dir = tempfile.gettempdir()

    # 拼接临时文件的路径
    temp_file_path = os.path.join(temp_dir, "log_analysis_last_opened_path.txt")

    # 检查文件是否存在
    if os.path.exists(temp_file_path):
        with open(temp_file_path, "r") as temp_file:
            last_path = temp_file.read()
            print(f"最后打开的 Log 路径: {last_path}")
            return last_path
    else:
        print("没有保存的最后打开路径")
        return os.getcwd()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.QSpacerItem: QSpacerItem = None
        self.file_group_box: QGroupBox = None
        self.open_folder_button_clicked: bool = False
        self.line_edit_log_path: QLineEdit = None
        self.analyze_button: QPushButton = None
        self.open_folder_button: QPushButton = None
        self.init()

    def init(self):
        self.setWindowTitle("Mtk Log Analysis")
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

        # 设置窗口大小
        screen_size = QApplication.primaryScreen().size()
        except_width = 600
        except_height = 160

        # 设置不允许拉伸窗口
        self.setFixedSize(except_width, except_height)
        self.setGeometry(int((screen_size.width() - except_width) / 2),
                         int((screen_size.height() - except_height) / 2),
                         except_width, except_height)

        # 创建布局
        file_layout = QVBoxLayout()
        file_layout.setAlignment(Qt.AlignVCenter)
        button_layout = QHBoxLayout()
        info_layout = QVBoxLayout()
        info_layout.setAlignment(Qt.AlignTop)

        # 添加输入框
        self.line_edit_log_path = QLineEdit(self)
        self.line_edit_log_path.setFixedHeight(30)
        self.line_edit_log_path.setPlaceholderText("Log 存放路径...")
        self.line_edit_log_path.setText(load_last_opened_path())
        file_layout.addWidget(self.line_edit_log_path)

        self.QSpacerItem = QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Minimum)
        file_layout.addItem(self.QSpacerItem)

        # 添加按钮
        self.open_folder_button = QPushButton('打开Log文件夹', self)
        self.open_folder_button.setFixedHeight(40)
        self.open_folder_button.clicked.connect(self.open_log_folder)
        button_layout.addWidget(self.open_folder_button)

        self.analyze_button = QPushButton('开始分析', self)
        self.analyze_button.setFixedHeight(40)
        self.analyze_button.clicked.connect(self.start_analyze)
        button_layout.addWidget(self.analyze_button)
        file_layout.addLayout(button_layout)

        # 分组布局
        self.file_group_box = QGroupBox("请选择 Log 文件夹", self)
        self.file_group_box.setLayout(file_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.file_group_box)

        # 设置主布局
        self.setLayout(main_layout)

    # 打开 Log 文件夹
    def open_log_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "请选择 Log 文件夹", load_last_opened_path())
        if folder_path:
            self.line_edit_log_path.setText(folder_path)
            save_last_opened_path(folder_path)

    # 开始分析 Log
    def start_analyze(self):
        log_path = self.line_edit_log_path.text()
        if not log_path:
            self.show_error_message("请选择正确的 Log 文件夹")
            return
        print("开始分析...")
        print("Log 文件夹 : ", log_path)

        self.analyze_button.setEnabled(False)

        if not check_log_path(log_path):
            self.show_error_message("请选择正确的 Log 文件夹!\n一般文件夹里面有 APLog_ 开头的文件夹!")
            self.analyze_button.setEnabled(True)
            return

        lh = LogHandler(log_path)
        detail_window = DetailWindow(log_path.replace('/', '\\'), lh)
        detail_window.exec_()
        self.analyze_button.setEnabled(True)

    def show_info_message(self, info):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("信息")
        msg_box.setText(info)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def show_error_message(self, error_message):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("错误")
        msg_box.setText(error_message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
