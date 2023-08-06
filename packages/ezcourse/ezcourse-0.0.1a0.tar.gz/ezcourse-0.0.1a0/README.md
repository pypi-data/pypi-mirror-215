# LISPI Documentation

## Introduction

`lispi` (Learning Interactive Slides and PIthon) is a Python package that provides a convenient way to convert Jupyter notebooks into interactive slides. It allows users to create engaging presentations with interactive elements directly from the slides.

## Installation

### Install from GitHub files
To install `lispi` package, you can clone the repository from GitHub and modify it to your liking and install on your system. Open your terminal and run the following command:

```
git clone https://github.com/B7M/lispi.git
```
Navigate to the directory containing the repository and follow these steps:

Make the build file:

```
python -m build
```
Once the build file is created successfully, you will see a folder named `dist` in the directory which contains `.whl` and '.tar.gz'. The name of the file will be the {package name}-{version number}-{py3-none-any.whl}. At this point run `pip install dist/{the .whl file}` command to install the package, here is an example of installing the package with `version 0.0.9`:

```
pip install dist/lispi-0.0.9-py3-none-any.whl
```


### Install from PyPI
To install `lispi` package, you can use pip, the Python package installer. Open your terminal and run the following command:

```
pip install lispi
```
## Configuration

Lispi provides several configuration options to customize the output slides. You can pass these options as arguments when creating an instance of the `lispi` class. Here are the available configuration options:

- `audio`: Specify if you wish the output without audio (default: "unmute").
- `output_file`: Specify the output file path for the generated slides (default: "output.html").

Example:

```python
generator = lispi(
    audio="unmute",
    output_file="path/to/output/slides.html"
)
```

## Usage
### Command Line Interface
To use lispi, in your terminal follow these steps:
After installing the package, you can use the `lispi` command to convert your Jupyter notebook into interactive slides. In your terminal, navigate to the folder containing the notebooks and run the following command:

```lispi```

Upon running the command, the package will prompt you with help text to show you how you can use it. Enter the name of the file press enter. The package will convert the Jupyter notebook into interactive slides and save the output HTML file in the output folder in the same directory as html file and audio file folder. If you wish to convert the notebook named `original_example.ipynb`, you will enter `original_example` and press enter. If you wish to convert the notebook without audio, you can enter `lispi -m original_example` and press enter.

### Python
If you want to use lispi in your Python code, you can import the package and use it as a library. To use lispi, in python follow these steps:

1. Import the `Gen` class from the package:

   ```python
   import lispi
   ```
   or 

   ```python
    from lispi import *
   ```

2. Create an instance of the `Interactive Slides Generator` class:

   ```python
   generator = lispi.Gen
   ```

3. Specify the Jupyter notebook file you want to convert:

   ```python
   notebook_file = "path/to/your/notebook.ipynb"
   ```

4. Generate the interactive slides:

   ```python
   generator(notebook_file)
   ```

5. The package will convert the Jupyter notebook into interactive slides and save the output HTML file in the output folder in the same directory as html file and audio file folder.



## Examples

Here is an example that comes with the package. To run the example, in your terminal or python code provide 'original_example' as the file name.

(with audio)
```bash 
lispi original_example
```
or

```bash
lispi -i original_example
```

(without audio)
```bash
lispi -m original_example
```
And in python code:

```python
import lispi

# Create an instance of the lispi class
generator = lispi.Gen

# Specify the example notebook file
notebook_file = "original_example"

# Generate the interactive slides
generator(notebook_file)
```

## Conclusion

Lispi package provides a convenient way to convert Jupyter notebooks into interactive slides. It allows users to create engaging presentations with interactive elements easily. By following the installation and usage instructions outlined in this documentation, you can leverage this package to generate interactive slides from your Jupyter notebooks effortlessly.
