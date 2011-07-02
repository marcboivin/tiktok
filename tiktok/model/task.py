import datetime
from basemodel import BaseModel, resourcemethod
from tiktok.lib.durations import secs_to_timedelta

class Task( BaseModel ):

    routes = {
        'get' : '/tasks/edit/%(tasknum)d.json',
        'start' : '/tasks/start_work_ajax/%(task_id)d',
        'stop' : '/tasks/stop_work_ajax',
        'current' : '/tasks/update_sheet_info.json',
        'updatelog' : '/tasks/updatelog.json',
        'cancel' : '/tasks/cancel_work_ajax'
    }

    def __init__(self, *args, **kwargs):

        BaseModel.__init__(self, *args, **kwargs)
        data = {
            'duration' : secs_to_timedelta( self['duration'] * 60 ),
            'worked' : secs_to_timedelta( self['worked_minutes'] * 60 ),
        }
        self.update(data)
        self.pop( 'worked_minutes' )


    @resourcemethod
    def get( cls, tasknum, **kwargs ):
        resource = kwargs['resource']

        return cls( resource.getjson( cls.routes['get'] % {'tasknum' : tasknum} )['task'], **kwargs )

    @resourcemethod
    def current( cls, **kwargs ):
        resource = kwargs['resource']

        task = None
        data = resource.postjson( cls.routes['current'] )

        if data:
            data = data['sheet']
            data['sheet_id'] = data.pop('id')
            data['id'] = data.pop('task_id')
            data['name'] = data.pop('task_name')
            task = cls( data, **kwargs )

        return task

    def start(self):

        self.resource.post( self.routes['start'] % {'task_id' : self['id'] } )

    @resourcemethod
    def stop( cls, **kwargs ):
        resource = kwargs['resource']

        resource.post( cls.routes['stop'] )

    @resourcemethod
    def updatelog( cls, text, **kwargs ):
        resource = kwargs['resource']

        resource.post( cls.routes['updatelog'], {'text' : text} )

    @resourcemethod
    def cancel( cls, **kwargs ):
        resource = kwargs['resource']

        resource.post( cls.routes['cancel'] )
