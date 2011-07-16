from collections import namedtuple
from durations import sets as duration_sets
from prettyprinter import PrettyPrinter
import datetime

helpers = None

def create_helper( config, resource ):

    members = ['resource', 'duration', 'datetime', 'date', 'printer', 'pprint', 'config']

    Helpers = namedtuple( 'Helpers', members )
    DurationHelper = namedtuple('DurationHelper', ['parser', 'parse', 'formatter', 'format'] )
    DateTimeHelper = namedtuple('DateTimeHelper', ['parse', 'format'] )
    DateHelper = namedtuple('DateHelper', ['parse', 'format'] )

    d_format = config['duration_format']

    if d_format in ('alarmclock', 'decimal'):

        parser = duration_sets[ d_format ][0]()
        formatter = duration_sets[ d_format ][1]()

    else:
        parser = duration_sets[ d_format ][0](
            int( config['days_in_week'] ),
            int( config['minutes_in_day'] )
        )

        formatter =  duration_sets[d_format][1](
            int( config['days_in_week'] ),
            int( config['minutes_in_day'] )
        )

    duration_helper = DurationHelper(
        parser,
        parser.parse,
        formatter,
        formatter.format
    )

    datetime_helper = DateTimeHelper(
     lambda x: datetime.datetime.strptime( x, config['datetime_format'] ),
     lambda x: datetime.datetime.strftime( x, config['datetime_format'] )
    )

    date_helper = DateHelper(
        lambda x: datetime.datetime.strptime( x, config['date_format'] ).date(),
        lambda x: datetime.datetime.strftime( x, config['date_format'] ).date()
    )

    pretty_printer = PrettyPrinter( formatter, config['datetime_format'] )

    helpers = Helpers(
        resource,
        duration_helper,
        datetime_helper,
        date_helper,
        pretty_printer,
        pretty_printer.pprint,
        config
    )

    return helpers

def set_helper( new_helper ):
    global helpers
    helpers = new_helper

def get_helper():
    global helpers
    return helpers
