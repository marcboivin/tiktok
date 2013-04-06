import restkit
import cookiefilter
import cookielib
import json
import uuid
import urllib
import pprint
import re

from restkit.util import url_quote, to_bytestring

routes = {
    'login_redirect' : '/login/login',
    'login'     : '/login/validate',
    'logout'    : '/login/logout',
    'dashboard' : '/activities/list',
}

restkit.set_logging(10)

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

class ProjetsRessource( restkit.Resource ):
    
    routes = {
        'issue' : '/issues',
    }
    # Used to build the task name
    name = 'RM'
    content = False
    format = 'json'

    def __init__( self, domain, protocol, username, password, ID, **client_opts ):
        '''
            We use the domain and protocol variable, along with the username
            and password to create a Basic HTTP Auth URL. This should not be
            deployed for external uses, it's quite unsafe.
        '''
        u = urllib.quote(username)
        p = urllib.quote(password) 
        
        uri = protocol + '://' + username + ':' + password + '@' + domain + '/'
        
        restkit.Resource.__init__( self, uri, **client_opts )
        
        self.username = username
        self.password = password
        self.ID = ID
    
    def get_content( self ):
        if not self.content:
            # We're using get JSON so please don,t change the format at 
            # class level
            json_return = self.getjson(self.routes['issue'] + '/' + self.ID + '.' + self.format)
            self.content = json_return
        
        return self.content

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

    def get_cit_id( self ):
        return self.name + ' #' + self.ID

    def get_name( self ):
        content = self.get_content( )
        name = self.get_task_id + ' ' + content['issue']['subject']

        return name
            
    def get_project_id( self ):
        content = self.get_content( )
        project_id = re.search('P-[0-9\-]*', content['issue']['project']['name'])

        if project_id:
            project_id = project_id.group( 0 )

        return project_id 
