import cookielib
import urllib2

class InfoWrapper( object ):

    def __init__(self, headers):
        self.headers = headers

    def sanitize_header_names( self, headers ):
        return dict(
            ( header.title(), value )
            for ( header, value ) in headers.items()
        )

    def getheaders(self, name):
        headers = self.sanitize_header_names( self.headers )
        return [ value for (key, value) in headers.items() if key == name ]

    def getallmatchingheaders(self, name):
        headers = self.sanitize_header_names( self.headers )
        return [ "%s: %s" % (key, value) for (key, value) in headers.items() if key == name ]

class ResourceWrapper( object ):

    def __init__(self, headers):
        self.info_wrapper = InfoWrapper( headers )

    def info(self):
        return self.info_wrapper

class CookieFilter( object ):

    def __init__(self, cookiejar = None):
        cookiejar = cookiejar or cookielib.CookieJar()
        self.cookiejar = cookiejar

    def on_request(self, request):
        fake_req = urllib2.Request( url = request.url )
        self.cookiejar.add_cookie_header( fake_req )
        headers = fake_req.headers
        headers.update( fake_req.unredirected_hdrs )
        request.headers.update( headers )

    def on_response(self, response, request):
        fake_request = urllib2.Request( url = request.url )
        headers = response.headers
        fake_resource = ResourceWrapper( headers )
        self.cookiejar.extract_cookies( fake_resource, fake_request )

