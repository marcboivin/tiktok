import restkit
import cookiefilter
import cookielib
import json
import uuid

from restkit.util import url_quote, to_bytestring

routes = {
    'login_redirect' : '/login/login',
    'login'     : '/login/validate',
    'logout'    : '/login/logout',
    'dashboard' : '/activities/list',
}

def form_encode(obj, charset="utf8"):

    if hasattr( obj, 'items' ):
        obj = obj.items()

    lines = [
        ( u"%s=%s" %
            ( url_quote(key), url_quote(value) )
        ).encode( charset ) for
            (key, value) in obj
    ]
    return to_bytestring( "&".join( lines ) )

class LoginError( Exception ):

    def __init__(self, username):
        self.username = username

    def __str__(self):
        return "Error during login of user %s" % self.username

class TikTakResource( restkit.Resource ):

    def __init__(self, uri, username, password, **client_opts):

        cookiejar = client_opts.pop( 'cookiejar', cookielib.CookieJar() )
        client_opts.update( {'filters' : [ cookiefilter.CookieFilter( cookiejar ) ] } )

        restkit.Resource.__init__( self, uri, **client_opts )

        self.username = username
        self.password = password

    def login(self):

        data = {
            'user[username]' : self.username,
            'user[password]' : self.password
        }

        resp = restkit.Resource.request( self, 'POST', routes['login'], data )
        if not ( 300 < resp.status_int < 400 and resp.location.endswith( routes['dashboard'] ) ):
            raise LoginError( self.username )

    def logout(self):

        self.get( routes['logout'], data )

    def request( self, method, path, payload=None, headers=None, params_dict=None, **params ):

        #HACK: restkit accepts dict payloads but not lists although
        #the code in client and wrappers would work (go figure)
        #TODO: submit a patch with my form_encode function
        if isinstance( payload, list ):
            payload = form_encode( payload )
            headers = headers or {}
            headers.update({
                'Content-Type' : 'application/x-www-form-urlencoded; charset=utf-8',
                'Content-Length' : len( payload )
                })

        return restkit.Resource.request( self, method, path, payload, headers, params_dict, **params )

    def json_request(self, method, path, payload=None, headers=None, params_dict=None, **params):
        resp = self.request(method, path, payload, headers, params_dict, **params)
        return json.loads( resp.body_string() )

    def getjson( self, path, payload=None, headers=None, params_dict=None, **params):
        return self.json_request( 'GET', path, payload, headers, params_dict, **params)

    def postjson( self, path, payload=None, headers=None, params_dict=None, **params):
        return self.json_request( 'POST', path, payload, headers, params_dict, **params)

    def putjson( self, path, payload=None, headers=None, params_dict=None, **params):
        return self.json_request( 'PUT', path, payload, headers, params_dict, **params)

    def deletejson( self, path, payload=None, headers=None, params_dict=None, **params):
        return self.json_request( 'DELETE', path, payload, headers, params_dict, **params)

class RedmineRessource( reskit.Ressource ):
    
    routes = {
        'issue' : '/issues/',
    }
    
    format = 'json'
    __init__( self, domain, protocol, username, password, **client_opts ):
    '''
        We use the domain and protocol variable, along with the username
        and password to create a Basic HTTP Auth URL. This should not be
        deployed for external uses, it's quite unsafe.
    '''
    
        # Construct said URL
        uri = protocol + '://' + username + ':' + password + '@' + domain + '/'
        
        restkit.Resource.__init__( self, uri, **client_opts )
        
        self.username = username
        self.password = password
        
        def get_issue( self, issue_id ):
            # We're using get JSON so please don,t change the format at 
            # class level
            self.getjson(self.routes.issue + '/' + issue_id + '.' + slef.format)

        def request( self, method, path, payload=None, headers=None, params_dict=None, **params ):

            #HACK: restkit accepts dict payloads but not lists although
            #the code in client and wrappers would work (go figure)
            #TODO: submit a patch with my form_encode function
            if isinstance( payload, list ):
                payload = form_encode( payload )
                headers = headers or {}
                headers.update({
                    'Content-Type' : 'application/x-www-form-urlencoded; charset=utf-8',
                    'Content-Length' : len( payload )
                    })

            return restkit.Resource.request( self, method, path, payload, headers, params_dict, **params )

        def json_request(self, method, path, payload=None, headers=None, params_dict=None, **params):
            resp = self.request(method, path, payload, headers, params_dict, **params)
            return json.loads( resp.body_string() )

        def getjson( self, path, payload=None, headers=None, params_dict=None, **params):
            return self.json_request( 'GET', path, payload, headers, params_dict, **params)

        def postjson( self, path, payload=None, headers=None, params_dict=None, **params):
            return self.json_request( 'POST', path, payload, headers, params_dict, **params)

        def putjson( self, path, payload=None, headers=None, params_dict=None, **params):
            return self.json_request( 'PUT', path, payload, headers, params_dict, **params)

        def deletejson( self, path, payload=None, headers=None, params_dict=None, **params):
            return self.json_request( 'DELETE', path, payload, headers, params_dict, **params)