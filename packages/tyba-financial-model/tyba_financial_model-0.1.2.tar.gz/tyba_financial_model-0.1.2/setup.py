# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['project_finance']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.24.1,<2.0.0', 'pydantic>=1.10.4,<2.0.0']

setup_kwargs = {
    'name': 'tyba-financial-model',
    'version': '0.1.2',
    'description': '',
    'long_description': 'None',
    'author': 'Casey Zak',
    'author_email': 'czak24@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
