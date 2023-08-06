import setuptools

# with open("./pydraulics/README.md", "r", encoding = "utf-8") as fh:
#     long_description = fh.read()

setuptools.setup(
    name = "pydraulics",
    version = "0.0.2",
    author = "Juan David Guerrero",
    author_email = "juanguerrero09mc@gmail.com",
    description = "A simple package for open and pipe flow in hydraulics created at IDOM.",
    # long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/JuanGuerrero09/pydraulics",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "pydraulics"},
    packages = setuptools.find_packages(where="pydraulics"),
    python_requires = ">=3.6",
    zip_safe = False
)