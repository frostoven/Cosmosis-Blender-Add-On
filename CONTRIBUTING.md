## General

We don't have many rules here. Just ensure you have a proper IDE setup, and
ensure you follow PEP 8 rules (any good IDE will warn you if PEP 8 rules are
not being followed).

## Basic IDE auto-completion
_Note: the below instructions are for IntelliJ, though they may help you figure
out how to do the same in other IDEs such as VSCode._

Start by installing the Python plugin, if not already installed.

In order for the IDE to offer completion suggestions for Blender, it needs to
read the Blender `bpy` module.

Start by opening up your copy of Blender, and go to the scripting tab. in the
console, run `bpy.__file__`. For example:
```idle
PYTHON INTERACTIVE CONSOLE 3.10.8 (main, Oct 18 2022, 21:01:35) [MSC v.1928 64 bit (AMD64)]

Builtin Modules:       bpy, bpy.data, bpy.ops, bpy.props, bpy.types, bpy.context, bpy.utils, bgl, blf, mathutils
Convenience Imports:   from mathutils import *; from math import *
Convenience Variables: C = bpy.context, D = bpy.data

>>> bpy.__file__
'C:\\Games\\Steam\\steamapps\\common\\Blender\\3.3\\scripts\\modules\\bpy\\__init__.py'

>>> 
```

Copy the output path that your command spits out.

Next, inside IntelliJ, go to `File -> Project Structure -> SDKs`.

If you do not already have a Python SDK setup click the `+` button in the top
left, select `Add Python SDK...` to set up the initial Python environment.
You'll want to try closely match the Python version that Blender is using,
because Python is notorious for hard-breaking features and changing syntax
across versions.
You may skip this step if you already have that set up (for new setups you
will also need to go to
`File -> Project Structure -> Project Settings -> Project` and ensure your
SDK is set there).

Once you have a Python SDK setup ready, ensure the `Classpath` tab is
selected, and then press the `+` button (this was called `Add...` in older
versions). Go to the directory of the file that `bpy.__file__` spat out, and
go 2 directories up to the `modules` directory. For example, if your `bpy`
file path is:
```
C:\MyDir\Blender\modules\bpy\__init__.py
```
then you'll want to select:
```
C:\MyDir\Blender\modules
```

Example:

![completion example](img/completion_example.png)

Your IDE should now resolve the `bpy` module and offer basic completion.
