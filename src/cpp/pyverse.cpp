#include <pybind11/pybind11.h>

namespace py = pybind11;

int add(int a, int b) {
    return a + b;
}

PYBIND11_MODULE(pyverse, m) {
    m.doc() = "PyVerse module";

    m.def("add", &add, "Add two numbers");
}