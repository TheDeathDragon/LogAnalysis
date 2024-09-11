class MainLog:
    def __init__(self, _log_file):
        self.log_file = _log_file
        self.main_log = []
        self.analyze_main_log()

    def analyze_main_log(self):
        with open(self.log_file, 'r', encoding='UTF-8', errors='ignore') as f:
            for line in f:
                if ' W System.err:' in line:
                    self.main_log.append(line.replace('\n', ''))
                if ' E ActivityManager:' in line:
                    self.main_log.append(line.replace('\n', ''))
        return self.main_log

    def get_main_log(self):
        return self.main_log
