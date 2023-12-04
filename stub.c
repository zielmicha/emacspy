#include <Python.h>
#include <dlfcn.h>
#include <dlfcn.h>
#include <stdio.h>

int emacs_module_init_py(void* runtime);
void PyInit_emacspy(void);
extern int plugin_is_GPL_compatible;

int emacs_module_init(void* runtime) {
    Py_Initialize();
    PyInit_emacspy();
    int result = emacs_module_init_py(runtime);
    PyEval_SaveThread();
    return result;
}
