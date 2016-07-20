from django import template
from anlzer.custom_modules import time_greeting
import os

register = template.Library()


@register.filter
def equals(value, arg):
    """Compares the value of the variable with the value of the arg"""
    return value == arg


@register.filter
def get_filename(value):
    """
    Returns the name of the uploaded file
    """
    return os.path.basename(value.file.name)


@register.filter
def get_appropriate_greeting(user):
    return time_greeting.time_greeting(user)
