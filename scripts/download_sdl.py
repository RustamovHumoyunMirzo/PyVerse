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
    elif PLATFORM.startswith("linux") or PLATFORM.startswith("darwin"):
        urls["tar"] = f"https://www.libsdl.org/release/SDL2-{SDL_VERSION}.tar.gz"
    else:
        raise RuntimeError(f"Unsupported platform: {PLATFORM}")
    return urls

def download_file(url, dest_path):
    if os.path.exists(dest_path):
        print(f"Already downloaded: {dest_path}")
        return
    print(f"Downloading {url} ...")
    urllib.request.urlretrieve(url, dest_path)
    print(f"Saved to {dest_path}")

def extract_zip(zip_path, dest_dir):
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        members = zip_ref.namelist()
        top_level = members[0].split("/")[0]
        for member in members:
            path_inside_zip = "/".join(member.split("/")[1:])
            if not path_inside_zip:
                continue
            target_path = os.path.join(dest_dir, path_inside_zip)
            if member.endswith("/"):
                os.makedirs(target_path, exist_ok=True)
            else:
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                with open(target_path, "wb") as f:
                    f.write(zip_ref.read(member))
    print(f"Extracted {zip_path} to {dest_dir}")

def extract_tar(tar_path, dest_dir):
    with tarfile.open(tar_path, "r:gz") as tar_ref:
        members = tar_ref.getmembers()
        top_level = members[0].name.split("/")[0]
        tar_ref.extractall(dest_dir)
    print(f"Extracted {tar_path} to {dest_dir}")

    extracted_dir = os.path.join(dest_dir, top_level)
    for item in os.listdir(extracted_dir):
        src = os.path.join(extracted_dir, item)
        dst = os.path.join(dest_dir, item)
        if os.path.exists(dst):
            if os.path.isdir(dst):
                shutil.rmtree(dst)
            else:
                os.remove(dst)
        shutil.move(src, dst)
    shutil.rmtree(extracted_dir)
    print(f"Flattened {top_level} into {dest_dir}")

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
        tar_url = urls["tar"]
        tar_path = os.path.join(BASE_DIR, os.path.basename(tar_url))
        download_file(tar_url, tar_path)
        extract_tar(tar_path, BASE_DIR)
        os.remove(tar_path)

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
    if PLATFORM != "win" and not os.path.isfile(os.path.join(lib_path, "libSDL2.a")):
        print(f"ERROR: SDL2 static library not found at {lib_path}/libSDL2.a")
        sys.exit(1)

    print(f"SDL2 is ready at {BASE_DIR}")

if __name__ == "__main__":
    ensure_sdl()