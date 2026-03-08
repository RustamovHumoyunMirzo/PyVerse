import platform
import urllib.request
import tarfile
import zipfile
import os

VERSION = "2.32.10"
ROOT = os.path.abspath("deps")
os.makedirs(ROOT, exist_ok=True)

system = platform.system()

def download(url, path):
    print("Downloading:", url)
    urllib.request.urlretrieve(url, path)

if system == "Windows":
    url = f"https://github.com/libsdl-org/SDL/releases/download/release-{VERSION}/SDL2-devel-{VERSION}-VC.zip"
    archive = os.path.join(ROOT, "sdl.zip")
    download(url, archive)

    with zipfile.ZipFile(archive) as z:
        z.extractall(ROOT)

elif system in ("Linux", "Darwin"):
    url = f"https://github.com/libsdl-org/SDL/archive/refs/tags/release-{VERSION}.tar.gz"
    archive = os.path.join(ROOT, "sdl.tar.gz")
    download(url, archive)

    with tarfile.open(archive) as t:
        t.extractall(ROOT)