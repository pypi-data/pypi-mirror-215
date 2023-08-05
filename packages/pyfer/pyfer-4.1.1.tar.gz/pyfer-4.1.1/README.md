![pyfer_cover](aux/rm_cover.jpg)

-----------------

# Pyfer ~ Encrypt and Decrypt Strings

[![PyPI - Version](https://img.shields.io/pypi/v/pyfer.svg)](https://pypi.org/project/pyfer/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyfer.svg)](https://pypi.org/project/pyfer/)
[![License: MIT](https://img.shields.io/badge/license-MIT-C06524)](https://github.com/celerygemini/pyfer/blob/main/LICENSE)

## 💡 What is it?

Pyfer is a simple encryption and decryption tool built in Python. 

### Features

With this little library you can do the following:

 - Encrypt and decrypt strings
 - Use one of three available encryption modes, each using a different ciphertext alphabet
 - Generate random digit keys

## 🛠️ Setup 

Install it from **PyPI** by running `pip install pyfer`.

### Dependencies 

The only dependency is [NumPy](https://numpy.org)

## 🚀 Execution

### Quickstart

```
import pyfer

k = pyfer.generate_key(45)
m = "Hello_world!"
pm = pyfer.Machine(k)

pm.scramble(m)

```

For more information, have a look at the demo [here](https://github.com/elbydata/pyfer/blob/master/demos/demo.ipynb)!

## 📝 Documentation

Documentation is currently available in the form of docstrings.
 
## ⚖️ License

The project is licensed under the MIT license.