from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def prefab_get(key, **kwargs):
    default = kwargs.get("default")
    context = kwargs.get("context") or {}
    return settings.PREFAB.get(key, default=default, context=context)


@register.simple_tag
def prefab_enabled(feature_flag, **kwargs):
    context = kwargs.get("context") or {}
    return settings.PREFAB.enabled(feature_flag, context=context)
