""" After: https://learndjango.com/tutorials/django-markdown-tutorial
Details extension from: https://facelessuser.github.io/pymdown-extensions/extensions/details/
"""

from django import template
from django.template.defaultfilters import stringfilter

import markdown as md
from .nesting_fenced_code import NestingFencedCodeExtension

register = template.Library()


@register.filter()
@stringfilter
def markdown(value):
    return md.markdown(value, extensions=['codehilite', NestingFencedCodeExtension(), 'pymdownx.details'])
