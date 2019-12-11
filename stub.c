#include <Python.h>
#include <dlfcn.h>

int emacs_module_init_py(void* runtime);
void PyInit_emacspy(void);

int emacs_module_init(void* runtime) {
    dlopen("libpython3.6m.so.1.0", RTLD_LAZY | RTLD_GLOBAL);
    Py_Initialize();
    PyInit_emacspy();
    int result = emacs_module_init_py(runtime);
    PyEval_SaveThread();
    return result;
}
