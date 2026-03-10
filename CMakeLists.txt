cmake_minimum_required(VERSION 3.18)
project(PyVerse LANGUAGES CXX)

find_package(pybind11 CONFIG REQUIRED)

set(SDL2_INCLUDE_DIR "${CMAKE_SOURCE_DIR}/deps/SDL2/include")
include_directories(
    ${SDL2_INCLUDE_DIR}
    ${CMAKE_SOURCE_DIR}/src/cpp
)

if(WIN32)
    set(SDL2_LIBRARY_DIR "${CMAKE_SOURCE_DIR}/deps/SDL2/lib/x64")
    set(SDL2_LIBS "SDL2")
    link_directories(${SDL2_LIBRARY_DIR})
elseif(APPLE OR UNIX)
    set(SDL2_LIBS "${CMAKE_SOURCE_DIR}/deps/SDL2/lib/libSDL2.a")
else()
    message(FATAL_ERROR "Unsupported platform")
endif()

pybind11_add_module(pyverse src/cpp/pyverse.cpp)

if(WIN32)
    target_link_libraries(pyverse PRIVATE ${SDL2_LIBS})
else()
    target_link_libraries(pyverse PRIVATE ${SDL2_LIBS})
endif()

set_target_properties(pyverse PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/pyverse"
)