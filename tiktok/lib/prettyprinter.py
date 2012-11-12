import datetime

class PrettyPrinter( object ):

    def __init__( self, duration_formatter, datetime_format ):

        self.duration_formatter = duration_formatter
        self.datetime_format = datetime_format

    def sanitize_string( self, text ):
        if isinstance( text, str ):
            text = text.decode("utf8")
        return text

    def format( self, obj, format ):

        data = {}
        for key, value in obj.items():

            if isinstance( value, datetime.timedelta ):
                data[key] = self.duration_formatter.format( value )
            elif isinstance( value, datetime.datetime ):
                data[key] = datetime.datetime.strftime( value, self.datetime_format )
            else:
                data[key] = value

        return self.sanitize_string( format % data )

    def pprint( self, obj, format ):

        print self.format( obj, format ).encode("utf8")

