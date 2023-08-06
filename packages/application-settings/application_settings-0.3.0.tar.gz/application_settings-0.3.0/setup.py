# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['application_settings']

package_data = \
{'': ['*']}

install_requires = \
['pathvalidate>=2.5,<4.0', 'pydantic>=1.10,<2.0', 'tomli-w>=1.0,<2.0']

extras_require = \
{':python_version < "3.11"': ['tomli>=2.0,<3.0',
                              'typing-extensions>=4.5.0,<5.0.0']}

setup_kwargs = {
    'name': 'application-settings',
    'version': '0.3.0',
    'description': 'For providing a python application with configuration and/or settings',
    'long_description': '# application_settings - version 0.3.0\n\n[![pypi](https://img.shields.io/pypi/v/application-settings.svg)](https://pypi.python.org/pypi/application-settings)\n[![versions](https://img.shields.io/pypi/pyversions/application-settings.svg)](https://github.com/StockwatchDev/application_settings)\n[![Build Status](https://github.com/StockwatchDev/application_settings/actions/workflows/merge_checks.yml/badge.svg?branch=develop)](https://github.com/StockwatchDev/application_settings/actions)\n[![codecov](https://codecov.io/gh/StockwatchDev/application_settings/branch/develop/graph/badge.svg)](https://app.codecov.io/gh/StockwatchDev/application_settings)\n[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)\n[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\n"You write the dataclasses to define parameters for configuration and settings, \napplication\\_settings takes care of the logic."\n\n## What and why\n\nApplication\\_settings is a package for providing a python application or library with\nparameters for configuration and settings. It uses [toml](https://toml.io/en/) or \n[json](https://www.json.org/) files that are parsed\ninto dataclasses. This brings some benefits:\n\n- Minimal work for the developer of the application / library\n- Parameters are typed, which allows for improved static code analyses.\n- IDEs will provide helpful hints and completion when using the parameters.\n- More control over what happens when a file contains mistakes\n  (by leveraging the power of [pydantic](https://docs.pydantic.dev/)).\n- Possibility to specify defaults when no file is found or entries are missing.\n- Configuration parameters are read-only (i.e., changed by editing the config file); we\n  recommend (and support) the use of `toml` for this, which is a human-oriented,\n  flexible, standardardized and not overly complex format.\n- Settings parameters are read-write (i.e., mostly changed via the UI of the\n  application); we recommend (and support) use `json` for this, an established\n  standardized machine-oriented format.\n\nParsing is done once before or during first access and the resulting set of parameters is\nstored as a singleton.\n\nInterested? Then have a look at our\n[quick start](https://stockwatchdev.github.io/application_settings/0.3.0/docs/Quick_start/).\n\n[//]: # (Change version in header and link to published quick start)\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'Stockwatchdevs',
    'author_email': 'stockwatchdevs@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/StockwatchDev/application_settings',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
