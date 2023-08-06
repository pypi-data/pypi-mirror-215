# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src/python'}

packages = \
['chef', 'chef.api']

package_data = \
{'': ['*']}

install_requires = \
['alembic>=1.11.1,<2.0.0',
 'fastapi>=0.97.0,<0.98.0',
 'loguru>=0.7.0,<0.8.0',
 'pillow>=9.5.0,<10.0.0',
 'python-multipart>=0.0.6,<0.0.7',
 'sqlalchemy>=2.0.16,<3.0.0',
 'uvicorn>=0.22.0,<0.23.0']

entry_points = \
{'console_scripts': ['chef = chef.main:serve']}

setup_kwargs = {
    'name': 'chef-recipes',
    'version': '1.0.1',
    'description': 'Home recipe management app.',
    'long_description': 'None',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
