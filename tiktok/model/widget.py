from basemodel import BaseModel, resourcemethod
from task import Task

class Widget( BaseModel ):

    fmt = "#%(id)d %(name)s - type:%(widget_type)s"

    routes = {
        'list'  : '/widgets/list.json',
        'tasks'   : '/widgets/show/%(widget_id)d.json',
    }

    @resourcemethod
    def tasks(cls, widget_id, **kwargs ):
        resource = kwargs['resource']
        return  [ Task( x['task'], **kwargs ) for x in
                    resource.getjson( cls.routes['tasks'] % {'widget_id' : widget_id} ) 
                ]

    @resourcemethod
    def list( cls, widget_id, **kwargs ):
        resource = kwargs['resource']
        return [ cls( x['widget'], **kwargs ) for x in
                    resource.getjson( cls.routes['list'] )
               ]

    @resourcemethod
    def get( cls, widget_id, **kwargs ):
        resource = kwargs['resource']
        data = resource.getjson( self.routes['get'] % {'widget_id' : widget_id } )
        return cls( data, **kwargs )

