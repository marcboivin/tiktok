from basemodel import BaseModel, resourcemethod
from tiktok.lib.durations import secs_to_timedelta
from tiktok.lib.datetimes import parse_isoutc

class Log( BaseModel ):

    routes = {
            'add' : '/tasks/add_log/%(task_id)d.json',
            }

    def __init__( self, *args, **kwargs ):

        BaseModel.__init__( self, *args, **kwargs )
        self['duration'] = secs_to_timedelta( self['duration'] )
        self['start'] = parse_isoutc( self.pop('started_at') )
        self['end'] = self['start'] + self['duration']
        del self['paused_duration']
        del self['scm_changeset_id']

    @resourcemethod
    def add( cls, context, task_id, **kwargs ):
        """
        kwargs:
            start : datetime, when work started
            duration : timedelta, time spent working
            end : datetime, when work stopped
            log : commentary (description) of the work period
        """
        resource = context.resource

        data = {
            'started_at' : context.datetime.format( kwargs['start'] ),
            'body' : kwargs.get('log', ''),
            'duration' : context.duration.format( kwargs['duration'] ),
        }

        data = dict( ('work_log[%s]' % key, value) for ( key, value ) in data.items() )

        #Send request
        newlog = resource.postjson(
            cls.routes['add'] % {'task_id' : task_id },
            data
        )

        newlog = newlog['work_log']
        return cls( newlog, context )
