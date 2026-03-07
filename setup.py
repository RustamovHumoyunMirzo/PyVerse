from setuptools import setup, Extension, find_packages

ext_modules = [
    Extension(
        "pyverse.pyverse",
        sources=["src/pyverse.cpp"],
        extra_compile_args=["/O2"],
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