
class TextDict( dict ):

    seperator = " : "

    def __init__( self, *args, **kwargs ):
        filename = kwargs.pop( 'filename', None )
        dict.__init__( self, *args, **kwargs )
        self.filename = filename

    def load( self, filename=None ):

        filename = filename or self.filename
        with open( filename, 'r' ) as f:
            self.update(
                dict(
                    unicode(x, encoding='utf8').strip().split( self.seperator )[0:2] for x in f
                )
            )

    def valid( self ):

        invalid = [ value for (key, value) in self.items() if not isinstance( value, (unicode, str) ) ]
        return len( invalid ) == 0

    def save( self, filename=None ):

        filename = filename or self.filename
        if not self.valid():
            raise ValueError("values in dict can only be strings")

        lines = (
            unicode( u"%s%s%s\n" % (key, self.seperator, value) ).encode('utf8') for
            (key, value) in self.items()
        )

        with open( filename, 'w' ) as f:
            f.writelines( lines )


if __name__ == '__main__':

    d = TextDict( filename = 'test' )
    d['1'] = 'a'
    d['2'] = 'b'
    d['3'] = 'c'
    d.save()

    e = TextDict( filename = 'test' )
    e.load()
    assert d == e

