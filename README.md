<img src="images/PyVerseIcon.png" alt="PyVerse icon" width="200" height="200">

# PyVerse

[![GitHub Actions Build Status](https://github.com/RustamovHumoyunMirzo/PyVerse/actions/workflows/build-wheels.yaml/badge.svg)](https://github.com/RustamovHumoyunMirzo/PyVerse/actions/workflows/build-wheels.yaml)

A powerful Python framework for building modern desktop and mobile applications using web technologies. It allows developers to create rich user interfaces with HTML, CSS, and JavaScript while keeping the core logic in Python.

## Requirements

- Python 3.8 or higher
- [CMake](https://cmake.org/) (for building C++ extensions)
- [pip](https://pip.pypa.io/) and [virtualenv](https://virtualenv.pypa.io/)

## Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/RustamovHumoyunMirzo/PyVerse.git
    cd PyVerse
    ```

2. **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate   # Linux/macOS
    venv\Scripts\activate      # Windows
    ```

3. **Install dependencies:**

    ```bash
    pip install --upgrade pip setuptools wheel
    pip install -e .
    ```
    The `-e .` option installs the package in editable mode for development.

## Build Wheels

You can build cross-platform wheels using [cibuildwheel](https://cibuildwheel.readthedocs.io/):

```bash
cibuildwheel --output-dir wheelhouse --archs AMD64
```

## Documentation

Full documentation is available in the [docs](docs) folder.