import os
import platform
from setuptools import setup, Extension, find_packages
import pybind11

SDL_ROOT = os.path.abspath("deps/SDL2")
PLATFORM = platform.system()

include_dirs = [pybind11.get_include()]
library_dirs = []
libraries = []

package_data = {}

if PLATFORM == "Windows":
    include_dirs.append(os.path.join(SDL_ROOT, "include"))
    library_dirs.append(os.path.join(SDL_ROOT, "lib", "x64"))
    libraries.append("SDL2")

    dll_path = os.path.join(SDL_ROOT, "bin", "SDL2.dll")
    if os.path.isfile(dll_path):
        package_data["pyverse"] = ["SDL2.dll"]
    else:
        print("Warning: SDL2.dll not found, the Windows wheel may fail at runtime!")

elif PLATFORM == "Darwin":
    include_dirs.append(os.path.join(SDL_ROOT, "include"))
    library_dirs.append(os.path.join(SDL_ROOT, "lib"))
    libraries.append("SDL2")
elif PLATFORM.startswith("Linux"):
    include_dirs.append(os.path.join(SDL_ROOT, "include"))
    library_dirs.append(os.path.join(SDL_ROOT, "lib"))
    libraries.append("SDL2")

ext_modules = [
    Extension(
        "pyverse.pyverse",
        ["src/cpp/pyverse.cpp"],
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
    include_package_data=True,
    package_data=package_data,
)