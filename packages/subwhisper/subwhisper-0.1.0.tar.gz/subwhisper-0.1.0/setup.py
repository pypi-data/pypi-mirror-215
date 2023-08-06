# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'subwhisper',
    'version': '0.1.0',
    'description': '',
    'long_description': "SubWhisper\n---------\n\nUse command for preload model\n```python\nfrom subwhisper import setup\n\nsetup()\n```\n\nUse command for transcribe audio\n```python\nfrom subwhisper import process\n\nprocess(file='/path/to/file')\n```\n",
    'author': 'tupiznak',
    'author_email': 'akej-vonavi@mail.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
