from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
import shutil
import os

class CustomBuild(build_py):
    def run(self):
        src_prebuilt = os.path.join("src", "prebuilt")
        dst_prebuilt = os.path.join(self.build_lib, "wrapper", "prebuilt")
        if os.path.exists(dst_prebuilt):
            shutil.rmtree(dst_prebuilt)
        shutil.copytree(src_prebuilt, dst_prebuilt)
        super().run()

setup(
    name="pyverse",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    cmdclass={"build_py": CustomBuild},
    python_requires=">=3.13",
)