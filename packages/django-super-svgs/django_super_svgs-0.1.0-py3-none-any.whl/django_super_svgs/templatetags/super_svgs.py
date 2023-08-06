from django import template

from .base import RenderSvg

register = template.Library()


@register.tag
def svg(parser, token):
    """Return a choosen svg rendered."""
    return RenderSvg(parser=parser, token=token)
