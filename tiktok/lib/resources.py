import restkit
import cookiefilter
import cookielib
import json

routes = {
    'login_redirect' : '/login/login',
    'login'     : '/login/validate',
    'logout'    : '/login/logout',
    'dashboard' : '/activities/list',
}

resource = None

def init_resource( url, username, password ):
    global resource
    resource = TikTakResource( url, username, password )
    resource.login()

def get_resource():
    global resource
    return resource

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


    def json_request(self, method, path, payload=None, headers=None, params_dict=None, **params):
        if not path.endswith('.json'):
            path += '.json'
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



