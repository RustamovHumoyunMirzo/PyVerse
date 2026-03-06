#define PY_SSIZE_T_CLEAN
#include <Python.h>

static PyObject* add(PyObject* self, PyObject* args)
{
    int a, b;

    if (!PyArg_ParseTuple(args, "ii", &a, &b))
        return NULL;

    return PyLong_FromLong(a + b);
}

static PyMethodDef Methods[] = {
    {"add", add, METH_VARARGS, "Add two numbers"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "pyverse",
    NULL,
    -1,
    Methods
};

PyMODINIT_FUNC PyInit_pyverse(void)
{
    return PyModule_Create(&module);
}