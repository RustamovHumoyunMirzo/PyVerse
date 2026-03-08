cmake_minimum_required(VERSION 3.18)
project(PyVerse LANGUAGES CXX)

find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(pyverse src/cpp/pyverse.cpp)

set_target_properties(pyverse PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/pyverse"
)