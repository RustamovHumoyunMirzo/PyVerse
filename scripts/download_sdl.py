import os
import sys
import platform
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

ARCH = platform.architecture()[0]

def download_file(url, dest_path):
    if os.path.exists(dest_path):
        print(f"Already downloaded: {dest_path}")
        return
    print(f"Downloading {url} ...")
    urllib.request.urlretrieve(url, dest_path)
    print(f"Saved to {dest_path}")

def extract_zip(zip_path, dest_dir):
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(dest_dir)
    print(f"Extracted {zip_path} to {dest_dir}")

def flatten_folder(top_dir, target_dir):
    for item in os.listdir(top_dir):
        src = os.path.join(top_dir, item)
        dst = os.path.join(target_dir, item)
        if os.path.exists(dst):
            if os.path.isdir(dst):
                shutil.rmtree(dst)
            else:
                os.remove(dst)
        shutil.move(src, dst)
    shutil.rmtree(top_dir)
    print(f"Flattened {top_dir} into {target_dir}")

def ensure_sdl():
    include_path = os.path.join(BASE_DIR, "include", "SDL.h")
    lib_path = os.path.join(BASE_DIR, "lib")

    dll_path = os.path.join(lib_path, "SDL2.dll")
    if os.path.isfile(include_path) and (IS_WINDOWS and os.path.isfile(dll_path) or not IS_WINDOWS):
        print(f"SDL2 already exists at {BASE_DIR}")
        return

    os.makedirs(BASE_DIR, exist_ok=True)

    if IS_WINDOWS:
        url = f"https://www.libsdl.org/release/SDL2-devel-{SDL_VERSION}-VC.zip"
        zip_path = os.path.join(BASE_DIR, os.path.basename(url))
        download_file(url, zip_path)
        extract_zip(zip_path, BASE_DIR)
        os.remove(zip_path)

        top_dir = os.path.join(BASE_DIR, f"SDL2-{SDL_VERSION}")
        if os.path.exists(top_dir):
            flatten_folder(top_dir, BASE_DIR)

        dll_src = os.path.join(BASE_DIR, "lib", "x64", "SDL2.dll")
        dll_dst = os.path.join("src", "pyverse", "SDL2.dll")
        os.makedirs(os.path.dirname(dll_dst), exist_ok=True)
        if os.path.isfile(dll_src):
            shutil.copy2(dll_src, dll_dst)
            print(f"Copied SDL2.dll to {dll_dst}")
        else:
            print(f"Warning: SDL2.dll not found at {dll_src}")

    else:
        if not os.path.exists(os.path.join(BASE_DIR, "CMakeLists.txt")):
            print(f"Cloning SDL2 CMake repo (release-{SDL_VERSION})...")
            subprocess.check_call([
                "git", "clone",
                "--branch", f"release-{SDL_VERSION}",
                "https://github.com/libsdl-org/SDL.git",
                BASE_DIR
            ])
        else:
            print("SDL2 repo already cloned")

        build_dir = os.path.join(BASE_DIR, "build")
        os.makedirs(build_dir, exist_ok=True)
        print("Building SDL2 (static)...")
        subprocess.check_call([
            "cmake",
            BASE_DIR,
            "-DSDL_SHARED=OFF",
            "-DSDL_STATIC=ON",
            "-DCMAKE_POSITION_INDEPENDENT_CODE=ON",
            f"-DCMAKE_INSTALL_PREFIX={BASE_DIR}"
        ], cwd=build_dir)

        subprocess.check_call([
            "cmake",
            "--build", ".",
            "--config", "Release",
            "--target", "install"
        ], cwd=build_dir)

        print("SDL2 built and installed successfully.")

    if not os.path.isfile(include_path):
        print(f"ERROR: SDL2 headers not found at {include_path}")
        sys.exit(1)

    if not IS_WINDOWS:
        lib_static = os.path.join(lib_path, "libSDL2.a")
        if not os.path.isfile(lib_static):
            sys.exit(1)

    print(f"SDL2 is ready at {BASE_DIR}")

if __name__ == "__main__":
    ensure_sdl()