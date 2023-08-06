"""

  conventions and supporting tools for using Fire in a more natural-ish
  language style

"""
__version__ = "0.0.4"

import sys
import functools

import fire

class Group():
  """
  
  baseclass for command groups
  
  """
  def __init__(self, _parent=None):
    self._parent = _parent

  @property
  def globals(self):
    return self._shared["globals"]

  @property
  def _shared(self):
    if self._parent:
      return self._parent._shared
    return None

  def then(self):
    return self._shared["exit"]

  def copy(self, value, name="default"):
    self._shared["clipboard"][name] = value
    return self

  def paste(self, name="default"):
    return self._shared["clipboard"][name]

def keep(method):
  @functools.wraps(method)
  def wrapper(self, *args, **kwargs):
    result = method(self, *args, **kwargs)
    self.copy(result)
    if result:
      next(self._shared["clipboard"])
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
    return [board["default"] for board in obj._shared["clipboard"]._boards[:-1] ]
else:
  def paste_result(obj):
    return obj.paste()

class Menu(Group):
  """
  
  a menu is a set of groups or other menus
  
  """
  def __init__(self, **kwargs):
    super().__init__()

    for group, clazz in kwargs.items():
      # unpack tuple(clazz, arguments)
      if type(clazz) is tuple:
        clazz, args = clazz
      else:
        args = {}
      # only handle classes, objects are used verbatim
      if isinstance(clazz, type):
        # make sure all public methods return self to allow for chaining
        for attr in clazz.__dict__:
          if callable(getattr(clazz, attr)) and attr != "__init__":
            setattr(clazz, attr, keep(getattr(clazz, attr)))
        self.__dict__[group] = clazz(_parent=self, **args)
      elif isinstance(clazz, Menu):
        # handle "sub"menu's, which are already created and need a ref to the
        # shared
        self.__dict__[group] = clazz
        clazz._parent = self
      else:
        raise ValueError("classes or Menu's, nothing else please")

class FiredUp(Menu):
  """
  
  the FiredUp class is the root-menu and holds the shared globals and clipboard
  
  """
  
  def __init__(self, name=None, **kwargs):
    super().__init__(**kwargs)
    self._actual_shared = {
      "clipboard" : Clipboards(),
      "globals"   : {},
      "exit"      : self
    }
    try:
      fire.Fire(self, name=name, serialize=paste_result)
    except KeyboardInterrupt:
      pass

  @property
  def _shared(self):
    return self._actual_shared
