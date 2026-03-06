import sys
import os
import importlib.util

def _load_pyverse():
    base = os.path.join(os.path.dirname(__file__), "prebuilt")
    plat = sys.platform
    pyver = f"{sys.version_info.major}{sys.version_info.minor}"

    if plat.startswith("win"):
        lib_path = os.path.join(base, f"pyverse.cp{pyver}-win_amd64.pyd")
    elif plat.startswith("linux"):
        lib_path = os.path.join(base, f"pyverse.cpython-{pyver}-x86_64-linux-gnu.so")
    elif plat.startswith("darwin"):
        lib_path = os.path.join(base, f"pyverse.cpython-{pyver}-darwin.so")
    else:
        raise RuntimeError(f"Unsupported platform: {plat}")

    spec = importlib.util.spec_from_file_location("pyverse", lib_path)
    pyverse = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pyverse)
    return pyverse

pyverse = _load_pyverse()