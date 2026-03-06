cmake_minimum_required(VERSION 3.15)
project(pyverse)

find_package(Python3 COMPONENTS Interpreter Development.Module REQUIRED)

add_library(pyverse MODULE src/pyverse.cpp)

target_compile_definitions(pyverse PRIVATE
    Py_LIMITED_API=0x03080000
)

set_target_properties(pyverse PROPERTIES
    PREFIX ""
    OUTPUT_NAME "pyverse"
)