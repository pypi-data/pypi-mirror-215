# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sathouel_ftp_client']

package_data = \
{'': ['*']}

install_requires = \
['paramiko>=3.2.0,<4.0.0']

setup_kwargs = {
    'name': 'sathouel-ftp-client',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Steven Athouel',
    'author_email': 'sathouel@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
