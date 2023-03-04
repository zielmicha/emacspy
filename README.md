# emacspy

emacspy enables you to program Emacs in Python instead of ELisp. It works by using dynamic modules support introduced in Emacs 25.

## Building and loading

Install Cython (`pip install cython`) and run `make`. `emacspy.so` will appear in the current directory. Make sure your Emacs build has loadable modules support enabled (default builds on some distributions don't!):

```
emacs --help | grep -q module-assertions && echo OK || echo "No loadable modules support"
```

You can load the module using normal `load` directive:

```
(add-to-list 'load-path "~/emacspy")
(load "~/emacspy/emacspy")
```

The module will expose two ELisp functions `eval-python` and `exec-python`.

```
(eval-python "4+4")
```

You can use `exec-python` to load you Python files:

```
(exec-python "import sys; sys.path.append('/home/user/my-files')")
(exec-python "import mymodule")
```

## Python

Emacspy also exposes Python API for interacting with Emacs. To use it import `emacspy` module.

```
import emacspy

# use emacspy.v to access Emacs variables
emacspy.v.tab_width

# use emacspy.f to call Emacs functions
emacspy.f.message("hello")

# returned values are wrapped in EmacsValue
emacspy.f["+"](1, 2) # => <EmacsValue ...>

# use functions to convert to Python values
emacspy.f["+"](1, 2).int()
emacspy.v.page_delimiter.str()
```
