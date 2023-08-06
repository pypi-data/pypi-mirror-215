# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gymnasium_quadruped', 'gymnasium_quadruped.envs']

package_data = \
{'': ['*'],
 'gymnasium_quadruped': ['assets/unitree_a1/*', 'assets/unitree_a1/assets/*']}

install_requires = \
['gymnasium[mujoco]>=0.28.1,<0.29.0', 'numpy>=1.24.3,<2.0.0']

setup_kwargs = {
    'name': 'gymnasium-quadruped',
    'version': '0.0.1',
    'description': 'Gymnasium environment for training quadruped legged robots',
    'long_description': '# gymnasium-quadruped\n\n[![Release](https://img.shields.io/github/v/release/dtch1997/gymnasium-quadruped)](https://img.shields.io/github/v/release/dtch1997/gymnasium-quadruped)\n[![Build status](https://img.shields.io/github/actions/workflow/status/dtch1997/gymnasium-quadruped/main.yml?branch=main)](https://github.com/dtch1997/gymnasium-quadruped/actions/workflows/main.yml?query=branch%3Amain)\n[![codecov](https://codecov.io/gh/dtch1997/gymnasium-quadruped/branch/main/graph/badge.svg)](https://codecov.io/gh/dtch1997/gymnasium-quadruped)\n[![Commit activity](https://img.shields.io/github/commit-activity/m/dtch1997/gymnasium-quadruped)](https://img.shields.io/github/commit-activity/m/dtch1997/gymnasium-quadruped)\n[![License](https://img.shields.io/github/license/dtch1997/gymnasium-quadruped)](https://img.shields.io/github/license/dtch1997/gymnasium-quadruped)\n\nGymnasium environment for training quadruped legged robots\n\n- **Github repository**: <https://github.com/dtch1997/gymnasium-quadruped/>\n- **Documentation** <https://dtch1997.github.io/gymnasium-quadruped/>\n\n## Getting started\n\nInstall the environment and the pre-commit hooks with \n\n```bash\nmake install\n```\n\n## Learning\n\nThis repository contains a simple PPO implementation in `learning/ppo.py`, adapted from [CleanRL](https://github.com/vwxyzjn/cleanrl). This serves to benchmark the environment. \n\nSee [learning/README.md](learning/README.md) for details. \n\n## Contributing \n\nWe welcome contributions; please refer to the [guidelines](CONTRIBUTING.rst)\n\n---\n\nRepository initiated with [fpgmaas/cookiecutter-poetry](https://github.com/fpgmaas/cookiecutter-poetry).',
    'author': 'Daniel CH Tan',
    'author_email': 'fdtch1997@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/dtch1997/gymnasium-quadruped',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
