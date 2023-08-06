# This file is placed in the Public Domain
#
# pylama: ignore=E402,W0611,W0401,C901


"""Skull, Bones and Number (OTP-CR-117/19)


    SBN is a python3 IRC bot is intended to be programmable  in a
    static, only code, no popen, no user imports and no reading modules from
    a directory, way. It can show genocide and suicide stats of king netherlands
    his genocide into a IRC channel, display rss feeds and log simple text
    messages.

    SBN contains correspondence <writings> with the International Criminal Court, 
    asking for arrest of the king of the  netherlands, for the genocide he is
    committing with his new treatement laws. Current status is "no basis to
    proceed" judgement of the prosecutor which requires a basis to prosecute
    <reconsider> to have the king actually arrested.


SYNOPSIS

    sbn <cmd> [key=val] 
    sbn <cmd> [key==val]
    sbn [-c] [-d] [-v]


INSTALL


    $ pipx install sbn


USAGE


    list of commands

    $ sbn cmd
    cmd,err,flt,sts,thr,upt


    start a console

    $ sbn -c
    >

    start additional modules

    $ sbn mod=<mod1,mod2> -c
    >

    list of modules

    $ sbn mod
    cmd,err,flt,fnd,irc,log,mdl,mod,
    req, rss,slg,sts,tdo,thr,upt,ver

    to start irc, add mod=irc when
    starting

    $ sbn mod=irc -c

    to start rss, also add mod=rss
    when starting

    $ sbn mod=irc,rss -c

    start as daemon

    $ sbn  mod=irc,rss -d
    $ 


CONFIGURATION


 irc

    $ sbn cfg server=<server>
    $ sbn cfg channel=<channel>
    $ sbn cfg nick=<nick>

 sasl

    $ sbn pwd <nsvnick> <nspass>
    $ sbn cfg password=<frompwd>

 rss

    $ sbn rss <url>
    $ sbn dpl <url> <item1,item2>
    $ sbn rem <url>
    $ sbn nme <url< <name>


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

    ~/.local/bin/sbn
    ~/.local/pipx/venvs/sbn/


AUTHOR

    Bart Thate <bthate@dds.nl>


COPYRIGHT

    SBN is Public Domain.

"""


__version__ = "3"


from . import clients, clocked, command, configs, decoder, default, defines
from . import encoder, errored, evented, handler, listens, logging, objects
from . import objfunc, parsers, persist, repeats, runtime, threads, utility


from .objects import *
from .objfunc import *
from .command import Commands
from .persist import *


def __dir__():
    return (
            'Object',
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
