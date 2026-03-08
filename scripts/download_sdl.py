import os
import sys
import platform
import urllib.request
import zipfile
import tarfile
import shutil

SDL_VERSION = "2.32.10"
BASE_DIR = os.path.abspath("deps/SDL2")
PLATFORM = sys.platform

def get_urls():
    urls = {}
    if PLATFORM.startswith("win"):
        urls["dev"] = f"https://www.libsdl.org/release/SDL2-devel-{SDL_VERSION}-VC.zip"
        urls["dll"] = f"https://www.libsdl.org/release/SDL2-{SDL_VERSION}-win32-x64.zip"
    elif PLATFORM == "darwin":
        urls["tar"] = f"https://www.libsdl.org/release/SDL2-{SDL_VERSION}.tar.gz"
    elif PLATFORM.startswith("linux"):
        urls["tar"] = f"https://www.libsdl.org/release/SDL2-{SDL_VERSION}.tar.gz"
    else:
        raise RuntimeError(f"Unsupported platform: {PLATFORM}")
    return urls

def download_file(url, dest_path):
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
    if os.path.isfile(include_path):
        print(f"SDL2 headers already exist at {include_path}")
        return

    os.makedirs(BASE_DIR, exist_ok=True)
    urls = get_urls()

    if PLATFORM.startswith("win"):
        dev_zip = os.path.join(BASE_DIR, os.path.basename(urls["dev"]))
        download_file(urls["dev"], dev_zip)
        extract_zip(dev_zip, BASE_DIR)
        os.remove(dev_zip)

        dll_zip = os.path.join(BASE_DIR, os.path.basename(urls["dll"]))
        download_file(urls["dll"], dll_zip)
        extract_zip(dll_zip, os.path.join(BASE_DIR, "bin"))
        os.remove(dll_zip)

        extracted_dirs = [
            d for d in os.listdir(BASE_DIR)
            if d.startswith("SDL2") and os.path.isdir(os.path.join(BASE_DIR, d))
        ]
        if not extracted_dirs:
            raise RuntimeError("SDL source folder not found after extraction")

        hdr_src = os.path.join(BASE_DIR, extracted_dirs[0], "include")
        hdr_dst = os.path.join(BASE_DIR, "include")
        if os.path.exists(hdr_dst):
            shutil.rmtree(hdr_dst)
        shutil.move(hdr_src, hdr_dst)

        shutil.rmtree(os.path.join(BASE_DIR, extracted_dirs[0]))

        dll_src = os.path.join(BASE_DIR, "bin", "SDL2.dll")
        dll_dst = os.path.join("src", "pyverse", "SDL2.dll")
        os.makedirs(os.path.dirname(dll_dst), exist_ok=True)
        if os.path.isfile(dll_src):
            shutil.copy2(dll_src, dll_dst)
            print(f"Copied SDL2.dll to {dll_dst}")
        else:
            print(f"Warning: SDL2.dll not found at {dll_src}, wheel may fail!")

    else:
        tar_path = os.path.join(BASE_DIR, os.path.basename(urls["tar"]))
        download_file(urls["tar"], tar_path)
        extract_tar(tar_path, BASE_DIR)
        os.remove(tar_path)

        extracted_dirs = [
            d for d in os.listdir(BASE_DIR)
            if d.startswith("SDL2") and os.path.isdir(os.path.join(BASE_DIR, d))
        ]
        if not extracted_dirs:
            raise RuntimeError("SDL source folder not found after extraction")

        hdr_src = os.path.join(BASE_DIR, extracted_dirs[0], "include")
        hdr_dst = os.path.join(BASE_DIR, "include")
        if os.path.exists(hdr_dst):
            shutil.rmtree(hdr_dst)
        shutil.move(hdr_src, hdr_dst)

        shutil.rmtree(os.path.join(BASE_DIR, extracted_dirs[0]))

        print("SDL2 headers prepared. You should have lib/ manually placed if needed.")

    if not os.path.isfile(include_path):
        print(f"ERROR: SDL2 headers not found at {include_path}")
        sys.exit(1)

    print(f"SDL2 is ready at {BASE_DIR}")

if __name__ == "__main__":
    ensure_sdl()