# prefab-cloud-django

This project provides custom template tags for using [`prefab-cloud-python`][prefabpython] in Django applications

## Usage

1. Add this project to your Django application's dependencies
2. Add `prefab_cloud_django` to the list of `INSTALLED_APPS` in your app's `settings.py`
3. Configure your Prefab client in `settings.py`

```python
options = prefab.Options(
    api_key="...",
    ...
    log_boundary=BASE_DIR,
)

PREFAB = prefab.Client(options)
LOGGER = PREFAB.logger
```

3. In your templates, add `{% load prefab_tags %}`

4. Use these tags

```python
{% prefab_get "name-of-config" %}
{% prefab_enabled "name-of-flag" %}

# with lookup key

{% prefab_get "name-of-config" lookup_key="lookup_key" %}
```

[prefabpython]: https://pypi.org/project/prefab-cloud-python/
