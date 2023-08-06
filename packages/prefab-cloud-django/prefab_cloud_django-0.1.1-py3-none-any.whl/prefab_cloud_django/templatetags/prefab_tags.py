from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def prefab_get(key, **kwargs):
    lookup_key = kwargs.get("lookup_key")
    default = kwargs.get("default")
    properties = kwargs.get("properties") or {}
    return settings.PREFAB.get(key, default=default, lookup_key=lookup_key, properties=properties)


@register.simple_tag
def prefab_enabled(feature_flag, **kwargs):
    lookup_key = kwargs.get("lookup_key")
    attributes = kwargs.get("attributes") or {}
    return settings.PREFAB.enabled(feature_flag, lookup_key=lookup_key, attributes=attributes)
