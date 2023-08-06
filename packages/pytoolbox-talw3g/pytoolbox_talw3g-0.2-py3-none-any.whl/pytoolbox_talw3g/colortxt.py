#! /usr/bin/env python3
# -*- coding: utf-8 -*-

def ctxt(txt, fgcol='default', bgcol='default', blink=False):
    """
    Returns a string with instructions to change appearance of 'txt'
    in Unix-like terminals.

    PARAMETERS:
    - txt is mandatory, and must be convertible to string.
    - fgcol is optional, and sets the foreground color (see colors below).
    - bgcol is optional, and sets the background color (see colors below).
    - blink is optional, and if true makes the foreground blink.
    If not set, optional parameters default to terminal's defaults and blink OFF.
    Exception handling is at the charge of the caller.

    Available color codes are:
    - 'default': terminal's default
    - 'blk': black
    - 'wht': white
    - 'grey': grey
    - 'lgrey': light grey
    - 'red': red
    - 'lred': light red
    - 'blue': blue
    - 'lblue': light blue
    - 'grn': green
    - 'lgrn': light green
    - 'yel': yellow
    - 'lyel': light yellow
    - 'cya': cyan
    - 'lcya': light cyan
    """

    FGCOLORS = {
        'default': '\033[39m',
        'blk': '\033[30m',
        'wht': '\033[37m',
        'grey': '\033[90m',
        'lgrey': '\033[37m',
        'red': '\033[31m',
        'lred': '\033[91m',
        'blue': '\033[34m',
        'lblue': '\033[94m',
        'grn': '\033[32m',
        'lgrn': '\033[92m',
        'yel': '\033[33m',
        'lyel': '\033[93m',
        'cya': '\033[36m',
        'lcya': '\033[96m',
        }
    BGCOLORS = {
        'default': '\033[49m',
        'blk': '\033[40m',
        'wht': '\033[47m',
        'grey': '\033[100m',
        'lgrey': '\033[47m',
        'red': '\033[41m',
        'lred': '\033[101m',
        'blue': '\033[44m',
        'lblue': '\033[104m',
        'grn': '\033[42m',
        'lgrn': '\033[102m',
        'yel': '\033[43m',
        'lyel': '\033[103m',
        'cya': '\033[46m',
        'lcya': '\033[106m',
        }

    txt = str(txt)
    reset_all = '\033[0m'

    if fgcol not in FGCOLORS:
        raise ValueError('Wrong foreground color: ' + fgcol)
    s = FGCOLORS[fgcol]
    if bgcol not in BGCOLORS:
        raise ValueError('Wrong background color: ' + bgcol)
    s += BGCOLORS[bgcol]
    if blink:
        s += '\033[5m'

    return s + txt + reset_all

