import os
import platform
from setuptools import setup, Extension, find_packages
import pybind11
import shutil

SDL_ROOT = os.path.abspath("deps/SDL2")
PLATFORM = platform.system()

include_dirs = [pybind11.get_include()]
library_dirs = []
libraries = []

extra_objects = []

package_data = {}

if PLATFORM == "Windows":
    include_dirs.append(os.path.join(SDL_ROOT, "include"))
    library_dirs.append(os.path.join(SDL_ROOT, "lib", "x64"))
    libraries.append("SDL2")
    dll_src = os.path.join(SDL_ROOT, "bin", "SDL2.dll")
    dll_dst = os.path.join("src", "pyverse", "SDL2.dll")
    os.makedirs(os.path.dirname(dll_dst), exist_ok=True)
    if os.path.isfile(dll_src):
        shutil.copy2(dll_src, dll_dst)
        print(f"Copied SDL2.dll into {dll_dst}")
    else:
        print(f"Warning: {dll_src} not found, wheel may fail at runtime")
    
    package_data = {"pyverse": ["SDL2.dll"]}

elif PLATFORM == "Darwin" or PLATFORM.startswith("Linux"):
    include_dirs.append(os.path.join(SDL_ROOT, "include"))

    sdl_static = os.path.join(SDL_ROOT, "build", "libSDL2.a")

    if os.path.isfile(sdl_static):
        extra_objects = [sdl_static]
    else:
        raise RuntimeError("libSDL2.a not found. SDL must be built first.")

ext_modules = [
    Extension(
        "pyverse.pyverse",
        ["src/cpp/pyverse.cpp"],
        include_dirs=include_dirs,
        library_dirs=library_dirs,
        libraries=libraries,
        extra_objects=extra_objects if 'extra_objects' in globals() else [],
        language="c++",
        extra_compile_args=["-std=c++17"]
    )
]

setup(
    name="PyVerse",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    ext_modules=ext_modules,
    include_package_data=True,
    package_data=package_data,
)