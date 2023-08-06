import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="imgo",
    version="2.5.9",
    author="celerygemini",
    description="Image Dataset Management Toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/celerygemini/imgo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
