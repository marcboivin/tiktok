from basemodel import BaseModel, resourcemethod
from task import Task

class Widget( BaseModel ):

    fmt = "#%(id)d %(name)s - type:%(widget_type)s"

    routes = {
        'list'  : '/widgets/list.json',
        'tasks'   : '/widgets/show/%(widget_id)d.json',
    }

    @resourcemethod
    def tasks(cls, resource, widget_id ):
        resource = resource or get_resource()
        return  [ Task( x['task'], resource ) for x in
                    resource.getjson( cls.routes['tasks'] % {'widget_id' : widget_id} ) 
                ]

    @resourcemethod
    def list( cls, resource ):
        resource = resource or get_resource()
        return [ cls( x['widget'], resource ) for x in
                    resource.getjson( cls.routes['list'] )
               ]

    @resourcemethod
    def get( cls, resource, widget_id ):
        resource = resource or get_resource()
        data = resource.getjson( self.routes['get'] % {'widget_id' : widget_id } )
        return cls( data, resource )

