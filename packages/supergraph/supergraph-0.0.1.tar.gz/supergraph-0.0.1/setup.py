# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['supergraph']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=2.8.8,<3.0.0', 'numpy>=1.24.3,<2.0.0', 'tqdm>=4.65.0,<5.0.0']

setup_kwargs = {
    'name': 'supergraph',
    'version': '0.0.1',
    'description': 'Supergraph compiler.',
    'long_description': None,
    'author': 'Bas van der Heijden',
    'author_email': 'd.s.vanderheijden@tudelft.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bheijden/supergraph',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
