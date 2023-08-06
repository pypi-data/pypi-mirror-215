# Fired Up

> conventions and supporting tools for using Fire in a more natural-ish style

[![Latest Version on PyPI](https://img.shields.io/pypi/v/fired-up.svg)](https://pypi.python.org/pypi/fired-up/)
[![Supported Implementations](https://img.shields.io/pypi/pyversions/fired-up.svg)](https://pypi.python.org/pypi/fired-up/)
[![Built with PyPi Template](https://img.shields.io/badge/PyPi_Template-v0.2.0-blue.svg)](https://github.com/christophevg/pypi-template)


## Your Fired Up Command Line

`Fire` is a fun module that allows for providing a quick and beautiful command line interface on top of a Python module. `Fired Up` adds some baseclasses and conventions to make this experience even more fun, by adding the possibility to chain multiple top-level commands/classes, using a shared clipboard.

### Minimal Survival Command

```console
% pip install fired-up
```

### An example

With `Fired Up` it is possible to run a command like this:

```console
% python examples/hello.py generate a_reversed_list 1,a,2,b then dump as_json
[
  "b",
  2,
  "a",
  1
]
```

The code to achieve this would be something like this:

```python
import json

from fired_up import FiredUp, Group

class Generator(Group):
  def a_reversed_list(self, lst):
    return list(reversed(lst))

class Dumper(Group):
  def as_json(self):
    return json.dumps(self.paste(), indent=2)

FiredUp(generate=Generator, dump=Dumper)
```

`Fired Up` provides the following support for creating a even "nicer" natural-ish command language: 

* a `Group` base class allows for simply creating a functional class, that has access to a `clipboard` using the `copy` and `paste` methods.
* a `FiredUp` top-level class to bring together the `Groups` and fire them up
* a `then` method on `Groups` allows to exit the `Group` scope and return to the top-level `FiredUp` class to access a different `Group`

### The Fire Guide Group Example

The [Fire Guide](https://google.github.io/python-fire/guide/#grouping-commands) has an example of grouping. With `FiredUp` this grouping is even improved upon:

Given a few alterations, the same and a lot more is possible:

```python
from fired_up import FiredUp, Group

class IngestionStage(Group):
  def run(self):
    return 'Ingesting! Nom nom nom...'

class DigestionStage(Group):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._volume = 1

  def volume(self, new_volume):
    self._volume = new_volume

  def run(self):
    return ' '.join(['Burp!'] * self._volume)

  def status(self):
    return 'Satiated.'

class Pipeline(FiredUp):
  def run(self):
    self.ingestion.run()
    ingestion_output = self.paste()
    self.digestion.run()
    digestion_output = self.paste()
    self.copy([ ingestion_output, digestion_output ])
    return self

if __name__ == "__main__":
  Pipeline(ingestion=IngestionStage, digestion=DigestionStage)
```

> I'm not happy yet with the required changes, so improvements will be imminent ;-)

For now, it runs the same and offers improved chaining possibilities:

```conole
% python examples/fire-group.py ingestion run
Ingesting! Nom nom nom...
% python examples/fire-group.py digestion run
Burp!
% python examples/fire-group.py digestion status
Satiated.
% python examples/fire-group.py ingestion run then digestion run status
Satiated.
% python examples/fire-group.py --all ingestion run then digestion run status
Ingesting! Nom nom nom...
Burp!
Satiated.
% python examples/fire-group.py --all ingestion run then digestion volume 2 run status
Ingesting! Nom nom nom...
Burp! Burp!
Satiated.
```

### Globals and Arguments

Besides the versioned clipboard, you can also use globals and pass arguments to the constructors of the Groups:

```python
from fired_up import FiredUp, Group

class Left(Group):
  def __init__(self, write, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._write = write

  def write(self):
    if self._write:
      self.globals["message"] = "left was here"

  def read(self):
    print("left>", self.globals["message"])

class Right(Group):
  def readwrite(self):
    print("right>", self.globals["message"])
    self.globals["message"] = "right was here too"

FiredUp(left=(Left, { "write" : True }), right=Right)
```

```console
% python examples/globals.py left write then right readwrite then left read
right> left was here
left> right was here too
```

### Menus

The FireUp class is kind of a Menu of Groups of Commands. You cal also nest Menus of your own:

```python
import json

from fired_up import FiredUp, Menu, Group

class Commands(Group):
  def run(self):
    print("Commands> running...")

class SubCommands(Group):
  def run(self):
    print("SubCommands> running...")

class SubSubCommands(Group):
  def run(self):
    print("SubSubCommands> running...")

FiredUp(
  commands=Commands,
  submenu=Menu(
    commands=SubCommands,
    subsubmenu=Menu(
      commands=SubSubCommands
    )
  )
)
```

```console
% python examples/nested.py commands run then submenu commands run then commands run then submenu subsubmenu commands run
Commands> running...
SubCommands> running...
Commands> running...
SubSubCommands> running...
```
