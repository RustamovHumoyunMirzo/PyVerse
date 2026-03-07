#include <Python.h>

static PyObject* hello(PyObject* self, PyObject* args) {
    return PyUnicode_FromString("Hello from PyVerse!");
}

static PyMethodDef PyVerseMethods[] = {
    {"hello", hello, METH_NOARGS, "Say hello"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef pyversemodule = {
    PyModuleDef_HEAD_INIT,
    "pyverse",
    "PyVerse module",
    -1,
    PyVerseMethods
};

PyMODINIT_FUNC PyInit_pyverse(void) {
    return PyModule_Create(&pyversemodule);
}