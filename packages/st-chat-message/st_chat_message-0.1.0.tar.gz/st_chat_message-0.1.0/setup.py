# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['st_chat_message']

package_data = \
{'': ['*'],
 'st_chat_message': ['frontend/out/*',
                     'frontend/out/_next/static/IMEkTAcHxgV58XEAbyzrE/*',
                     'frontend/out/_next/static/chunks/*',
                     'frontend/out/_next/static/chunks/pages/*',
                     'frontend/out/_next/static/css/*',
                     'frontend/out/_next/static/media/*']}

install_requires = \
['streamlit>=0.63']

setup_kwargs = {
    'name': 'st-chat-message',
    'version': '0.1.0',
    'description': 'A Streamlit component to display chat messages',
    'long_description': '',
    'author': 'Manolo Santos',
    'author_email': 'manolo.santos@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8, !=2.7.*, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*, !=3.7.*',
}


setup(**setup_kwargs)
