#include <pybind11/pybind11.h>
#include <string>
#include <iostream>

namespace py = pybind11;

// Simple function: adds two numbers
int add(int a, int b) {
    return a + b;
}

// Stub class to represent a Window
class Window {
public:
    Window(const std::string& title, int width, int height)
        : title(title), width(width), height(height) {
        std::cout << "Creating window: " << title 
                  << " (" << width << "x" << height << ")" << std::endl;
    }

    void show() {
        std::cout << "Showing window: " << title << std::endl;
    }

    std::string get_title() const { return title; }
    int get_width() const { return width; }
    int get_height() const { return height; }

private:
    std::string title;
    int width, height;
};

// Module definition
PYBIND11_MODULE(pyverse, m) {
    m.doc() = "PyVerse C++ module for windowing and more";

    // Expose function
    m.def("add", &add, "Add two numbers");

    // Expose Window class
    py::class_<Window>(m, "Window")
        .def(py::init<const std::string&, int, int>())
        .def("show", &Window::show)
        .def("get_title", &Window::get_title)
        .def("get_width", &Window::get_width)
        .def("get_height", &Window::get_height);
}