#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .exceptions import InvalidColor
from .library import Library


class MetaFore(type):
    """ Overrides AttributeError when __getattr__ called. """
    def __getattr__(cls, color):
        raise InvalidColor(f'{InvalidColor.__name__}: {color}')


class Fore(metaclass=MetaFore):

    END: str = Library.END
    COLORS: dict = Library.COLORS
    FOREGROUND: str = Library.FOREGROUND

    for color, code in COLORS.items():
        vars()[color] = f'{FOREGROUND}{code}{END}'
        vars()[color.upper()] = f'{FOREGROUND}{code}{END}'


class fore(Fore):
    """ This will be deprecated in the future, do not use this for version >= 2.0.0,
        instead please use Fore class (See issue #28). """
    pass
