"""
    Module contains utils methods used by library
"""

from dateutil.relativedelta import relativedelta

from todolib.models import EndType, Period
from todolib.exceptions import ObjectNotFoundError


def check_object_exist(obj, params, type):
    """
    Allow to ensure does the object exist.
    Throws ObjectNotFoundError
    """
    if obj is None:
        raise ObjectNotFoundError(f'{type} with params: {params} not found')


def get_interval(period_type: Period, period_quantity):
    """
    Calculates period type according to provided period and quantity.
    """
    if period_type.value == 'Min':
        return relativedelta(minutes=period_quantity)
    elif period_type.value == 'Hour':
        return relativedelta(hours=period_quantity)
    elif period_type.value == 'Day':
        return relativedelta(days=period_quantity)
    elif period_type.value == 'Week':
        return relativedelta(weeks=period_quantity)
    elif period_type.value == 'Month':
        return relativedelta(months=period_quantity)
    elif period_type.value == 'Year':
        return relativedelta(years=period_quantity)


def enum_converter(value, type, type_str):
    """
    Allows to convert string value to provided enum type.
    Otherwise throws KeyError exception.
    """
    try:
        value = type[value.upper()]
    except KeyError as e:
        raise KeyError(f'{type_str} not Found') from e
    return value


def get_end_type(start_date, period_type, period_amount,
                 end_date=None, repetitions_amount=None) -> EndType:
    """
    Allows to calculate end type by specified params
    """
    if end_date and repetitions_amount:
        interval = get_interval(period_type, period_amount)
        if interval * repetitions_amount + start_date < end_date:
            return EndType.AMOUNT
        return EndType.DATE
    '''
        When both end_date and repetitions_amount are set:
            Calculate how much times task can be repeated until the end_date
            if it less then end_date => EndType.AMOUNT
            othwerwise => EndType.DATE
        Otherwise we select EndType by (end_date or repetitions_amount) or
        just EndType.NEVER
    '''

    if end_date:
        return EndType.DATE
    if repetitions_amount:
        return EndType.AMOUNT
    return EndType.NEVER
