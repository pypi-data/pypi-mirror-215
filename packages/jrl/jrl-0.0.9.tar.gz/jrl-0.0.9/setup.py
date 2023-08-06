import os
import pathlib

from setuptools import setup


def package_files(directory: str, ignore_ext: list = []) -> list:
    """Returns the filepath for all files in a directory. Borrowed from https://stackoverflow.com/a/36693250"""
    paths = []
    ignore_ext = [ext.lower() for ext in ignore_ext]
    for path, directories, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(path, filename)
            if pathlib.Path(filepath).suffix.lower().strip(".") in ignore_ext:
                continue
            paths.append(filepath)
    return paths


urdf_files = package_files("jrl/urdfs/")
for file in urdf_files:
    assert os.path.isfile(file), f"Error: parsed filepath '{file}' does not exist"

urdf_files = [
    fname.replace("jrl/", "") for fname in urdf_files
]  # filenames are relative to the root directory, but we want them relative to the root/jrl directory
assert len(urdf_files) > 0, "No URDF files found"

for file in urdf_files:
    reconstructed = "jrl/" + file
    assert os.path.isfile(reconstructed), f"Error: reconstructed filepath '{reconstructed}' does not exist"

setup(
    name="jrl",
    version="0.0.9",
    author="Jeremy Morgan",
    author_email="jsmorgan6@gmail.com",
    scripts=[],
    url="https://github.com/jstmn/jrl",
    license="LICENSE.txt",
    description="Jeremy's Robotics Library",
    py_modules=[],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    # TODO: Specify version numbers. also move to pyproject.toml
    install_requires=["klampt", "numpy", "torch==2.0.1", "more_itertools", "roma", "tqdm"],
    extras_require={  # pip install -e ".[dev]"
        "dev": [
            "black==22.12.0",
            "pylint==2.15.9",
            "PyQt5==5.15.7",
            "kinpy==0.2.0",
            "pandas==1.5.3",
            "matplotlib==3.6.2",
            "tabulate==0.9.0",
            "jupyter==1.0.0",
            "torchviz==0.0.2",
            "meshcat==0.3.2",
        ]
    },
    packages=["jrl"],
    package_data={"jrl": urdf_files},
    # setup.py dist does ommites non-py files when this command is included. See
    # https://stackoverflow.com/a/33167220/5191069. (... Wat?! ...)
    # include_package_data=True,
)
