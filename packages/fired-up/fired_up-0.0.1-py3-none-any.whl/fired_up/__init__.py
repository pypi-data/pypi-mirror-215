"""

  conventions and supporting tools for using Fire in a more natural-ish
  language style

"""
__version__ = "0.0.1"

import sys
import functools

import fire

class Group():
  """
  
  baseclass for command groups
  
  """
  def __init__(self, _shared=None, _exit=None):
    self._shared = _shared
    self._exit   = _exit

  def then(self):
    # next(self._shared)
    return self._exit

  def copy(self, value, name="default"):
    self._shared[name] = value
    return self

  def paste(self, name="default"):
    return self._shared[name]

def keep(method):
  @functools.wraps(method)
  def wrapper(self, *args, **kwargs):
    result = method(self, *args, **kwargs)
    self.copy(result)
    if result:
      next(self._shared)
    return self
  return wrapper

class Clipboards():
  """
  
  simple multi-clipboard support
  
  """
  def __init__(self):
    self._boards = []
    next(self)

  def __next__(self):
    self._boards.append({"default": self["default"]})

  def __setitem__(self, key, value):
    self._boards[-1][key] = value

  def __getitem__(self, key):
    try:
      return self._boards[-1][key]
    except:
      pass
    return None

  def __str__(self):
    return str(self._boards)

if "--all" in sys.argv:
  sys.argv.remove("--all")
  def paste_result(obj):
    return [board["default"] for board in obj._shared._boards[:-1] ]
else:
  def paste_result(obj):
    return obj.paste()

class FiredUp(Group):
  def __init__(self, name=None, *args, **kwargs):
    self._shared = Clipboards()
    for group, clazz in kwargs.items():
      for attr in clazz.__dict__:
        if callable(getattr(clazz, attr)) and attr != "__init__":
          setattr(clazz, attr, keep(getattr(clazz, attr)))
      self.__dict__[group] = clazz(_shared=self._shared, _exit=self)
    try:
      fire.Fire(self, name=name, serialize=paste_result)
    except KeyboardInterrupt:
      pass
