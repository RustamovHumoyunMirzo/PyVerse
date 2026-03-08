import os
import sys
import shutil
import subprocess
import urllib.request
import zipfile

SDL_VERSION = "2.32.10"
BASE_DIR = os.path.abspath("deps/SDL2")

PLATFORM = sys.platform
IS_WINDOWS = PLATFORM.startswith("win")
IS_LINUX = PLATFORM.startswith("linux")
IS_MAC = PLATFORM.startswith("darwin")

def download_file(url, dest):
    if os.path.exists(dest):
        print("Already downloaded:", dest)
        return
    print("Downloading", url)
    urllib.request.urlretrieve(url, dest)

def flatten_folder(folder):
    for item in os.listdir(folder):
        src = os.path.join(folder, item)
        dst = os.path.join(BASE_DIR, item)

        if os.path.exists(dst):
            if os.path.isdir(dst):
                shutil.rmtree(dst)
            else:
                os.remove(dst)

        shutil.move(src, dst)

    shutil.rmtree(folder)

def ensure_windows_sdl():
    url = f"https://www.libsdl.org/release/SDL2-devel-{SDL_VERSION}-VC.zip"
    zip_path = os.path.join(BASE_DIR, os.path.basename(url))

    download_file(url, zip_path)

    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(BASE_DIR)

    os.remove(zip_path)

    top = os.path.join(BASE_DIR, f"SDL2-{SDL_VERSION}")
    if os.path.exists(top):
        flatten_folder(top)

    dll_src = os.path.join(BASE_DIR, "lib", "x64", "SDL2.dll")
    dll_dst = os.path.join("src", "pyverse", "SDL2.dll")

    os.makedirs(os.path.dirname(dll_dst), exist_ok=True)

    if os.path.isfile(dll_src):
        shutil.copy2(dll_src, dll_dst)
        print("Copied SDL2.dll")
    else:
        print("WARNING: SDL2.dll not found")

def ensure_unix_sdl():
    if not os.path.exists(os.path.join(BASE_DIR, "CMakeLists.txt")):
        print("Cloning SDL repository...")
        subprocess.check_call([
            "git", "clone",
            "--depth", "1",
            "--branch", f"release-{SDL_VERSION}",
            "https://github.com/libsdl-org/SDL.git",
            BASE_DIR
        ])

    build = os.path.join(BASE_DIR, "build")
    os.makedirs(build, exist_ok=True)

    print("Building SDL2 static...")

    subprocess.check_call([
        "cmake",
        "..",
        "-DSDL_SHARED=OFF",
        "-DSDL_STATIC=ON",
        "-DCMAKE_POSITION_INDEPENDENT_CODE=ON",
        f"-DCMAKE_INSTALL_PREFIX={BASE_DIR}"
    ], cwd=build)

    subprocess.check_call([
        "cmake",
        "--build",
        ".",
        "--target",
        "install",
        "--config",
        "Release"
    ], cwd=build)

def verify():
    include = os.path.join(BASE_DIR, "include", "SDL.h")

    if not os.path.isfile(include):
        print("ERROR: SDL headers missing:", include)
        sys.exit(1)

    if not IS_WINDOWS:
        possible = [
            os.path.join(BASE_DIR, "lib", "libSDL2.a"),
            os.path.join(BASE_DIR, "lib64", "libSDL2.a"),
            os.path.join(BASE_DIR, "build", "libSDL2.a")
        ]

        if not any(os.path.isfile(p) for p in possible):
            print("ERROR: SDL static library not found.")
            print("Checked:", possible)
            sys.exit(1)

def ensure_sdl():
    if os.path.exists(os.path.join(BASE_DIR, "include", "SDL.h")):
        print("SDL already prepared.")
        return

    os.makedirs(BASE_DIR, exist_ok=True)

    if IS_WINDOWS:
        ensure_windows_sdl()
    else:
        ensure_unix_sdl()

    verify()

    print("SDL2 setup complete.")

if __name__ == "__main__":
    ensure_sdl()