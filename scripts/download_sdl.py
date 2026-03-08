import subprocess
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
ARCH = platform.architecture()[0]

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

def extract_zip(zip_path, dest_dir, flatten_top=True):
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        members = zip_ref.namelist()
        top_level = members[0].split("/")[0] if flatten_top else ""
        for member in members:
            path_parts = member.split("/", 1)
            if len(path_parts) > 1:
                target_path = os.path.join(dest_dir, path_parts[1])
            else:
                target_path = os.path.join(dest_dir, member)
            if member.endswith("/"):
                os.makedirs(target_path, exist_ok=True)
            else:
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                with open(target_path, "wb") as f:
                    f.write(zip_ref.read(member))
    print(f"Extracted {zip_path} to {dest_dir}")

def extract_tar(tar_path, dest_dir):
    with tarfile.open(tar_path, "r:gz") as tar_ref:
        tar_ref.extractall(dest_dir)
    print(f"Extracted {tar_path} to {dest_dir}")

def ensure_sdl():
    include_path = os.path.join(BASE_DIR, "include", "SDL.h")
    if os.path.isfile(include_path):
        print(f"SDL2 headers already exist at {include_path}")
    else:
        os.makedirs(BASE_DIR, exist_ok=True)
        urls = get_urls()

        if PLATFORM.startswith("win"):
            dev_url = urls["dev"]
            dev_zip = os.path.join(BASE_DIR, os.path.basename(dev_url))
            download_file(dev_url, dev_zip)
            extract_zip(dev_zip, BASE_DIR)
            os.remove(dev_zip)

            dll_url = urls["dll"]
            dll_zip = os.path.join(BASE_DIR, os.path.basename(dll_url))
            download_file(dll_url, dll_zip)
            extract_zip(dll_zip, os.path.join(BASE_DIR, "bin"))
            os.remove(dll_zip)

            extracted_dirs = [
                os.path.join(BASE_DIR, d)
                for d in os.listdir(BASE_DIR)
                if d.startswith("SDL2-") and os.path.isdir(os.path.join(BASE_DIR, d))
            ]
            
            if not extracted_dirs:
                raise RuntimeError("SDL source folder not found after extraction")
            
            source_dir = extracted_dirs[0]
            hdr_src = os.path.join(source_dir, "include")
            hdr_dst = os.path.join(BASE_DIR, "include")
            
            if not os.path.isdir(hdr_src):
                raise RuntimeError("SDL include directory missing in source archive")
            
            if os.path.exists(hdr_dst):
                shutil.rmtree(hdr_dst)
            
            shutil.move(hdr_src, hdr_dst)
            shutil.rmtree(source_dir)
            
            print("SDL2 headers prepared for macOS/Linux.")

            dll_src = os.path.join(BASE_DIR, "bin", "SDL2.dll")
            dll_dst = os.path.join("src", "pyverse", "SDL2.dll")
            os.makedirs(os.path.dirname(dll_dst), exist_ok=True)
            if os.path.isfile(dll_src):
                shutil.copy2(dll_src, dll_dst)
                print(f"Copied SDL2.dll to {dll_dst}")
            else:
                print(f"Warning: SDL2.dll not found at {dll_src} — Windows wheel may fail!")

        else:
            tar_url = urls["tar"]
            tar_path = os.path.join(BASE_DIR, os.path.basename(tar_url))

            download_file(tar_url, tar_path)
            extract_tar(tar_path, BASE_DIR)
            os.remove(tar_path)

            extracted = [
                f for f in os.listdir(BASE_DIR)
                if f.startswith("SDL2-") and os.path.isdir(os.path.join(BASE_DIR, f))
            ]

            for folder in extracted:
                folder_path = os.path.join(BASE_DIR, folder)

                hdr_src = os.path.join(folder_path, "include")
                hdr_dst = os.path.join(BASE_DIR, "include")

                if os.path.isdir(hdr_src):
                    shutil.move(hdr_src, hdr_dst)

                shutil.rmtree(folder_path)

            print("Building SDL2...")

            source_dir = os.path.join(BASE_DIR, f"SDL2-{SDL_VERSION}")
            build_dir = os.path.join(BASE_DIR, "build")

            os.makedirs(build_dir, exist_ok=True)

            subprocess.check_call([
                "cmake",
                source_dir,
                "-DSDL_SHARED=OFF",
                "-DSDL_STATIC=ON",
                "-DCMAKE_OSX_ARCHITECTURES=x86_64;arm64"
            ], cwd=build_dir)

            subprocess.check_call([
                "cmake",
                "--build",
                ".",
                "--config",
                "Release"
            ], cwd=build_dir)

            print("SDL2 built successfully.")

    if not os.path.isfile(include_path):
        print(f"ERROR: SDL2 headers not found at {include_path}")
        sys.exit(1)
    print(f"SDL2 is ready at {BASE_DIR}")

if __name__ == "__main__":
    ensure_sdl()