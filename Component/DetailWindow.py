from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCharFormat, QColor
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, \
    QWidget, QTextEdit, QGroupBox, QSpacerItem, QLabel, \
    QListWidget, QTabWidget, QDialog, QListWidgetItem

from LogType.log_handler import LogHandler, get_log_text


def create_tab(tab_content: str = None):
    tab = QWidget()
    text_edit = QTextEdit()
    text_edit.setReadOnly(True)
    if tab_content:
        text_edit.setText(tab_content)
    else:
        text_edit.setPlaceholderText("没有找到可疑的信息")
    layout = QVBoxLayout()
    layout.addWidget(text_edit)
    tab.setLayout(layout)
    return tab, text_edit


class DetailWindow(QDialog):
    def __init__(self, path, log_handler: LogHandler):
        super().__init__()
        self.tab_system_text: QTextEdit = None
        self.tab_crash_text: QTextEdit = None
        self.tab_top_activity_text: QTextEdit = None
        self.tab_activity_text: QTextEdit = None
        self.tab_proc_text: QTextEdit = None
        self.tab_main_text: QTextEdit = None
        self.tab_top_activity: QWidget = None
        self.tab_activity: QWidget = None
        self.tab_proc: QWidget = None
        self.tab_main: QWidget = None
        self.tab_crash: QWidget = None
        self.tab_system: QWidget = None
        self.log_path = path
        self.spacer: QSpacerItem = None
        self.log_info_summary_label: QLabel = None
        self.log_info_summary_box: QGroupBox = None
        self.log_info_detail_box: QGroupBox = None
        self.device_info_box: QGroupBox = None
        self.log_select_box: QGroupBox = None
        self.log_select_list: QListWidget = None
        self.device_info_text: QTextEdit = None
        self.log_info_detail_tab: QTabWidget = None
        self.log_info_summary_content: str = ""
        self.log_handler = log_handler
        self.init()

    def init(self):
        self.setWindowTitle("当前Log路径  >  " + self.log_path)
        self.setWindowFlags(Qt.WindowMinimizeButtonHint |
                            Qt.WindowMaximizeButtonHint |
                            Qt.WindowCloseButtonHint)

        # 设置窗口大小
        screen_size = QApplication.primaryScreen().size()
        except_width = 1600
        except_height = 860
        left_window_width = 400

        # 设置窗口位置
        self.setGeometry(int((screen_size.width() - except_width) / 2),
                         int((screen_size.height() - except_height) / 2),
                         except_width, except_height)

        # 创建布局
        main_layout = QHBoxLayout()
        log_select_layout = QVBoxLayout()
        device_info_layout = QVBoxLayout()
        log_info_summary_layout = QHBoxLayout()
        log_info_detail_layout = QVBoxLayout()

        main_right_layout = QVBoxLayout()
        main_left_layout = QVBoxLayout()

        main_layout.setAlignment(Qt.AlignTop)
        log_select_layout.setAlignment(Qt.AlignTop)
        device_info_layout.setAlignment(Qt.AlignTop)
        log_info_summary_layout.setAlignment(Qt.AlignTop)

        # Log 选择
        self.log_select_list = QListWidget(self)

        ap_log_list = self.log_handler.get_ap_log_name_list()
        for log_name in ap_log_list:
            current_item = QListWidgetItem()
            _, crash_count = self.log_handler.get_crash_log(ap_log_list.index(log_name))
            _, anr_count = self.log_handler.get_sys_log(ap_log_list.index(log_name))
            if anr_count > 0 and crash_count > 0:
                log_name = f"{log_name} [ANR: {anr_count}][Crash: {crash_count}]"
                current_item.setBackground(QColor("#F76560"))
            elif anr_count > 0:
                log_name = f"{log_name} [ANR: {anr_count}]"
                current_item.setBackground(QColor("#FCC59F"))
            elif crash_count > 0:
                log_name = f"{log_name} [Crash: {crash_count}]"
                current_item.setBackground(QColor("#FBACA3"))
            current_item.setText(log_name)
            self.log_select_list.addItem(current_item)

        self.log_select_list.setCurrentItem(self.log_select_list.item(0))
        self.log_select_list.clicked.connect(self.select_log)

        # Log 选择 Group Box
        self.log_select_box = QGroupBox("Log 选择")
        self.log_select_box.setFixedHeight(180)
        self.log_select_box.setFixedWidth(left_window_width)
        self.log_select_box.setLayout(log_select_layout)
        log_select_layout.addWidget(self.log_select_list)

        # 设备信息
        self.device_info_text = QTextEdit(self)
        self.device_info_text.setReadOnly(True)
        self.update_device_info()
        device_info_layout.addWidget(self.device_info_text)

        # 设备信息 Group Box
        self.device_info_box = QGroupBox("设备信息")
        self.device_info_box.setFixedWidth(left_window_width)
        self.device_info_box.setMinimumHeight(300)
        self.device_info_box.setSizePolicy(self.device_info_box.sizePolicy().horizontalPolicy(),
                                           self.device_info_box.sizePolicy().Expanding)
        self.device_info_box.setLayout(device_info_layout)

        self.log_info_summary_label = QLabel(self.log_info_summary_content)
        self.update_log_info_summary()
        log_info_summary_layout.addWidget(self.log_info_summary_label)

        # Log 信息概要 Group Box
        self.log_info_summary_box = QGroupBox("Log 信息概要")
        self.log_info_summary_box.setFixedHeight(180)
        self.log_info_summary_box.setMaximumWidth(left_window_width)
        self.log_info_summary_box.setLayout(log_info_summary_layout)

        # Log 信息详情
        self.log_info_detail_tab = QTabWidget()
        self.log_info_detail_tab.setMinimumWidth(800)

        (main_log_text, proc_log_text, activity_log_text, top_activity_log_text,
         crash_log_text, sys_log_text) = self.get_detail_logs()

        self.tab_main, self.tab_main_text = create_tab(main_log_text)
        self.tab_proc, self.tab_proc_text = create_tab(proc_log_text)
        self.tab_activity, self.tab_activity_text = create_tab(activity_log_text)
        self.tab_top_activity, self.tab_top_activity_text = create_tab(top_activity_log_text)
        self.tab_crash, self.tab_crash_text = create_tab(crash_log_text)
        self.tab_system, self.tab_system_text = create_tab(sys_log_text)

        self.log_info_detail_tab.addTab(self.tab_crash, "Crash Log")
        self.log_info_detail_tab.addTab(self.tab_main, "Main Log")
        self.log_info_detail_tab.addTab(self.tab_system, "System Log")
        self.log_info_detail_tab.addTab(self.tab_proc, "Proc Log")
        self.log_info_detail_tab.addTab(self.tab_activity, "Activity Log")
        self.log_info_detail_tab.addTab(self.tab_top_activity, "Top Activity Log")
        log_info_detail_layout.addWidget(self.log_info_detail_tab)

        # Log 信息详情 Group Box
        self.log_info_detail_box = QGroupBox("Log 信息详情")
        self.log_info_detail_box.setSizePolicy(self.log_info_detail_box.sizePolicy().horizontalPolicy(),
                                               self.log_info_detail_box.sizePolicy().Expanding)
        self.log_info_detail_box.setLayout(log_info_detail_layout)

        main_right_layout.addWidget(self.log_info_detail_box)
        main_left_layout.addWidget(self.log_select_box)
        main_left_layout.addWidget(self.log_info_summary_box)
        main_left_layout.addWidget(self.device_info_box)

        main_layout.addLayout(main_left_layout)
        main_layout.addLayout(main_right_layout)
        self.setLayout(main_layout)

    def update_log_info_summary(self):
        properties_origin = self.log_handler.get_property_log(self.log_select_list.currentRow())
        last_reboot_reason = properties_origin['last_boot_reason']
        _, crash_count_all = self.log_handler.get_crash_log_all()
        _, anr_count_all = self.log_handler.get_sys_log_all()
        _, crash_count = self.log_handler.get_crash_log(self.log_select_list.currentRow())
        _, anr_count = self.log_handler.get_sys_log(self.log_select_list.currentRow())
        properties = {
            'crash_count_all': crash_count_all,
            'anr_count_all': anr_count_all,
            'crash_count': crash_count,
            'anr_count': anr_count,
            'last_boot_reason': last_reboot_reason
        }
        self.log_info_summary_content = f"总共 App Crash 次数: [{properties['crash_count_all']}]\n" \
                                        f"总共 ANR 次数: [{properties['anr_count_all']}]\n" \
                                        f"当前 App Crash 次数: [{properties['crash_count']}]\n" \
                                        f"当前 ANR 次数 : [{properties['anr_count']}]\n" \
                                        f"当前 重启原因 : [{properties['last_boot_reason']}]"
        self.log_info_summary_label.setText(self.log_info_summary_content)

    def update_device_info(self):
        self.device_info_text.clear()
        format_prop = QTextCharFormat()
        format_prop.setForeground(QColor("#871094"))
        format_value = QTextCharFormat()
        format_value.setForeground(QColor("#067d17"))
        data = self.log_handler.get_property_log(self.log_select_list.currentRow()).items()
        for row, (prop, val) in enumerate(data):
            if prop == 'last_boot_reason':
                continue
            formatted_prop = prop.replace('_', '.')
            cursor = self.device_info_text.textCursor()
            cursor.insertText(f'{formatted_prop}', format_prop)
            cursor.insertText(' : ')
            cursor.insertText(f'{val}', format_value)
            cursor.insertText('\n')

    def get_detail_logs(self):
        main_log = self.log_handler.get_main_log(self.log_select_list.currentRow())
        proc_log, activity_log, top_activity_log = (
            self.log_handler.get_event_log(self.log_select_list.currentRow()))
        crash_log, _ = self.log_handler.get_crash_log(self.log_select_list.currentRow())
        sys_log, _ = self.log_handler.get_sys_log(self.log_select_list.currentRow())

        main_log_text = get_log_text(main_log)
        proc_log_text = get_log_text(proc_log)
        activity_log_text = get_log_text(activity_log)
        top_activity_log_text = get_log_text(top_activity_log)
        crash_log_text = get_log_text(crash_log)
        sys_log_text = get_log_text(sys_log)
        return (main_log_text, proc_log_text, activity_log_text, top_activity_log_text,
                crash_log_text, sys_log_text)

    def update_log_info_detail(self):
        (main_log_text, proc_log_text, activity_log_text, top_activity_log_text,
         crash_log_text, sys_log_text) = self.get_detail_logs()

        self.tab_main_text.clear()
        self.tab_main_text.setPlainText(main_log_text)
        self.tab_proc_text.clear()
        self.tab_proc_text.setPlainText(proc_log_text)
        self.tab_activity_text.clear()
        self.tab_activity_text.setPlainText(activity_log_text)
        self.tab_top_activity_text.clear()
        self.tab_top_activity_text.setPlainText(top_activity_log_text)
        self.tab_crash_text.clear()
        self.tab_crash_text.setPlainText(crash_log_text)
        self.tab_system_text.clear()
        self.tab_system_text.setPlainText(sys_log_text)

    def select_log(self):
        self.update_log_info_summary()
        self.update_log_info_detail()
