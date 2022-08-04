# coding=utf-8
from multiprocessing import Event
from threading import Thread


class ThreadTimer(Thread):
    duration: float = 0

    time_interval: float = 0

    is_open: bool = False

    def __init__(self,
                 event: Event,
                 duration: float,
                 time_interval: float,
                 function: any,
                 args: tuple = ()):
        Thread.__init__(self)
        self.stopped = event
        self.duration = duration
        self.function = function
        self.time_interval = time_interval
        self.args = args

    def run(self):
        remain_time: float = self.time_interval
        while not self.stopped.wait(self.duration):
            remain_time = remain_time - 1
            if remain_time == 0:
                ret = self.function(*self.args)
                self.stopped.set()
                self.is_open = ret
            else:
                ret = self.function(*self.args)
                if ret:
                    self.stopped.set()
                    self.is_open = ret
                    break
