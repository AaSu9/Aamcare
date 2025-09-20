from django import template
from django.template.defaultfilters import stringfilter
from core.translation_utils import get_translation

register = template.Library()

@register.simple_tag(takes_context=True)
def trans(context, text):
    """
    Custom translation filter that can be used in templates
    Usage: {% trans "Hello" %}
    """
    # Get language from context or request session
    language = context.get('language', 'en')
    request = context.get('request')
    if request and hasattr(request, 'session'):
        language = request.session.get('django_language', language)
    
    return get_translation(text, language)

@register.simple_tag(takes_context=True)
def get_language(context):
    """
    Get the current language from session
    """
    request = context.get('request')
    if request and hasattr(request, 'session'):
        return request.session.get('django_language', 'en')
    return 'en'

@register.filter
def get_item(dictionary, key):
    """
    Get item from dictionary by key
    Usage: {{ dictionary|get_item:key }}
    """
    if dictionary is None:
        return None
    
    # Try to convert key to int if dictionary has int keys
    if isinstance(key, str) and key.isdigit():
        try:
            int_key = int(key)
            if int_key in dictionary:
                return dictionary[int_key]
        except (ValueError, TypeError):
            pass
    
    # Fall back to original key
    return dictionary.get(key) 