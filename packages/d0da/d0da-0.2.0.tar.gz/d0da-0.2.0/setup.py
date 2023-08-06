# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['d0da']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'protobuf>=4.23.2,<5.0.0']

entry_points = \
{'console_scripts': ['d0da-cli = d0da.cli:main']}

setup_kwargs = {
    'name': 'd0da',
    'version': '0.2.0',
    'description': 'Wooting D0DA protocol',
    'long_description': "# Wooting D0DA Protocol\n\n## Introduction\n\nWooting has been very generous in supplying Open Source (!) SDKs for their hardware, only, the SDKs aren't\nvery thoroughly documented, limited to a single use case and written in C.\n\nThis repository tries to fill in these gaps, it generated the packets and the used fields are described. It also\ndescribes what the packets do and in what order they should be sent.\n\n## Features\n\n- Technical documentation\n- Command line interface (d0da-cli) for sending packets to the keyboard\n- Unit tests\n\n## Limitations\n\n- Linux only (for now)\n- Wooting 60HE (ARM) only, though the packets should be compatible with other keyboards.\n\n## Installation\n\nRun:\n\n```bash\npipx install d0da\n```\n",
    'author': 'Dick Marinus',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
