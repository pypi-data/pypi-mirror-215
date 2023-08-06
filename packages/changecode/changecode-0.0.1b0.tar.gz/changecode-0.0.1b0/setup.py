# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['changecode']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'changecode',
    'version': '0.0.1b0',
    'description': 'Change python code',
    'long_description': '# Changecode\n\n___\n',
    'author': 'BulatXam',
    'author_email': 'Khamdbulat@yandex.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
