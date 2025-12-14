# Python Package Management

Like any other programming language, Python has its own package management system. The most
common package manager for Python is `pip`, which stands for "Pip Installs Packages". It
allows you to install, upgrade, and remove Python packages from the Python Package Index
(PyPI) and other repositories. However, there are other package managers available for
Python, such as `conda`, which is part of the Anaconda distribution and is used for managing
packages and environments in data science and scientific computing.

`poetry` is another popular package manager that focuses on dependency management and
packaging in Python. It allows you to create and manage virtual environments, handle
dependencies, and publish packages to PyPI. 

Given that we have options for package management, it is important to understand the
differences between them and when to use each one. In this document, we  compare 
`pip`, `conda` `poetry` and `uv` in terms of their features.

[source](https://www.datacamp.com/tutorial/python-uv)
| Tool                       | `uv`                    | `pip`    | `conda`         | `poetry`        |
| -------------------------- | ----------------------- | -------- | --------------- | --------------- |
| Implementation             | Rust                    | Python   | Python          | Python          |
| Speed                      | 10-100x faster than pip | Baseline | Slower than pip | Faster than pip |
| Memory Usage               | Very efficient          | Higher   | High            | Moderate        |
| Dependency Resolution      | Fast, modern resolver   | Basic    | Comprehensive   | Modern resolver |
| Lock Files                 | Yes                     | No       | Yes             | Yes             |
| Package Management         | Yes                     | Yes      | Yes             | Yes             |
| Cross-platform Consistency | Yes                     | Limited  | Excellent       | Good            |

`uv` is a package manager that is designed to be fast and efficient, with a focus on modern dependency
resolution. It is implemented in Rust, which allows it to be significantly faster than `pip`, especially
for large projects with many dependencies. `uv` also has a very efficient memory usage profile, making
it a good choice for resource-constrained environments.

For python version management, `uv` just needs a .python-version file in the root of the project. It
will automatically create a virtual environment with the specified python version. This is similar
to how `pyenv` works, but `uv` does not require any additional setup or configuration. This makes it
easy to manage different python versions for different projects without having to worry about conflicts
or compatibility issues.

For example, for a new project, you can a file called `.python-version` in the root of the project
with the following content:

```bash
3.12
```

`uv init` will generate a `pyproject.toml` file flagging python version 3.12 is required for the project.
And, when we run `uv sync`, it will create a virtual environment with python 3.12 and install all the
dependencies listed in the `pyproject.toml` file. This makes it easy to manage different python versions
for different projects without having to worry about conflicts or compatibility issues.

If we want to upgrade to a new version of python, we can simply update the `.python-version` file and
run `uv sync` again. This will automatically create a new virtual environment with the specified python
version and install all the dependencies listed in the `pyproject.toml` file. This makes it easy to
manage different python versions for different projects without having to worry about conflicts or
compatibility issues.

On top of this, `uv` also install the Python version specified in the `.python-version` file if it is
not already installed. This makes it easy to manage different python versions for different projects
without having to worry about conflicts or compatibility issues.

## Conclusion
In conclusion, `uv` is a powerful and efficient package manager for Python that is designed to be fast
and easy to use. It is a good choice for projects that require modern dependency resolution and
efficient memory usage. It is also a good choice for projects that require cross-platform consistency
and easy management of different python versions. Overall, `uv` is a great choice for Python developers
who want a fast and efficient package manager.

## References
1. [uv official doc](https://docs.astral.sh/uv/)
1. [uv git repo](https://github.com/astral-sh/uv)
1. [uv install Python](https://docs.astral.sh/uv/guides/install-python/)
1. [migrate to uv](https://github.com/mkniewallner/migrate-to-uv)

