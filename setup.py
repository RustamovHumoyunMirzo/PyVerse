import os
import sys
import platform
import subprocess
import shutil
from setuptools import setup, Extension, find_packages
import pybind11

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SDL_ROOT = os.path.join(BASE_DIR, "deps", "SDL2")
PLATFORM = platform.system()

def ensure_sdl():
    include = os.path.join(SDL_ROOT, "include", "SDL.h")
    if os.path.isfile(include):
        return
    print("SDL2 not found. Running download script...")
    subprocess.check_call([sys.executable, "scripts/download_sdl.py"])

def find_static_sdl():
    candidates = [
        os.path.join(SDL_ROOT, "lib", "libSDL2.a"),
        os.path.join(SDL_ROOT, "lib64", "libSDL2.a"),
        os.path.join(SDL_ROOT, "build", "libSDL2.a"),
    ]
    for c in candidates:
        if os.path.isfile(c):
            return c
    raise RuntimeError(
        "SDL2 static library not found after build. Checked:\n" +
        "\n".join(candidates)
    )

ensure_sdl()

include_dirs = [
    pybind11.get_include(),
    os.path.join(SDL_ROOT, "include"),
]

library_dirs = []
libraries = []
extra_objects = []
package_data = {}

if PLATFORM == "Windows":
    lib_dir = os.path.join(SDL_ROOT, "lib", "x64")
    library_dirs.append(lib_dir)
    libraries.append("SDL2")

    dll_src = os.path.join(lib_dir, "SDL2.dll")
    dll_dst = os.path.join(BASE_DIR, "src", "pyverse", "SDL2.dll")

    os.makedirs(os.path.dirname(dll_dst), exist_ok=True)

    if os.path.isfile(dll_src):
        shutil.copy2(dll_src, dll_dst)
        print("Copied SDL2.dll to package directory")
    else:
        raise RuntimeError("SDL2.dll not found in expected location")

    package_data = {"pyverse": ["SDL2.dll"]}

elif PLATFORM in ["Linux", "Darwin"]:
    static_lib = find_static_sdl()
    extra_objects = [static_lib]
    print("Using SDL static library:", static_lib)

else:
    raise RuntimeError(f"Unsupported platform: {PLATFORM}")

ext_modules = [
    Extension(
        "pyverse.pyverse",
        ["src/cpp/pyverse.cpp"],
        include_dirs=include_dirs,
        library_dirs=library_dirs,
        libraries=libraries,
        extra_objects=extra_objects,
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