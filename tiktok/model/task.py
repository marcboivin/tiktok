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
        'addlog' : '/tasks/add_log/%(task_id)d.json',
        'savelog' : '/tasks/save_log/%(worklog_id)d.json',
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

    def addlog( self, **kwargs ):
        """
        kwargs:
            start : datetime, when work started
            duration : timedelta, time spent working
            end : datetime, when work stopped
            log : commentary (description) of the work period
        """

        #Validation
        if 'start' not in kwargs:
            raise ValueError("start is required")
        elif 'duration' in kwargs and 'end' in kwargs:
            raise ValueError("please use either duration OR end, not both")
        elif not( 'duration' or 'end' in kwargs ):
            raise ValueError("duration OR end is required")

        data = {
            'started_at' : kwargs['start'].strftime( self.datetime_format ),
            'body' : kwargs.get('log', '')
        }

        #Transform data that will be sent to tiktak
        if 'duration' in kwargs:
            data['duration'] = self.duration_formatter.format( kwargs['duration'] )
        elif 'end' in kwargs:
            duration = kwargs['end'] - kwargs['start']
            data['duration'] = self.duration_formatter.format( duration )

        data = dict( ('work_log[%s]' % key, value) for ( key, value ) in data.items() )

        #Send request
        newlog = self.resource.postjson(
            self.routes['addlog'] % {'task_id' : self['id'] },
            data
        )

        newlog = newlog['work_log']
        return newlog
