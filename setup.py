"""The setup script."""
from setuptools import find_packages, setup

with open("README.md") as readme_file:
    readme = readme_file.read()

setup(
    author_email="hi@ludeeus.dev",
    author="Joakim Sorensen",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    version="main",
    description="Python API wrapper for Uptime Robot.",
    install_requires=["aiohttp>=3.6.1,<4.0"],
    keywords=["homeassistant", "version", "update"],
    license="MIT license",
    long_description_content_type="text/markdown",
    long_description=readme,
    name="pyuptimerobot",
    packages=find_packages(include=["pyuptimerobot", "pyuptimerobot*"]),
    python_requires=">=3.13.0",
    url="https://github.com/ludeeus/pyuptimerobot",
)
