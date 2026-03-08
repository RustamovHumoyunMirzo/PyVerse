cmake_minimum_required(VERSION 3.18)
project(PyVerse LANGUAGES CXX)

find_package(Python3 REQUIRED COMPONENTS Interpreter Development)

add_library(pyverse MODULE src/cpp/pyverse.cpp)

target_include_directories(pyverse PRIVATE ${Python3_INCLUDE_DIRS})

set_target_properties(pyverse PROPERTIES
    PREFIX ""
    OUTPUT_NAME "pyverse"
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/pyverse"
)