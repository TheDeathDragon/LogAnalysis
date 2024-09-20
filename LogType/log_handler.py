import os
from LogType.main_log import MainLog
from LogType.crash_log import CrashLog
from LogType.system_log import SysLog
from LogType.event_log import EventLog
from LogType.property_log import PropLog

is_print_log = False
crash_log_prefix = 'crash_log_'
main_log_prefix = 'main_log_'
sys_log_prefix = 'sys_log_'
events_log_prefix = 'events_log_'
property_log = 'properties'


def get_log_text(log_list):
    log_text = ""
    for _ in log_list:
        if isinstance(_, list) and len(_) == 0:
            continue
        for line in _:
            log_text += line + "\n"
    return log_text


def get_property_log_text(prop):
    log_text = ''
    result = {}
    for _ in prop:
        # _ is a dict
        for key, value in _.items():
            if key not in result:
                result[key] = value
            else:
                if isinstance(result[key], list):
                    if value not in result[key]:
                        result[key].append(value)
                else:
                    if result[key] != value:
                        result[key] = [result[key], value]
    result = sorted(result.items(), key=lambda x: x[0], reverse=True)
    for key, value in result:
        if isinstance(value, list):
            log_text += key + ":" + str(value) + "\n"
        else:
            log_text += key + ":" + value + "\n"
    log_text.replace(' ', '')
    log_text.replace(':', ' : ')
    return log_text


class LogHandler:
    def __init__(self, _log_dir):
        print("log handler init +")
        self.ap_logs = []
        self.log_dir = _log_dir
        self.ap_log_dir_list = []
        self.ap_log_name_list = []
        self.all_log_name_list = []
        self.all_log_path_list = []
        self.all_crash_log_list = []
        self.all_main_log_list = []
        self.all_sys_log_list = []
        self.all_events_log_list = []
        self.all_property_log_list = []
        self.__analyze_all_log()
        print("log handler init -")

    def __analyze_all_log(self):
        self.__get_ap_log_dir_list()
        self.__get_all_log_files()
        self.__get_all_log_type_list()

    def print_log(self):
        if is_print_log:
            print("ap_log_dir_list count: ", len(self.ap_log_dir_list))
            print("crash_log_list count: ", len(self.all_crash_log_list))
            print("main_log_list count: ", len(self.all_main_log_list))
            print("sys_log_list count: ", len(self.all_sys_log_list))
            print("events_log_list count: ", len(self.all_events_log_list))
            print("property_log_list count: ", len(self.all_property_log_list))
            crash_log, crash_count = self.get_crash_log_all()
            print("crash count: ", crash_count)
            main_log = self.get_main_log_all()
            sys_log, anr_count = self.get_sys_log_all()
            print("anr count: ", anr_count)
            proc_log, activity_log, top_activity_log = self.get_event_log_all()
            properties_log = self.get_property_log_all()
            print("crash log: \n", get_log_text(crash_log))
            print("main log: \n", get_log_text(main_log))
            print("sys log: \n", get_log_text(sys_log))
            print("proc log: \n", get_log_text(proc_log))
            print("activity log: \n", get_log_text(activity_log))
            print("top activity log: \n", get_log_text(top_activity_log))
            print("properties log: \n", get_property_log_text(properties_log))

    def get_ap_log_name_list(self):
        return self.ap_log_name_list

    def get_crash_log_all(self):
        crash_log = []
        crash_count = 0
        for _ in self.all_crash_log_list:
            cl = CrashLog(_)
            crash_log.append(cl.get_crash_log())
            crash_count += cl.get_crash_count()
        return crash_log, crash_count

    def get_crash_log(self, ap_log_index):
        crash_log = []
        crash_count = 0
        ap_dir = self.ap_log_name_list[ap_log_index]
        for _ in self.all_crash_log_list:
            if ap_dir in _:
                cl = CrashLog(_)
                crash_log.append(cl.get_crash_log())
                crash_count += cl.get_crash_count()
        return crash_log, crash_count

    def get_main_log_all(self):
        main_log = []
        for _ in self.all_main_log_list:
            ml = MainLog(_)
            main_log.append(ml.get_main_log())
        return main_log

    def get_main_log(self, ap_log_index):
        main_log = []
        ap_dir = self.ap_log_name_list[ap_log_index]
        for _ in self.all_main_log_list:
            if ap_dir in _:
                ml = MainLog(_)
                main_log.append(ml.get_main_log())
        return main_log

    def get_sys_log_all(self):
        sys_log = []
        anr_count = 0
        for _ in self.all_sys_log_list:
            sl = SysLog(_)
            sys_log.append(sl.get_sys_log())
            anr_count += sl.get_anr_count()
        return sys_log, anr_count

    def get_sys_log(self, ap_log_index):
        sys_log = []
        anr_count = 0
        ap_dir = self.ap_log_name_list[ap_log_index]
        for _ in self.all_sys_log_list:
            if ap_dir in _:
                sl = SysLog(_)
                sys_log.append(sl.get_sys_log())
                anr_count += sl.get_anr_count()
        return sys_log, anr_count

    def get_event_log_all(self):
        proc_log = []
        activity_log = []
        top_activity_log = []
        for _ in self.all_events_log_list:
            el = EventLog(_)
            proc, activity, top_activity = el.get_events_log()
            proc_log.append(proc)
            activity_log.append(activity)
            top_activity_log.append(top_activity)
        return proc_log, activity_log, top_activity_log

    def get_event_log(self, ap_log_index):
        proc_log = []
        activity_log = []
        top_activity_log = []
        notification_log = []
        ap_dir = self.ap_log_name_list[ap_log_index]
        for _ in self.all_events_log_list:
            if ap_dir in _:
                el = EventLog(_)
                proc, activity, top_activity, notification = el.get_events_log()
                proc_log.append(proc)
                activity_log.append(activity)
                top_activity_log.append(top_activity)
                notification_log.append(notification)
        return proc_log, activity_log, top_activity_log, notification_log

    def get_property_log_all(self):
        properties_log = []
        for _ in self.all_property_log_list:
            pl = PropLog(_)
            properties = pl.get_prop_log()
            properties_log.append(properties)
        return properties_log

    def get_property_log(self, ap_log_index):
        properties = {}
        if ap_log_index >= len(self.ap_log_name_list):
            return properties
        ap_dir = self.ap_log_name_list[ap_log_index]
        for _ in self.all_property_log_list:
            if ap_dir in _:
                pl = PropLog(_)
                properties = pl.get_prop_log()
        return properties

    # find the APLog_ directory
    def __get_ap_log_dir_list(self):
        name_list = []
        dir_list = []
        for root, dirs, files in os.walk(self.log_dir):
            for _ in dirs:
                if _.startswith('APLog_'):
                    name_list.append(_)
                    # print("ap log name: ", _)
                    current_path = os.path.join(root, _)
                    # print("ap log dir : ", current_path)
                    dir_list.append(current_path)
        self.ap_log_name_list = name_list
        self.ap_log_dir_list = dir_list
        return name_list, dir_list

    # get the log files by the APLog_ directory
    def __get_all_log_files(self):
        ap_logs = []
        name_list = []
        path_list = []
        for ap_log_dir in self.ap_log_dir_list:
            print("current ap_log_dir: ", ap_log_dir)
            temp_name_list = []
            temp_path_list = []
            for root, dirs, files in os.walk(ap_log_dir):
                for file in files:
                    current_log_path = os.path.join(root, file)
                    temp_name_list.append(file)
                    temp_path_list.append(current_log_path)
            ap_logs.append([temp_name_list, temp_path_list])
            name_list.extend(temp_name_list)
            path_list.extend(temp_path_list)
        self.all_log_name_list, self.all_log_path_list = name_list, path_list
        self.ap_logs = ap_logs
        return ap_logs

    # get all log type list
    def __get_all_log_type_list(self):
        crash_log_list = []
        main_log_list = []
        sys_log_list = []
        events_log_list = []
        property_log_list = []
        pos = 0
        for log_file in self.all_log_name_list:
            if log_file.startswith(crash_log_prefix):
                crash_log_list.append(self.all_log_path_list[self.all_log_name_list.index(log_file)])
            elif log_file.startswith(main_log_prefix):
                main_log_list.append(self.all_log_path_list[self.all_log_name_list.index(log_file)])
            elif log_file.startswith(sys_log_prefix):
                sys_log_list.append(self.all_log_path_list[self.all_log_name_list.index(log_file)])
            elif log_file.startswith(events_log_prefix):
                events_log_list.append(self.all_log_path_list[self.all_log_name_list.index(log_file)])
            elif log_file == property_log:
                property_log_list.append(self.all_log_path_list[pos])
            pos += 1
        self.all_crash_log_list = crash_log_list
        self.all_main_log_list = main_log_list
        self.all_sys_log_list = sys_log_list
        self.all_events_log_list = events_log_list
        self.all_property_log_list = property_log_list
        return self.all_crash_log_list, self.all_main_log_list, self.all_sys_log_list, self.all_events_log_list, self.all_property_log_list

# if __name__ == "__main__":
#     origin_log_path = r'C:\Users\WangRuiLong\Desktop\C50v01出现报错\20240906_182930_log'
#     log_handler = LogHandler(origin_log_path)
