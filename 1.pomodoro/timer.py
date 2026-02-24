import time

class PomodoroTimer:
    def __init__(self, work_minutes=25, break_minutes=5):
        self.work_seconds = work_minutes * 60
        self.break_seconds = break_minutes * 60
        self.state = 'work'  # 'work' or 'break'
        self.remaining = self.work_seconds
        self.running = False

    def start(self):
        self.running = True
        self.state = 'work'
        self.remaining = self.work_seconds

    def tick(self):
        if self.running and self.remaining > 0:
            self.remaining -= 1
        return self.remaining

    def switch(self):
        if self.state == 'work':
            self.state = 'break'
            self.remaining = self.break_seconds
        else:
            self.state = 'work'
            self.remaining = self.work_seconds

    def reset(self):
        if self.state == 'work':
            self.remaining = self.work_seconds
        else:
            self.remaining = self.break_seconds
        self.running = False

    def is_finished(self):
        return self.remaining == 0
