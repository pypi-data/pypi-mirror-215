# imgo

## Process, Augment, and Balance Image Data

[![PyPI - Version](https://img.shields.io/pypi/v/imgo.svg)](https://pypi.org/project/imgo/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/imgo.svg)](https://pypi.org/project/imgo/)
[![License: MIT](https://img.shields.io/badge/license-MIT-C06524)](https://github.com/celerygemini/imgo/blob/main/LICENSE)

## 💡 What is it?

This library is designed to facilitate the preprocessing phase of image classification projects in order to get into the fun part: training the models!

### Features:

Imgo is composed of two modules: **uptools** and **augtools**.

**Uptools** helps to streamline various image data preprocessing tasks, such as:

 - Reading images from a local disk
 - Rescaling images
 - Normalizing and standardizing pixel values
 - Converting image datasets into numpy-arrays
 - One-hot-encoding label data
 - Splitting image datasets into training, validation, and testing subsets
 - Merging data subsets into a single dataset
 - Saving numpy-arrays as images in class subdirectories
 
![imgo_up_demo](aux/imgo_up_demo.jpg)
 
**Augtools** allows the user to quickly and efficiently apply augmentation to image data. With Augtools, users can perform the following augmentation tasks using very few lines of code:

 - Apply a powerful collection of transformation and corruption functions
 - Augment images saved on a local disk
 - Save augmented images in class subdirectories
 - Augment entire image datasets
 - Augment training data in place in preparation for machine learning projects
 - Rebalance class sizes by generating new training images

![imgo_aug_demo](aux/imgo_aug_demo.jpg)

## 🛠️ Setup 

Install it from **PyPI** by running `pip install imgo`.

### Dependencies 

The code was written with **Python 3.6**, and it is recommended to run it in a virtual environment. 
All the required libraries are listed in the `requirements.txt` file in this repo.

## 🚀 Execution

Once the package has been installed, it is simply a case of experimenting with the various classes and functions. For a quickstart, please see the [demo](https://github.com/celerygemini/imgo/tree/master/demos).

## 📝 Documentation

Documentation is currently available in the form of docstrings.

## ⚖️ License

The project is licensed under the MIT license.

### Acknowledgements

Some of the **augtools** library is built as a wrapper around **Imgaug**, a powerful image augmentation library. For more information, please see https://imgaug.readthedocs.io/en/latest/.