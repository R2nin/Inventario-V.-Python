from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Retorna dictionary[key], convertendo key para string (padrão dos logs)."""
    return dictionary.get(str(key))
