import datetime
import re

format_regex = {
    'alarmclock' : r"(?P<hours>\d{1,2}):(?P<minutes>[0-5][0-9])",
    'colons' : r"((\d+):)?((\d+):)?((\d+):)?([0-5]?[0-9])",
    'standard' : r"((?P<weeks>\d+)w)? ?((?P<days>\d+)d)? ?((?P<hours>\d{1,2})h)? ?((?P<minutes>[0-5]?[0-9]?)m)?",
    'decimal' : r"(?P<hours>\d+)\.(?P<minutes>\d{2})",
}

format_template = {
    'alarmclock' : "%(hours)02d:%(minutes)02d",
    'colons' : "%(weeks)s%(days)s%(hours)s%(minutes)s",
    'compact' : "%(weeks)s%(days)s%(hours)s%(minutes)s",
    'standard' : "%(weeks)s %(days)s %(hours)s %(minutes)s",
    'decimal' : "%(hours)02d.%(minutes)02d",
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

class DecimalParser( DurationParser ):

    regex = re.compile( format_regex['decimal'] )

    def parse( self, text ):

        DurationParser.parse( self, text )

        group = self.match.groupdict()

        hours = int( group['hours'] )
        minutes = int( group['minutes'] )
        minutes = int( minutes / 100.0 * 60 )

        duration = secs_to_timedelta( hours * HOUR + minutes * MINUTE )

        return duration

class StandardParser( DurationParser ):

    regex = re.compile( format_regex['standard'] )

    def __init__( self, days_in_week, day_length ):
        DurationParser.__init__( self )
        self.days_in_week = days_in_week
        self.day_length = day_length

    def duration( self, weeks, days, hours, minutes ):

        total_minutes = weeks * self.days_in_week * self.day_length
        total_minutes += days * self.day_length
        total_minutes += hours * 60
        total_minutes += minutes

        duration = secs_to_timedelta( total_minutes * MINUTE )

        return duration

    def parse( self, text ):

        DurationParser.parse( self, text )

        group = dict( (key, value) for (key, value) in self.match.groupdict().items() if value )

        weeks = int( group.get( 'weeks', 0 ) )
        days = int( group.get( 'days', 0 ) )
        hours = int( group.get( 'hours', 0 ) )
        minutes = int( group['minutes'] )

        return self.duration( weeks, days, hours, minutes )

class ColonParser( StandardParser ):

    regex = re.compile( format_regex['colons'] )

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

        return self.duration( weeks, days, hours, minutes )

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

class DecimalFormat( DurationFormat ):

    template = format_template['decimal']

    def format( self, duration ):

        secs = total_seconds( duration )

        hours = secs / HOUR
        minutes = (secs % HOUR) / MINUTE
        minutes = int( minutes / 60.0 * 100 )

        return self.template % {
                'hours' : hours,
                'minutes' : minutes
                }

class StandardFormat( DurationFormat ):

    template = format_template['standard']

    whitespace = re.compile( r"\s{2,}" )

    suffixes = {
        'weeks' : 'w',
        'days' : 'd',
        'hours' : 'h',
        'minutes' : 'm'
    }

    particle_template = "%d%s"

    elements = ( 'weeks', 'days', 'hours', 'minutes' )

    def __init__( self, days_in_week, day_length ):
        DurationFormat.__init__( self )
        self.days_in_week = days_in_week
        self.day_length = day_length

    def values( self, duration ):

        total_minutes = total_seconds( duration ) / MINUTE

        weeks = total_minutes / (self.day_length * self.days_in_week)
        total_minutes -= weeks * self.day_length * self.days_in_week

        days = total_minutes / self.day_length
        total_minutes-= days * self.day_length

        hours = total_minutes / 60
        minutes = total_minutes % 60

        return (weeks, days, hours, minutes)

    def particle( self, suffix, value ):
        return self.particle_template % (value, self.suffixes[suffix])

    def sub_template( self, particles ):

        data = {
            'weeks' : '',
            'days' : '',
            'hours' : '',
            'minutes' : '',
        }
        data.update( particles )

        fmt = self.template % data

        return self.whitespace.sub( " ", fmt ).strip()

    def format( self, duration ):

        values = zip( self.elements, self.values( duration ) )

        data = {}

        for suffix, value in values:
            if value > 0:
                data[suffix] = self.particle( suffix, value )

        return self.sub_template( data )

class ColonFormat( StandardFormat ):

    suffixes = {
        'weeks' : ':',
        'days' : ':',
        'hours' : ':',
        'minutes' : '',
    }

    template = format_template['colons']

    def format( self, duration ):

        values = zip( self.elements, self.values( duration ) )
        data = {}

        for x in range( len( values ) ):

            suffix, value = values[x]

            if value > 0:
                data[suffix] = self.particle( suffix, value )
                for sub_s, sub_v in values[x + 1:]:
                    data[sub_s] = self.particle( sub_s, 0 )


        return self.sub_template( data )


class CompactFormat( StandardFormat ):

    template = format_template['compact']


if __name__ == '__main__':

    #Parser tests
    parser = ClockParser()


    t = parser.parse( "12:34" )
    secs = 12 * HOUR + 34 * MINUTE
    assert total_seconds( t ) == secs

    parser = DecimalParser()

    t = parser.parse( "12.99" )
    secs = 12 * HOUR + 59 * MINUTE
    assert total_seconds( t ) == secs

    parser = ColonParser( 5, 7 * 60 )

    t = parser.parse( "1:2:3:4" )
    secs = 5 * ( 7 * HOUR ) + 2 * ( 7 * HOUR ) + 3 * HOUR + 4 * MINUTE
    assert total_seconds( t ) == secs

    t = parser.parse( "2:03:4" )
    secs = 2 * ( 7 * HOUR ) + 3 * HOUR + 4 * MINUTE
    assert total_seconds( t ) == secs

    t = parser.parse( "3:04" )
    secs = 3 * HOUR + 4 * MINUTE
    assert total_seconds( t ) == secs

    t = parser.parse( "4" )
    secs = 4 * MINUTE
    assert total_seconds( t ) == secs



    parser = StandardParser( 5, 7 * 60 )

    t = parser.parse( "1w 2d 3h 4m" )
    secs = 5 * ( 7 * HOUR ) + 2 * ( 7 * HOUR ) + 3 * HOUR + 4 * MINUTE
    assert total_seconds( t ) == secs

    t = parser.parse( "002d 3h 4m" )
    secs = 2 * ( 7 * HOUR ) + 3 * HOUR + 4 * MINUTE
    assert total_seconds( t ) == secs

    t = parser.parse( "03h 4m" )
    secs = 3 * HOUR + 4 * MINUTE
    assert total_seconds( t ) == secs

    t = parser.parse( "04m" )
    secs = 4 * MINUTE
    assert total_seconds( t ) == secs

    t = parser.parse( "1w 2h 3m" )
    secs = 5 * ( 7 * HOUR ) + 2 * HOUR + 3 * MINUTE
    assert total_seconds( t ) == secs

    t = parser.parse( "0001d 2m" )
    secs = 7 * HOUR + 2 * MINUTE
    assert total_seconds( t ) == secs



    #Format tests
    f = ClockFormat()

    t = secs_to_timedelta( HOUR * 34 + MINUTE * 56 )
    assert f.format( t ) == "34:56"

    t = secs_to_timedelta( 3 )
    assert f.format( t ) == "00:00"



    f = DecimalFormat()

    t = secs_to_timedelta( HOUR * 12 + MINUTE * 59 )
    assert f.format( t ) == "12.98"

    t = secs_to_timedelta( HOUR * 12 + MINUTE * 30 )
    assert f.format( t ) == "12.50"



    day = 7 * HOUR
    week = 5 * day
    hour = HOUR
    minute = MINUTE

    f = StandardFormat( 5, 7 * 60 )

    t = secs_to_timedelta( 1 * week + 2 * day + 3 * hour + 4 * minute )
    assert f.format( t ) == "1w 2d 3h 4m"

    t = secs_to_timedelta( 1 * day + 2 * hour + 3 * minute )
    assert f.format( t ) == "1d 2h 3m"

    t = secs_to_timedelta( 1 * hour + 2 * minute )
    assert f.format( t ) == "1h 2m"

    t = secs_to_timedelta( minute )
    assert f.format( t ) == "1m"

    t = secs_to_timedelta( 1 * week + 2 * hour )
    assert f.format( t ) == "1w 2h"



    f = CompactFormat( 5, 7 * 60 )

    t = secs_to_timedelta( 1 * week + 2 * day + 3 * hour + 4 * minute )
    assert f.format( t ) == "1w2d3h4m"

    t = secs_to_timedelta( 1 * day + 2 * hour + 3 * minute )
    assert f.format( t ) == "1d2h3m"

    t = secs_to_timedelta( 1 * hour + 2 * minute )
    assert f.format( t ) == "1h2m"

    t = secs_to_timedelta( minute )
    assert f.format( t ) == "1m"

    t = secs_to_timedelta( 1 * week + 2 * hour )
    assert f.format( t ) == "1w2h"



    f = ColonFormat( 5, 7 * 60 )

    t = secs_to_timedelta( 1 * week + 2 * day + 3 * hour + 4 * minute )
    assert f.format( t ) == "1:2:3:4"

    t = secs_to_timedelta( 1 * day + 2 * hour + 3 * minute )
    assert f.format( t ) == "1:2:3"

    t = secs_to_timedelta( 1 * day + 2 * minute )
    assert f.format( t ) == "1:0:2"

    t = secs_to_timedelta( 1 * week + 2 * minute )
    assert f.format( t ) == "1:0:0:2"

