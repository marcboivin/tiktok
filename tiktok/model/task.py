import datetime
from basemodel import BaseModel, resourcemethod
from tiktok.lib.durations import secs_to_timedelta

import pdb

import urllib

class Task( BaseModel ):

    routes = {
        'get' : '/tasks/edit/%(tasknum)d.json',
        'start' : '/tasks/start_work_ajax/%(task_id)d',
        'stop' : '/tasks/stop_work_ajax',
        'current' : '/tasks/update_sheet_info.json',
        'create' : '/tasks/create.json',
        'updatelog' : '/tasks/updatelog.json',
        'cancel' : '/tasks/cancel_work_ajax',
        'search' : '/work_logs/task_autocomplete.json',
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
    def get( cls, context, tasknum ):
        resource = context.resource
        data = resource.getjson( cls.routes['get'] % {'tasknum' : tasknum} )['task']
        return cls( data, context )

    @resourcemethod
    def current( cls, context ):
        resource = context.resource

        task = None
        data = resource.postjson( cls.routes['current'] )

        if data:
            data = data['sheet']
            data['sheet_id'] = data.pop('id')
            data['id'] = data.pop('task_id')
            data['name'] = data.pop('task_name')
            data['duration'] = data.pop('duration') / 60
            task = cls( data, context )

        return task

    def start( self ):

        self.resource.post( self.routes['start'] % {'task_id' : self['id'] } )

    @resourcemethod
    def stop( cls, context ):
        resource = context.resource
        resource.post( cls.routes['stop'] )

    @resourcemethod
    def updatelog( cls, context, text ):
        resource = context.resource
        resource.post( cls.routes['updatelog'], {'text' : text} )

    @resourcemethod
    def cancel( cls, context ):
        resource = context.resource
        resource.post( cls.routes['cancel'] )

    @resourcemethod
    def create( cls, context, **kwargs ):

        resource = context.resource

        data = [
            ( 'name' , kwargs['name'] ),
            ( 'description', kwargs.get('description', '') ),
            ( 'project_id', kwargs['project_id'] ),
            ( 'status', 0 ),
        ]

        #Ugh, I HATE task properties
        for (property_id, property_value) in context.task_properties:
            data.append( ( 'properties[%d]' % property_id, property_value ) )

        if 'duration' in kwargs:
            data.append(
                ( 'duration', context.duration.format( kwargs['duration'] ) )
            )
        if 'due_at' in kwargs:
            data.append(
                ( 'due_at', context.datetime.format( kwargs['due_at'] ) )
            )

        data = [ ('task[%s]' % key, value) for (key, value) in data ]

        for user_id in kwargs['user_ids']:
            data.extend( [
                ('users[]', user_id),
                ('assigned[]', user_id),
                ('notify[]', user_id),
            ] )

        newtask = resource.postjson( cls.routes['create'], data )
        newtask = newtask['task']

        return cls( newtask, context )
    
    @resourcemethod   
    def search( cls, context, **kwargs ):
        ressource = context.resource
        
        data = [
             ( 'term' , kwargs['keyword'] ),
        ]
        
        json_response = ressource.getjson( cls.routes['search'], data)
        
        return json_response
