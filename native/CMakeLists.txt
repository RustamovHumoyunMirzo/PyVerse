cmake_minimum_required(VERSION 3.16)
project(PyVerse LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)

find_package(Python COMPONENTS Interpreter Development REQUIRED)
add_subdirectory(external/pybind11)

pybind11_add_module(pyverse pyverse.cpp)