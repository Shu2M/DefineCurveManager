"""Модуль соответсвия названия кейворда соответсвующему классу."""
import types
from source.keywords import *

KEYWORDS_DISPATCH_DICT = types.MappingProxyType({
    'DEFINE_CURVE': DefineCurve,
})
