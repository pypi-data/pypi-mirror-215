# This file is placed in the Public Domain.
#
# pylint: disable=E0012,C0114,C0115,C0116,C0413,E0401,W0212,W0611,W1514,R1732
# pylint: disable=E0611
# flake8: noqa: E402
# pylama: ignore=W0611,E402

import os
import readline
import sys
import termios
import time


from .clients import Client
from .command import Commands
from .logging import Logging
from .persist import Persist
from .runtime import DATE, NAME, Cfg, command, parse_cli
from .runtime import scanstr, waiter


from . import  modules
Commands.modules = modules


__VERSION__ = "200"


NAME = "opr"


Persist.workdir = os.path.expanduser(f"~/.{NAME}")


class CLI(Client):

    def announce(self, txt):
        pass

    def raw(self, txt):
        print(txt)


class Console(CLI):

    def handle(self, evt):
        CLI.handle(self, evt)
        evt.wait()

    def poll(self):
        return self.event(input("> "))


def banner():
    print(f"{NAME.upper()} started {DATE}")
    sys.stdout.flush()


def daemon():
    pid = os.fork()
    if pid != 0:
        os._exit(0)
    os.setsid()
    os.umask(0)
    sis = open('/dev/null', 'r')
    os.dup2(sis.fileno(), sys.stdin.fileno())
    sos = open('/dev/null', 'a+')
    ses = open('/dev/null', 'a+')
    os.dup2(sos.fileno(), sys.stdout.fileno())
    os.dup2(ses.fileno(), sys.stderr.fileno())


def wrap(func):
    fds = sys.stdin.fileno()
    gotterm = True
    try:
        old = termios.tcgetattr(fds)
    except termios.error:
        gotterm = False
    try:
        func()
    except (EOFError, KeyboardInterrupt):
        pass
    finally:
        if gotterm:
            termios.tcsetattr(fds, termios.TCSADRAIN, old)
        waiter()


def ver(event):
    event.reply(f"{NAME.upper()} version {__VERSION__}")


def main():
    parse_cli(' '.join(sys.argv[1:]))
    if "v" in Cfg.opts and "d" not in Cfg.opts:
        Logging.verbose = True
        Logging.raw = print
    Commands.add(ver)
    dowait = False
    if Cfg.txt:
        scanstr(modules, Cfg.mod, doall=True)
        cli = CLI()
        command(cli, Cfg.otxt)
    elif 'd' in Cfg.opts:
        daemon()
        dowait = True
    if "c" in Cfg.opts:
        dowait = True
    if dowait:
        banner()
        if 'c' in Cfg.opts and "d" not in Cfg.opts:
            csl = Console()
            csl.start()
        scanstr(modules, Cfg.mod)
        scanstr(modules, Cfg.mod, True, wait=True)
        while 1:
            time.sleep(1.0)
            waiter()


if __name__ == "__main__":
    wrap(main)
