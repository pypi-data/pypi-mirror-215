# This file is placed in the Public Domain
#
# pylama: ignore=E402,W0611,W0401,C901


"""Object Programming Runtime"


OPR is a python3 IRC bot is intended to be programmable in a
static, only code, no popen, no user imports and no reading
modules from a directory, way. 


SYNOPSIS

    opr <cmd> [key=val] 
    opr <cmd> [key==val]
    opr [-c] [-d] [-v]


INSTALL


    $ pipx install opr


USAGE


    list of commands

    $ opr cmd
    cmd,err,flt,sts,thr,upt


    start a console

    $ opr -c
    >

    start additional modules

    $ opr mod=<mod1,mod2> -c
    >

    list of modules

    $ opr mod
    cmd,err,flt,fnd,irc,log,mdl,mod,
    req, rss,slg,sts,tdo,thr,upt,ver

    to start irc, add mod=irc when
    starting

    $ opr mod=irc -c

    to start rss, also add mod=rss
    when starting

    $ opr mod=irc,rss -c

    start as daemon

    $ opr  mod=irc,rss -d
    $ 


CONFIGURATION


 irc

    $ opr cfg server=<server>
    $ opr cfg channel=<channel>
    $ opr cfg nick=<nick>

 sasl

    $ opr pwd <nsvnick> <nspass>
    $ opr cfg password=<frompwd>

 rss

    $ opr rss <url>
    $ opr dpl <url> <item1,item2>
    $ opr rem <url>
    $ opr nme <url< <name>


COMMANDS

    cmd - commands
    cfg - irc configuration
    dlt - remove a user
    dpl - sets display items
    ftc - runs a fetching batch
    fnd - find objects 
    flt - instances registered
    log - log some text
    mdl - genocide model
    met - add a user
    mre - displays cached output
    nck - changes nick on irc
    now - genocide stats
    pwd - sasl nickserv name/pass
    rem - removes a rss feed
    req - reconsider
    rss - add a feed
    slg - slogan
    thr - show the running threads
    tpc - genocide stats into topic


FILES

    ~/.local/bin/opr
    ~/.local/pipx/venvs/opr/


AUTHOR

    Bart Thate <bthate@dds.nl>


COPYRIGHT

    OPR is placed in the Public Domain.

"""


__version__ = "13"


from . import clients, clocked, command, configs, decoder, default, defines
from . import encoder, errored, evented, handler, listens, logging, objects
from . import objfunc, parsers, persist, repeats, runtime, threads, utility


from .objects import *
from .objfunc import *
from .command import Commands
from .persist import *


def __dir__():
    return (
            'copy',
            'dump',
            'dumprec',
            'edit',
            'ident',
            'items',
            'keys',
            'kind',
            'load',
            'prt',
            'read',
            'readrec',
            'search',
            'update',
            'values',
            'write',
            'writerec'
           )


__all__ = __dir__()
