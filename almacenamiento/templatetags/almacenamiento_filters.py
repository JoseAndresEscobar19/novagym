from django import template

from decimal import Decimal

register = template.Library()


@register.filter(name="conversion")
def conversion(kylobytes):
    mb = kylobytes * Decimal(str(0.001))
    if mb >= 1 and mb < 1000:
        return f'{round(mb,1)} MB'
    
    gb = mb * Decimal(str(0.001))
    if gb >= 1 and gb < 1000:
        return f'{round(gb, 1)} GB'
    
    tb = gb * Decimal(str(0.001))
    if tb >= 1 and tb < 1000:
        return f'{round(tb, 1)} TB'
    
    return f'{kylobytes} KB'


@register.filter(name="calculate_percentage")
def calculate_percentage(used, total):
    division = used / total
    if division >= 1:
        return 100
    return round(division * 100, 0)


@register.filter(name="to_mb")
def to_mb(kylobytes):
    mb = kylobytes * Decimal(str(0.001))
    return str(round(mb, 0))