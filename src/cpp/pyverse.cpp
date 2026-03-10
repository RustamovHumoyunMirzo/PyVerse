#include <pybind11/pybind11.h>
#include "window.h"
#include "app.h"

namespace py = pybind11;

PYBIND11_MODULE(pyverse, m)
{
    py::class_<Window>(m, "Window")
        .def(py::init<int, int>())
        .def("show", &Window::show)
        .def("destroy", &Window::destroy);

    m.def("_run_engine", &run_engine);
}