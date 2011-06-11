from basemodel import BaseModel

class Widget( BaseModel ):

    fmt = "#%(id)d %(name)s - type:%(widget_type)s"

    routes = {
        'list'  : '/widgets/list',
        'get'   : '/widgets/show/%(widget_id)d',
    }

    def tasks(self, widget_id):
        return  [ x['task'] for x in
                  self.resource.getjson( self.routes['get'] % {'widget_id' : widget_id} ) 
                ]

    def list(self):
        return [ x['widget'] for x in
                 self.resource.getjson( self.routes['list'] )
               ]

