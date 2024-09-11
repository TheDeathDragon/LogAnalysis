class SysLog:
    def __init__(self, _log_file):
        self.log_file = _log_file
        self.sys_log = []
        self.analyze_sys_log()

    def analyze_sys_log(self):
        with open(self.log_file, 'r', encoding='UTF-8', errors='ignore') as f:
            for line in f:
                if ' I WindowManager: ANR' in line:
                    self.sys_log.append(line.replace('\n', ''))
        return self.sys_log

    def get_sys_log(self):
        return self.sys_log

    def get_anr_count(self):
        return len(self.sys_log)