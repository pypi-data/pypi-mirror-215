from setuptools import setup, find_packages
import os


def _version():
    _globals, _locals = {}, {}

    with open(os.path.join("wrang_utils", "version.py")) as version_file:
        exec(version_file.read(), _globals, _locals)

    return _locals["__version__"]


def get_requirements():
    with open("requirements.txt") as f:
        return f.read().splitlines()


setup(
    name="wrang_utils",
    version=_version(),
    author="Conrad Moss",
    author_email="cmoss@wrangledinsights.com",
    description="Wrangled Insights utilities",
    packages=find_packages(exclude=("tests")),
    install_requires=get_requirements(),
    data_files=[("", ["requirements.txt"])],
    extras_require={
        "dev": [
            "pytest",
            "mypy",
            "black",
            "pylint",
            "pytest-cov",
        ]
    },
)
