cmake_minimum_required(VERSION 3.18)
project(PyVerse LANGUAGES CXX)

find_package(pybind11 CONFIG REQUIRED)

set(SDL2_INCLUDE_DIR "${CMAKE_SOURCE_DIR}/deps/SDL2/include")
set(SDL2_LIBRARY_DIR "${CMAKE_SOURCE_DIR}/deps/SDL2/lib/x64")
set(SDL2_LIBS "SDL2")

include_directories(${SDL2_INCLUDE_DIR})

pybind11_add_module(pyverse src/cpp/pyverse.cpp)

target_link_directories(pyverse PRIVATE ${SDL2_LIBRARY_DIR})
target_link_libraries(pyverse PRIVATE ${SDL2_LIBS})

set_target_properties(pyverse PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/pyverse"
)