from setuptools import setup, find_packages

setup(
    name="alx-utils",
    version="0.6",
    description="A collection of utility tools for ALX",
    author="BIO",
    url="https://github.com/amasin76/alx-utils",
    packages=find_packages(include=["src", "src.*", "tools", "tools.*"]),
    package_data={
        "tools.checker": ["test.bash"],
    },
    install_requires=[
        "beautifulsoup4",
    ],
    entry_points={
        "console_scripts": [
            "alx-utils=src.alx_utils:main",
        ],
    },
)
