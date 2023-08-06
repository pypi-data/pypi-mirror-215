# This file is placed in the Public Domain.
#
# pylint: disable=C0114,C0115,C0116


"execute at a time"


import threading
import time


from .objects import Object
from .runtime import launch


def __dir__():
    return (
            'Timer',
           )


class Timer:

    def __init__(self, sleep, func, *args, thrname=None):
        super().__init__()
        self.args = args
        self.func = func
        self.sleep = sleep
        self.name = thrname or str(self.func).split()[2]
        self.state = Object
        self.timer = None

    def run(self) -> None:
        self.state.latest = time.time()
        launch(self.func, *self.args)

    def start(self) -> None:
        timer = threading.Timer(self.sleep, self.run)
        timer.name = self.name
        timer.daemon = True
        timer.sleep = self.sleep
        timer.state = self.state
        timer.state.starttime = time.time()
        timer.state.latest = time.time()
        timer.func = self.func
        timer.start()
        self.timer = timer

    def stop(self) -> None:
        if self.timer:
            self.timer.cancel()
