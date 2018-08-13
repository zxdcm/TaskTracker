from dateutil.relativedelta import relativedelta
from .models import EndType


def get_interval(period_type, period_quantity):
    if period_type.value == 'Min':
        return relativedelta(minutes=period_quantity)
    if period_type.value == 'Hour':
        return relativedelta(hours=period_quantity)
    elif period_type.value == 'Day':
        return relativedelta(days=period_quantity)
    elif period_type.value == 'Week':
        return relativedelta(weeks=period_quantity)
    elif period_type.value == 'Month':
        return relativedelta(months=period_quantity)
    elif period_type.value == 'Years':
        return relativedelta(years=period_quantity)


def get_end_type(task_start_date,
                 end_date=None, repetitions_amount=None) -> EndType:

    if end_date and repetitions_amount:
        interval = get_interval(end_date, repetitions_amount)
        print(end_date, repetitions_amount, end=' ')
        if interval * repetitions_amount + task_start_date < end_date:
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
