# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['prefab_cloud_django', 'prefab_cloud_django.templatetags']

package_data = \
{'': ['*']}

install_requires = \
['Django>=4.2,<5.0', 'prefab-cloud-python>=0.3.3']

setup_kwargs = {
    'name': 'prefab-cloud-django',
    'version': '0.2.0',
    'description': 'Custom template tags for using prefab-cloud-python in Django applications',
    'long_description': '# prefab-cloud-django\n\nThis project provides custom template tags for using [`prefab-cloud-python`][prefabpython] in Django applications\n\n## Usage\n\n1. Add this project to your Django application\'s dependencies\n2. Add `prefab_cloud_django` to the list of `INSTALLED_APPS` in your app\'s `settings.py`\n3. Configure your Prefab client in `settings.py`\n\n```python\noptions = prefab.Options(\n    api_key="...",\n    ...\n    log_boundary=BASE_DIR,\n)\n\nPREFAB = prefab.Client(options)\nLOGGER = PREFAB.logger\n```\n\n3. In your templates, add `{% load prefab_tags %}`\n\n4. Use these tags\n\n```python\n{% prefab_get "name-of-config" %}\n{% prefab_enabled "name-of-flag" %}\n\n# with default\n\n{% prefab_get "name-of-config" default="default" %}\n\n# with context\n\n{% prefab_get "name-of-config" context=context %}\n```\n\n[prefabpython]: https://pypi.org/project/prefab-cloud-python/\n',
    'author': 'Michael Berkowitz',
    'author_email': 'michael.berkowitz@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
