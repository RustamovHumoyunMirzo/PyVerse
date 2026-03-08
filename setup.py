from setuptools import setup, Extension, find_packages
import pybind11

ext_modules = [
    Extension(
        "pyverse.pyverse",
        sources=["src/cpp/pyverse.cpp"],
        include_dirs=[pybind11.get_include()],
        extra_compile_args=["/O2"],
        language="c++",
    )
]

setup(
    name="PyVerse",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    ext_modules=ext_modules,
)