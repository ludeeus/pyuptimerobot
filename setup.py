import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="pyuptimerobot",
    version="0.0.4",
    author="Joakim Sorensen",
    author_email="joasoe@gmail.com",
    description="A python module to monitor Uptime Robot monitors.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ludeeus/pyuptimerobot",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)