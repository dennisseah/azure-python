Guidelines for Python Development

ISE Commercial Studio Microsoft Corporation

From Oxford Languages

> guide·line /ˈɡīdˌlīn/ noun a general rule, principle, or piece of advice.

From Cambridge Dictionary

> A piece of information that suggests how something should be done: "The
> article gives guidelines on how to invest your money safely."

These definitions are important. This document provides guidelines—a set of
principles that guide our coding and engineering practices. They are not rigid
rules.

> "Guidelines account for judgement, rules don't"

We've gained valuable insights from using Python in past engagements, and we
hope to improve our Python experience with these guidelines. These guidelines
serve as an addendum to ISE guidelines for software development. This is
intended to be a living document that we update as needed.

| Revision | Date      | Author      | Description                       |
| -------- | --------- | ----------- | --------------------------------- |
| 1.0      | 2025Feb23 | Dennis Seah | Initial version                   |
| 1.1      | 2025Mar07 | Dennis Seah | Improve the step to setup project |
| 1.2      | 2025Mar20 | Dennis Seah | added information on pip-audit    |
| 1.3      | 2025Mar27 | Dennis Seah | added information on uv           |
| 1.4      | 2025Dec14 | Dennis Seah | added azure storage service       |
| 1.4      | 2025Dec14 | Dennis Seah | added openai service              |
| 1.5      | 2025Dec14 | Dennis Seah | added adversarial simulation svc  |
| 1.5      | 2025Dec14 | Dennis Seah | addded mlflow service             |

---

<h1>Table of Contents</h1>

- [1. Motivation](#1-motivation)
- [2. Guidelines](#2-guidelines)
  - [2.1 Python Versions](#21-python-versions)
    - [2.1.1 Python Version for Our Project](#211-python-version-for-our-project)
  - [2.2 Visual Studio Code](#22-visual-studio-code)
  - [2.3 Setup Python Project](#23-setup-python-project)
    - [2.3.1 Initialize a Python Project](#231-initialize-a-python-project)
    - [2.3.2 Add or Remove Python Packages](#232-add-or-remove-python-packages)
  - [2.4 Static Type Checking](#24-static-type-checking)
    - [2.4.1 Use Type Hints](#241-use-type-hints)
    - [2.4.2 Use Static Type Checker](#242-use-static-type-checker)
  - [2.5 Runtime Type Checking](#25-runtime-type-checking)
  - [2.6 Code Formatting and Prettifying](#26-code-formatting-and-prettifying)
  - [2.7 Dependency Injection](#27-dependency-injection)
  - [2.8 Unit Testing](#28-unit-testing)
  - [2.9 Package and Dependency Scanning](#29-package-and-dependency-scanning)
- [Appendix A: Ruff vs Black](#appendix-a-ruff-vs-black)
  - [Speed](#speed)
  - [Compatibility](#compatibility)
  - [Configurability](#configurability)
  - [Features](#features)

---

# 1. Motivation

Python is a widely popular programming language used for various applications,
including web development, data analysis, and data science. In many companies,
Python is the primary language for machine learning and data science. It's
attractive due to its flexibility and abundance of open-source libraries.
However, there are several considerations to keep in mind:

1. Dynamic Typing
   - While dynamic typing allows for flexibility, it can also lead to
     type-related errors.
2. Performance
   - Python is generally slower than compiled languages. For large datasets,
     consider using optimized libraries like NumPy or Pandas to improve
     performance. When possible, push computation closer to the data store to
     minimize data transfer overhead.
3. Python versions
   - Azure Python libraries do not always support the latest Python version.
     Hence it is important to choose the right version for development. We use
     Python virtual environment to help us manage different Python versions.
4. Package and Dependency Management
   - Modern tooling provides better alternatives to manually maintaining
     requirements.txt files and relying solely on pip install.
5. Unit Testing, Code Coverage, and Mock Testing
   - There are many techniques for mocking functions and classes. We aim to
     establish consistent testing practices so that all team members understand
     what to test and how to test it.

Additionally, we aim to structure our codebase in a consistent manner to
facilitate collaboration among software engineers in our studio. This
consistency simplifies code reviews and project handoffs because all Python
developers in our studio follow the same practices for setting up development
environments, contributing code, and developing unit tests.

# 2. Guidelines

Our main goal is to leverage Python's flexibility and versatility while
maintaining code quality. Python's clean syntax and emphasis on readability make
code easier to understand and maintain. At the same time, we establish
structures as guardrails to ensure we develop and ship maintainable,
high-performance software solutions.

## 2.1 Python Versions

Python releases a new version annually and supports each version for 5 years.
This means that every year, a Python version is deprecated. Over time,
developers working on multiple projects will need to manage multiple Python
versions on their machines.

> **Why Not Use System Python?** The Python installation that comes with your
> operating system (accessible via `python --version` on Mac or Linux) belongs
> to the OS. This is often not the version needed for development. Moreover,
> modifying the system Python version can cause issues with OS functionality.

To manage multiple Python versions, we recommend using `uv` to install and
switch between Python versions as needed.

To install a specific Python version:

```bash
uv python install 3.13
```

To install a specific patch version:

```bash
uv python install 3.13.2
```

for more commands see
[uv guide](https://docs.astral.sh/uv/concepts/python-versions/)

### 2.1.1 Python Version for Our Project

In the project's root folder, add a `.python-version` file. For example,
specifying `3.13` in this file indicates to the `uv` tool that it should use
Python version `3.13.x`.

---

## 2.2 Visual Studio Code

We have excellent experience using
[Visual Studio Code](https://code.visualstudio.com/docs/languages/python) for
Python development. It's a lightweight IDE with rich Python extension support.

> **Customer's Choice:** We adapt to what our customers are comfortable with.
> Some customers prefer PyCharm or other IDEs. We suggest Visual Studio Code
> when appropriate.

Here are the recommended extensions for Python development in Visual Studio
Code:

- ms-python.python
- charliermarsh.ruff
- editorconfig.editorconfig
- esbenp.prettier-vscode

---

## 2.3 Setup Python Project

We recommend [uv](https://docs.astral.sh/uv/) for Python package management. For
more information, refer to [this document](./docs/uv_package_management.md).

`uv` (Unified Python packaging) is a fast Python package manager written in
Rust, designed to replace tools like pip, virtualenv, poetry, and pyenv.

### 2.3.1 Initialize a Python Project

```bash
cd <git-root-folder>
```

**Note:** Create a `.python-version` file with the desired Python version.

```bash
uv init
```

and we will have

```file
.
├── .python-version
├── README.md
├── main.py
└── pyproject.toml
```

Next, we run `uv sync` to install the Python version and create a virtual
environment.

```bash
uv sync
source .venv/bin/activate
```

or on Windows

```powershell
uv sync
.venv\Scripts\activate
```

and we will have (observe the .venv folder is created)

```file
.
├── .venv
│   ├── bin
│   ├── lib
│   └── pyvenv.cfg
├── .python-version
├── README.md
├── main.py
├── pyproject.toml
└── uv.lock
```

> **Where is the requirements.txt file?** This file can be generated with these
> commands:

```bash
uv export --frozen --no-dev --output-file=requirements.txt
uv export --frozen --all-groups --output-file=requirements.dev.txt
```

These exports can be automated using pre-commit git hooks.

### 2.3.2 Add or Remove Python Packages

To add or remove Python packages:

```bash
uv add <package-name>
uv remove <package-name>
```

To add a development package:

```bash
uv add --dev <package-name>
```

## 2.4 Static Type Checking

Python is dynamically typed and there are a few things that we can do to avoid
potential runtime errors due to unexpected data types.

### 2.4.1 Use Type Hints

Type hints (introduced in [PEP 484](https://peps.python.org/pep-0484/)) specify
the expected types of function parameters and return values. They are optional
and provide additional information for developers and static type checkers.

```python
def my_function(
    param1: str,
    param2: list[str]
) -> dict[str, float]:
    ...
```

Note that these hints are ignored by the Python interpreter at runtime. They
help understand expected types and allow static type checkers to identify
potential type mismatches.

### 2.4.2 Use Static Type Checker

We recommend [pyright](https://microsoft.github.io/pyright) for static type
checking.

## 2.5 Runtime Type Checking

We recommend using [pydantic](https://docs.pydantic.dev/latest/) for runtime
type checking. Code should raise `ValueError` as early as possible when type
violations occur to prevent unintended downstream errors.

## 2.6 Code Formatting and Prettifying

Python is indentation-sensitive, using indentation to determine statement
grouping. Therefore, correct indentation is crucial for code functionality and
readability.

We recommend using [ruff](https://github.com/astral-sh/ruff) for code formatting
over Black (see Appendix A for comparison).

## 2.7 Dependency Injection

We recommend using [lagom](https://lagom-di.readthedocs.io/en/latest/) for
dependency injection. We advocate for dependency injection for the following
reasons:

- Improves testability
- Increases flexibility (enables easy service replacement)
- Supports concurrent code development
- Promotes code reusability

Refer to the codebase for implementation examples. See
[hosting.py](azure_python/hosting.py) and files in the
[protocols](azure_python/protocols/), [services](azure_python/services/), and
[tests](tests/) folders.

## 2.8 Unit Testing

We aim for comprehensive test coverage. Use `pytest-cov` to identify gaps in
test coverage.

Recommended testing packages:

- `pytest` - Testing framework
- `pytest-cov` - Coverage reporting
- `pytest-mock` - Mocking support
- `pytest-asyncio` - Async testing support

Command to run all tests with coverage:

```bash
python -m pytest --cov-report term-missing --cov=<your_module_name> tests
```

## 2.9 Package and Dependency Scanning

We recommend using `pip-audit` to scan dependencies for security
vulnerabilities.

```bash
pip-audit -r requirements.txt
```

---

# Appendix A: Ruff vs Black

## Speed

Ruff is written in Rust, which makes it significantly faster than Black for
large code bases. Black is slower than Ruff.

## Compatibility

Ruff aims to be 100% compatible with Black. Black has its own unique formatting
style, which is highly opinionated and non-configurable.

## Configurability

Ruff offers limited configuration options, such as quote style, indent style,
and line endings, while still maintaining compatibility with Black. Black
intentionally offers almost no configuration options, enforcing a consistent
style across all projects.

## Features

In addition to formatting, Ruff also functions as a linter, replacing tools like
Flake8. Black solely focuses on code formatting.
