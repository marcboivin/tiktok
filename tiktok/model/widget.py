from basemodel import BaseModel, resourcemethod
from task import Task

class Widget( BaseModel ):

    fmt = "#%(id)d %(name)s - type:%(widget_type)s"

    routes = {
        'list'  : '/widgets/list.json',
        'tasks'   : '/widgets/show/%(widget_id)d.json',
    }

    @resourcemethod
    def tasks( cls, context, widget_id ):
        resource = context.resource
        return  [ Task( x['task'], context ) for x in
                    resource.getjson( cls.routes['tasks'] % {'widget_id' : widget_id} )
                ]

    @resourcemethod
    def list( cls, context ):
        resource = context.resource
        return [ cls( x['widget'], context ) for x in
                    resource.getjson( cls.routes['list'] )
               ]

    @resourcemethod
    def get( cls, context, widget_id ):
        resource = context.resource
        data = resource.getjson( self.routes['get'] % {'widget_id' : widget_id } )
        return cls( data, context )

