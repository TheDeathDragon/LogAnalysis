class EventLog:
    def __init__(self, _log_file):
        self.log_file = _log_file
        self.proc_log = []
        self.activity_log = []
        self.top_activity_log = []
        self.analyze_events_log()

    def analyze_events_log(self):
        with open(self.log_file, 'r', encoding='UTF-8', errors='ignore') as f:
            for line in f:
                if ' I am_proc_start:' in line:
                    self.proc_log.append(line.replace('\n', ''))
                if ' I wm_create_activity:' in line:
                    self.activity_log.append(line.replace('\n', ''))
                if ' I wm_on_top_resumed_gained_called:' in line:
                    self.top_activity_log.append(line.replace('\n', ''))
        return self.proc_log, self.activity_log, self.top_activity_log

    def get_events_log(self):
        return self.proc_log, self.activity_log, self.top_activity_log

    def get_proc_log(self):
        return self.proc_log

    def get_activity_log(self):
        return self.activity_log

    def get_top_activity_log(self):
        return self.top_activity_log
