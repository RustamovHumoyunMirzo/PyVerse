cmake_minimum_required(VERSION 3.16)
project(PyVerse LANGUAGES CXX)

include_directories("${CMAKE_SOURCE_DIR}/python_local/include")

add_library(pyverse SHARED src/pyverse.cpp)

target_link_libraries(pyverse PRIVATE "${CMAKE_SOURCE_DIR}/python_local/libs/python3.lib")
target_compile_definitions(pyverse PRIVATE Py_LIMITED_API=0x03080000)

set_target_properties(pyverse PROPERTIES
    PREFIX ""
    SUFFIX ".pyd"
    OUTPUT_NAME "pyverse"
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/pyverse"
)