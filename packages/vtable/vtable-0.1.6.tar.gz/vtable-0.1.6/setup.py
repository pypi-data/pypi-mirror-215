# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vtable']

package_data = \
{'': ['*']}

install_requires = \
['PyQt5', 'ipdb', 'numpy', 'pandas']

entry_points = \
{'console_scripts': ['vtable = vtable.main:main']}

setup_kwargs = {
    'name': 'vtable',
    'version': '0.1.6',
    'description': 'A Qt based table viewer for Python',
    'long_description': '# qtable\nA QT based table viewer with filters\n',
    'author': 'fergal',
    'author_email': 'fergal.mullally@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>3.6',
}


setup(**setup_kwargs)
