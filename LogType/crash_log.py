class CrashLog:
    def __init__(self, _log_file):
        self.log_file = _log_file
        self.crash_count = 0
        self.crash_log = []
        self.analyze_crash_log()

    def analyze_crash_log(self):
        with open(self.log_file, 'r', encoding='UTF-8', errors='ignore') as f:
            for line in f:
                if 'AndroidRuntime:' in line:
                    if 'FATAL EXCEPTION' in line:
                        if self.crash_count > 0:
                            self.crash_log.append('\n' + line.replace('\n', ''))
                        else:
                            self.crash_log.append(line.replace('\n', ''))
                        self.crash_count += 1
                    else:
                        self.crash_log.append(line.replace('\n', ''))
        return self.crash_log

    def get_crash_log(self):
        return self.crash_log

    def get_crash_count(self):
        return self.crash_count
