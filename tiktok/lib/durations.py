import datetime
import re

format_regex = {
    'alarmclock' : r"(?P<hours>\d{1,2}):(?P<minutes>[0-5][0-9])",
    'colons' : r"((\d+):)?((\d+):)?((\d+):)?([0-5]?[0-9])",
    'standard' : r"((?P<weeks>\d+)w)? ?((?P<days>\d+)d)? ?((?P<hours>\d{1,2})h)? ?((?P<minutes>[0-5]?[0-9]?)m)?",
}

format_template = {
    'alarmclock' : "%(hours)02d:%(minutes)02d",
    'colons' : "%(weeks)d:%(days)d:%(hours)d:%(minutes)d",
    'compact' : "%(weeks)dw%(days)dd%(hours)dh%(minutes)dm",
    'standard' : "%(weeks)dw %(days)dd %(hours)dh %(minutes)dm",
}

MINUTE = 60
HOUR = MINUTE * 60
DAY = HOUR * 24
WEEK = DAY * 7

def secs_to_timedelta( secs ):
    info = {
        'weeks' : secs / WEEK,
        'days' : (secs % WEEK) / DAY,
        'hours' : (secs % DAY) / HOUR,
        'minutes' : (secs % HOUR) / MINUTE,
        'seconds' : (secs % MINUTE)
    }
    return datetime.timedelta( **info )

def total_seconds( td ):

    return td.days * DAY + td.seconds

class DurationParser( object ):

    def parse( self, text ):

        match = self.regex.match( text )
        if not match:
            raise ValueError( "datetime does not match format" )
        self.match = match


class ClockParser( DurationParser ):

    regex =  re.compile( format_regex['alarmclock'] )

    def parse( self, text ):

        DurationParser.parse( self, text )

        group = self.match.groupdict()

        hours = int( group['hours'] )
        minutes = int( group['minutes'] )

        duration = secs_to_timedelta( hours * HOUR + minutes * MINUTE )

        return duration

class ColonParser( DurationParser ):

    regex = re.compile( format_regex['colons'] )

    def __init__( self, days_in_week, day_length ):
        DurationParser.__init__( self )
        self.days_in_week = days_in_week
        self.day_length = day_length

    def parse( self, text ):

        DurationParser.parse( self, text )

        numbers = [ x for x in self.match.groups() if x ]

        weeks = days = hours = 0

        minutes = int( numbers[ -1 ] )
        if len( numbers ) >= 3:
            hours  = int( numbers[ -2 ] )
        if len( numbers ) >= 5:
            days = int( numbers[ -4 ] )
        if len( numbers ) >= 7:
            weeks = int( numbers[ -6 ] )

        total_minutes = weeks * self.days_in_week * self.day_length
        total_minutes += days * self.day_length
        total_minutes += hours * 60
        total_minutes += minutes

        duration = secs_to_timedelta( total_minutes * MINUTE )

        return duration

class StandardParser( DurationParser ):

    regex = re.compile( format_regex['standard'] )

    def __init__( self, days_in_week, day_length ):
        DurationParser.__init__( self )
        self.days_in_week = days_in_week
        self.day_length = day_length

    def parse( self, text ):

        DurationParser.parse( self, text )

        group = dict( (key, value) for (key, value) in self.match.groupdict().items() if value )

        weeks = int( group.get( 'weeks', 0 ) )
        days = int( group.get( 'days', 0 ) )
        hours = int( group.get( 'hours', 0 ) )
        minutes = int( group['minutes'] )

        total_minutes = weeks * self.days_in_week * self.day_length
        total_minutes += days * self.day_length
        total_minutes += hours * 60
        total_minutes += minutes

        duration = secs_to_timedelta( total_minutes * MINUTE )

        return duration

class CompactParser( StandardParser ):
    pass



class DurationFormat( object ):

    def format( self, duration ):
        raise NotImplementedError

class ClockFormat( DurationFormat ):

    template = format_template['alarmclock']

    def format( self, duration ):

        secs = total_seconds( duration )

        hours = secs / HOUR
        minutes = (secs % HOUR) / MINUTE

        return self.template % {
                'hours' : hours,
                'minutes' : minutes
                }

class StandardFormat( DurationFormat ):

    template = format_template['standard']

    def __init__( self, days_in_week, day_length ):
        DurationFormat.__init__( self )
        self.days_in_week = days_in_week
        self.day_length = day_length

    def format( self, duration ):

        total_minutes = total_seconds( duration ) / MINUTE

        weeks = total_minutes / (self.day_length * self.days_in_week)
        total_minutes -= weeks * self.day_length * self.days_in_week

        days = total_minutes / self.day_length
        total_minutes-= days * self.day_length

        hours = total_minutes / 60
        minutes = total_minutes % 60

        data = {
            'weeks' : weeks,
            'days' : days,
            'hours' : hours,
            'minutes' : minutes,
            }

        return self.template % data

class ColonFormat( StandardFormat ):

    template = format_template['colons']

class CompactFormat( StandardFormat ):

    template = format_template['compact']

