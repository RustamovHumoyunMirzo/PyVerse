from setuptools import setup
from setuptools import Extension
import sysconfig

ext = Extension(
    "pyverse",
    sources=["src/pyverse.cpp"],
    include_dirs=[sysconfig.get_path("include")],
)

setup(
    name="PyVerse",
    version="0.1.0",
    ext_modules=[ext],
)