import os
import sys
import platform
import urllib.request
import zipfile
import tarfile
import shutil
import subprocess

SDL_VERSION = "2.32.10"
BASE_DIR = os.path.abspath("deps/SDL2")
PLATFORM = sys.platform
ARCH = platform.architecture()[0]

def get_urls():
    urls = {}
    if PLATFORM.startswith("win"):
        urls["dev"] = f"https://www.libsdl.org/release/SDL2-devel-{SDL_VERSION}-VC.zip"
    elif PLATFORM.startswith("darwin") or PLATFORM.startswith("linux"):
        urls["tar"] = f"https://www.libsdl.org/release/SDL2-{SDL_VERSION}.tar.gz"
    else:
        raise RuntimeError(f"Unsupported platform: {PLATFORM}")
    return urls

def download_file(url, dest_path):
    if os.path.exists(dest_path):
        print(f"Already downloaded {dest_path}")
        return
    print(f"Downloading {url}...")
    urllib.request.urlretrieve(url, dest_path)
    print(f"Saved to {dest_path}")

def extract_zip(zip_path, dest_dir):
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(dest_dir)
    print(f"Extracted {zip_path} to {dest_dir}")

def extract_tar(tar_path, dest_dir):
    with tarfile.open(tar_path, "r:gz") as tar_ref:
        tar_ref.extractall(dest_dir)
    print(f"Extracted {tar_path} to {dest_dir}")

def ensure_sdl():
    include_path = os.path.join(BASE_DIR, "include", "SDL.h")
    lib_path = os.path.join(BASE_DIR, "lib")
    dll_path = os.path.join(lib_path, "SDL2.dll")

    if os.path.isfile(include_path) and (PLATFORM.startswith("win") and os.path.isfile(dll_path) or PLATFORM != "win"):
        print(f"SDL2 already exists at {BASE_DIR}")
        return

    os.makedirs(BASE_DIR, exist_ok=True)
    urls = get_urls()

    if PLATFORM.startswith("win"):
        dev_url = urls["dev"]
        dev_zip = os.path.join(BASE_DIR, os.path.basename(dev_url))
        download_file(dev_url, dev_zip)
        extract_zip(dev_zip, BASE_DIR)
        os.remove(dev_zip)

        lib_dir = os.path.join(BASE_DIR, "lib", "x64")
        dll_src = os.path.join(lib_dir, "SDL2.dll")
        dll_dst = os.path.join("src", "pyverse", "SDL2.dll")
        os.makedirs(os.path.dirname(dll_dst), exist_ok=True)
        if os.path.isfile(dll_src):
            shutil.copy2(dll_src, dll_dst)
            print(f"Copied SDL2.dll to {dll_dst}")
        else:
            print(f"Warning: SDL2.dll not found at {dll_src}")

    else:
        tar_path = os.path.join(BASE_DIR, os.path.basename(urls["tar"]))
        download_file(urls["tar"], tar_path)
        extract_tar(tar_path, BASE_DIR)
        os.remove(tar_path)

        src_dir = os.path.join(BASE_DIR, f"SDL2-{SDL_VERSION}")
        build_dir = os.path.join(BASE_DIR, "build")
        os.makedirs(build_dir, exist_ok=True)

        print("Building SDL2 (static)...")
        subprocess.check_call([
            "cmake",
            src_dir,
            "-DSDL_SHARED=OFF",
            "-DSDL_STATIC=ON",
            "-DCMAKE_POSITION_INDEPENDENT_CODE=ON",
            "-DCMAKE_INSTALL_PREFIX=" + BASE_DIR
        ], cwd=build_dir)

        subprocess.check_call([
            "cmake",
            "--build", ".",
            "--config", "Release",
            "--target", "install"
        ], cwd=build_dir)
        print("SDL2 built and installed successfully.")

    print(f"Listing all files in {BASE_DIR}:")

    BASE_DIRt = os.path.abspath("deps")
    for root, dirs, files in os.walk(BASE_DIRt):
        for name in files:
            file_path = os.path.join(root, name)
            rel_path = os.path.relpath(file_path, BASE_DIRt)
            print(f"- {rel_path}")

    if not os.path.isfile(include_path):
        print(f"ERROR: SDL2 headers not found at {include_path}")
        sys.exit(1)
    print(f"SDL2 is ready at {BASE_DIR}")

if __name__ == "__main__":
    ensure_sdl()