# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['golem_core',
 'golem_core.cli',
 'golem_core.core',
 'golem_core.core.activity_api',
 'golem_core.core.activity_api.resources',
 'golem_core.core.events',
 'golem_core.core.golem_node',
 'golem_core.core.market_api',
 'golem_core.core.market_api.resources',
 'golem_core.core.market_api.resources.demand',
 'golem_core.core.market_api.resources.demand.demand_offer_base',
 'golem_core.core.market_api.resources.demand.demand_offer_base.payload',
 'golem_core.core.network_api',
 'golem_core.core.network_api.resources',
 'golem_core.core.payment_api',
 'golem_core.core.payment_api.resources',
 'golem_core.core.resources',
 'golem_core.core.resources.event_collectors',
 'golem_core.managers',
 'golem_core.managers.payment',
 'golem_core.pipeline',
 'golem_core.utils',
 'golem_core.utils.storage']

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
    'name': 'golem-api-python',
    'version': '0.1.1',
    'description': 'Golem Netowrk (https://www.golem.network/) API for Python',
    'long_description': 'None',
    'author': 'Golem Factory',
    'author_email': 'contact@golem.network',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/golemfactory/golem-core-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
