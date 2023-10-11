"""Модуль соответсвия названия кейворда соответсвующему классу."""
import types
from source.keywords import *

KEYWORDS_DISPATCH_DICT = types.MappingProxyType({
    'DEFINE_CURVE': DefineCurve,
    'DEFINE_CURVE_TITLE': DefineCurve,
    'SET_SHELL_LIST': SetShellList,
    'SET_SHELL_LIST_TITLE': SetShellList,
})
