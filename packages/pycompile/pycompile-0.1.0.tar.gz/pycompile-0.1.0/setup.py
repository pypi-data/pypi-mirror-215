# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src', 'src.examples']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'cython>=0.29.33,<0.30.0',
 'nuitka>=1.4.8,<2.0.0',
 'pytest-benchmark>=4.0.0,<5.0.0',
 'tqdm>=4.64.1,<5.0.0']

entry_points = \
{'console_scripts': ['pycompile = src.cli:main']}

setup_kwargs = {
    'name': 'pycompile',
    'version': '0.1.0',
    'description': 'A CLI tool for compiling python',
    'long_description': '# pycompile\n\n```python\n"""                                        _ _\n    _ __  _   _  ___ ___  _ __ ___  _ __ (_) | ___\n   | \'_ \\| | | |/ __/ _ \\| \'_ ` _ \\| \'_ \\| | |/ _ \\\n   | |_) | |_| | (_| (_) | | | | | | |_) | | |  __/\n   | .__/ \\__, |\\___\\___/|_| |_| |_| .__/|_|_|\\___|\n   |_|    |___/                    |_|\n   \n"""\n```\nA CLI tool for compiling python source code using [Cython](https://cython.org/)  or\n[Nuitka](https://nuitka.net/).\n\n## Table of contents\n1. [Local-development](#local-development)\n2. [Usage](#usage)\n\n### Local-development\nFor local development run the following command\n```bash\nmake setup-local-dev\n```\nAll available `make` commands\n```bash\nmake help\n```\n\n## Usage\n\n```bash\npycompile -i your_python_files --clean-source --engine nuitka \n```\n\nBy default, the [Cython](https://cython.org/) is being used as the default\ncompiler. \n\n\n| Syntax                | Description                                                   |\n|-----------------------|---------------------------------------------------------------|\n| `--input-path PATH`   | by default it will exclude any `test` and `__init__.py` files |\n| `--clean-source`      | Deletes the sources files.                                    |\n| `--keep-builds`       | Keeps the temp build files.                                   |\n| `--clean-executables` | Deletes the shared objects (`.so`) files.                     |\n| `--engine`            | Can be `cython` or `nuitka`.                                  |\n| `-exclude-glob-paths` | Glob file patterns for excluding specific files.              |\n| `--verbose`           | Increase log messages.                                        |\n\n### Compiling the examples\nFor compiling the `examples` use the following command:\n```bash\npycompile -i examples\n```\nwhich by default, deletes any temp build files and keeps the source files.\n\n[![asciicast](https://asciinema.org/a/QK5h8zR0oW2CGvfJtrmWZ3es0.svg)](https://asciinema.org/a/QK5h8zR0oW2CGvfJtrmWZ3es0)\n\n',
    'author': 'iplitharas',
    'author_email': 'johnplitharas@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>3.8',
}


setup(**setup_kwargs)
