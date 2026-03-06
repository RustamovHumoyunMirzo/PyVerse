#define Py_LIMITED_API 0x03080000
#include <Python.h>

static PyObject* add(PyObject* self, PyObject* args) {
    int a, b;

    if (!PyArg_ParseTuple(args, "ii", &a, &b))
        return NULL;

    return PyLong_FromLong(a + b);
}

static PyMethodDef methods[] = {
    {"add", add, METH_VARARGS, "Add two numbers"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "pyverse",
    "PyVerse Native Module",
    -1,
    methods
};

PyMODINIT_FUNC PyInit_pyverse(void) {
    return PyModule_Create(&module);
}