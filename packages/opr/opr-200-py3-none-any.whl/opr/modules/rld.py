# This file is placed in the Public Domain.
#
# pylint: disable=C0116


"reload"


from .. import modules


from ..command import Commands


def rld(event):
    if not event.args:
        event.reply("rld <modname>")
        return
    modname = event.args[0]
    mod = getattr(modules, modname)
    if not mod:
        event.reply(f"{modname} is not available")
        return
    Commands.scan(mod)
    event.reply(f"reloaded {modname}")


def unl(event):
    if not event.args:
        event.reply("rld <modname>")
        return
    modname = event.args[0]
    if modname == "rld":
        event.reply("won't unload myself")
        return
    mod = getattr(modules, modname)
    if not mod:
        event.reply(f"{modname} is not available")
        return
    Commands.remove(mod)
    event.reply(f"unloaded {modname}")
