# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cpyrt']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.9,<2.0.0']

setup_kwargs = {
    'name': 'cpyrt',
    'version': '0.1.0',
    'description': "A Python library for handling data in NIST's Cybersecurity and Privacy Reference Tool JSON format.",
    'long_description': None,
    'author': 'Al S',
    'author_email': 'xee5ch@member.fsf.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
