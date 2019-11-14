#include <Python.h>

int emacs_module_init_py(void* runtime);
void PyInit_emacspy(void);

int emacs_module_init(void* runtime) {
    Py_Initialize();
    PyInit_emacspy();
    return emacs_module_init_py(runtime);
}
