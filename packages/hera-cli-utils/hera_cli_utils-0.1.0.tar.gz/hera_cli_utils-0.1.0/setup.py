# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hera_cli_utils']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1',
 'line-profiler>=4.0.3,<5.0.0',
 'psutil>=5.9.5,<6.0.0',
 'rich>=13.4.2,<14.0.0']

entry_points = \
{'console_scripts': ['hera-cli-utils = hera_cli_utils.__main__:main']}

setup_kwargs = {
    'name': 'hera-cli-utils',
    'version': '0.1.0',
    'description': 'HERA CLI Utils',
    'long_description': "# HERA CLI Utils\n\n[![PyPI](https://img.shields.io/pypi/v/hera-cli-utils.svg)][pypi status]\n[![Status](https://img.shields.io/pypi/status/hera-cli-utils.svg)][pypi status]\n[![Python Version](https://img.shields.io/pypi/pyversions/hera-cli-utils)][pypi status]\n[![License](https://img.shields.io/pypi/l/hera-cli-utils)][license]\n\n[![Read the documentation at https://hera-cli-utils.readthedocs.io/](https://img.shields.io/readthedocs/hera-cli-utils/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Tests](https://github.com/steven-murray/hera-cli-utils/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/steven-murray/hera-cli-utils/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi status]: https://pypi.org/project/hera-cli-utils/\n[read the docs]: https://hera-cli-utils.readthedocs.io/\n[tests]: https://github.com/steven-murray/hera-cli-utils/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/steven-murray/hera-cli-utils\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\n## Features\n\n- TODO\n\n## Requirements\n\n- TODO\n\n## Installation\n\nYou can install _HERA CLI Utils_ via [pip] from [PyPI]:\n\n```console\n$ pip install hera-cli-utils\n```\n\n## Usage\n\nPlease see the [Command-line Reference] for details.\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [MIT license][license],\n_HERA CLI Utils_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n## Credits\n\nThis project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/steven-murray/hera-cli-utils/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/steven-murray/hera-cli-utils/blob/main/LICENSE\n[contributor guide]: https://github.com/steven-murray/hera-cli-utils/blob/main/CONTRIBUTING.md\n[command-line reference]: https://hera-cli-utils.readthedocs.io/en/latest/usage.html\n",
    'author': 'Steven Murray',
    'author_email': 'steven.g.murray@asu.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/steven-murray/hera-cli-utils',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
