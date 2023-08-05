from temper_core import TemperObject as TemperObject0, str_cat as str_cat_1239, list_join as list_join_1214, bool_not as bool_not_1222, list_builder_add as list_builder_add_1218
from typing import List as List6, Callable as Callable3
from builtins import list as list_1244
from temper_core import LoggingConsole
vGlobalConsole__36_1245 = LoggingConsole(__name__)
class TestFixtureBase(TemperObject0):
  __slots__ = ()
passing__3: 'bool' = True
t_72: 'List6[str]' = list_1244()
messages__4: 'List6[str]' = t_72
def test(name__5: 'str', body__6: 'Callable3[[], None]') -> 'None':
  global messages__4, passing__3, vGlobalConsole__36_1245
  return__1: 'None'
  t_67: 'Callable3[[str], str]'
  t_68: 'str'
  return__1 = None
  passing__3 = True
  t_63: 'List6[str]' = list_1244()
  messages__4 = t_63
  body__6()
  if passing__3:
    vGlobalConsole__36_1245.log(str_cat_1239(name__5, ': Passed'))
  else:
    def fn__61(it__8: 'str') -> 'str':
      return__42: 'str'
      return__42 = it__8
      return return__42
    t_67 = fn__61
    t_68 = list_join_1214(messages__4, '\n', t_67)
    vGlobalConsole__36_1245.log(str_cat_1239(name__5, ': Failed ', t_68))
  return return__1
def assert13(success__9: 'bool', message__10: 'Callable3[[], str]') -> 'None':
  global messages__4, passing__3
  return__2: 'None'
  t_58: 'str'
  return__2 = None
  if bool_not_1222(success__9):
    passing__3 = False
    t_58 = message__10()
    list_builder_add_1218(messages__4, t_58)
  return return__2
return__41: 'None' = None
export = return__41
