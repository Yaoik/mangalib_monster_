from django import template
from manga.utils import get_rgb_value

register = template.Library()

@register.filter
def get_color(value):
    red, green, blue = get_rgb_value(float(value))
    return f"rgb({red}, {green}, {blue})"
