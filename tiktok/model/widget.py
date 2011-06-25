from basemodel import BaseModel, get_resource
from task import Task

class Widget( BaseModel ):

    fmt = "#%(id)d %(name)s - type:%(widget_type)s"

    routes = {
        'list'  : '/widgets/list.json',
        'tasks'   : '/widgets/show/%(widget_id)d.json',
    }

    @classmethod
    def tasks(cls, widget_id, resource=None):
        resource = resource or get_resource()
        return  [ Task( x['task'], resource ) for x in
                    resource.getjson( cls.routes['tasks'] % {'widget_id' : widget_id} ) 
                ]
   
    @classmethod
    def list( cls, resource=None ):
        resource = resource or get_resource()
        return [ cls( x['widget'], resource ) for x in
                    resource.getjson( cls.routes['list'] )
               ]

    @classmethod
    def get( cls, widget_id, resource=None ):
        resource = resource or get_resource()
        data = resource.getjson( self.routes['get'] % {'widget_id' : widget_id } )
        return cls( data, resource )

