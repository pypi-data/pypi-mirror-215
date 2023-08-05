# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['golem_py',
 'golem_py.cli',
 'golem_py.core',
 'golem_py.core.activity_api',
 'golem_py.core.activity_api.resources',
 'golem_py.core.events',
 'golem_py.core.golem_node',
 'golem_py.core.market_api',
 'golem_py.core.market_api.resources',
 'golem_py.core.market_api.resources.demand',
 'golem_py.core.market_api.resources.demand.demand_offer_base',
 'golem_py.core.market_api.resources.demand.demand_offer_base.payload',
 'golem_py.core.network_api',
 'golem_py.core.network_api.resources',
 'golem_py.core.payment_api',
 'golem_py.core.payment_api.resources',
 'golem_py.core.resources',
 'golem_py.core.resources.event_collectors',
 'golem_py.managers',
 'golem_py.managers.payment',
 'golem_py.pipeline',
 'golem_py.utils',
 'golem_py.utils.storage']

package_data = \
{'': ['*']}

install_requires = \
['async-exit-stack==1.0.1',
 'click>=8.1.3,<9.0.0',
 'jsonrpc-base>=1.0.3,<2.0.0',
 'prettytable>=3.4.1,<4.0.0',
 'semantic-version>=2.8,<3.0',
 'srvresolver>=0.3.5,<0.4.0',
 'ya-aioclient>=0.6.4,<0.7.0']

setup_kwargs = {
    'name': 'golem-py',
    'version': '0.1.0',
    'description': 'Python Golem (https://www.golem.network/) Core API',
    'long_description': 'None',
    'author': 'Jan Betley',
    'author_email': 'jan.betley@golem.network',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/golemfactory/golem-core-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
