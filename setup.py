from setuptools import setup, Extension, find_packages
import pybind11
import os
import platform

SDL_ROOT = os.path.abspath("deps")

include_dirs = [
    pybind11.get_include(),
]

library_dirs = []
libraries = []

system = platform.system()

if system == "Windows":
    include_dirs.append(os.path.join(SDL_ROOT, "SDL2-2.32.10", "include"))
    library_dirs.append(os.path.join(SDL_ROOT, "SDL2-2.32.10", "lib", "x64"))
    libraries.append("SDL2")

ext_modules = [
    Extension(
        "pyverse.pyverse",
        ["src/cpp/window.cpp"],
        include_dirs=include_dirs,
        library_dirs=library_dirs,
        libraries=libraries,
        language="c++",
    )
]

setup(
    name="PyVerse",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    ext_modules=ext_modules,
)