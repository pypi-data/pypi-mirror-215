# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src']

package_data = \
{'': ['*']}

install_requires = \
['pyinquirer>=1.0.3,<2.0.0',
 'python-dotenv>=1.0.0,<2.0.0',
 'requests>=2.31.0,<3.0.0',
 'rich>=13.4.2,<14.0.0',
 'textual[dev]>=0.28.0,<0.29.0',
 'typer[all]>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'linear-cli-ai',
    'version': '0.1.0',
    'description': 'A simple cli for interacting with linear',
    'long_description': '# linear-cli\nA CLI for the linear app\n',
    'author': 'scar3crow',
    'author_email': 'rss.holmes@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.8.10',
}


setup(**setup_kwargs)
