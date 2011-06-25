from basemodel import BaseModel, resourcemethod

class Task( BaseModel ):

    fmt = u"#%(task_num)d %(name)s - %(w_hour)02d:%(w_min)02d / %(d_hour)02d:%(d_min)02d"

    routes = {
        'get' : '/tasks/edit/%(tasknum)d.json',
        'start' : '/tasks/start_work_ajax/%(taskid)d.js',
        'stop' : '/tasks/stop_work_ajax',
        'current' : '/tasks/update_sheet_info.json',
        'updatelog' : '/tasks/updatelog.json',
    }

    def __init__(self, *args, **kwargs):

        BaseModel.__init__(self, *args, **kwargs)
        data = {'w_hour' : self['worked_minutes'] / 60,
                'w_min' : self['worked_minutes'] % 60,
                'd_hour' : self['duration'] / 60,
                'd_min' : self['duration'] % 60 }
        self.update(data)


    @resourcemethod
    def get( cls, resource, tasknum ):

        return cls( resource.getjson( cls.routes['get'] % {'tasknum' : tasknum} )['task'] )

    @resourcemethod
    def current( cls, resource ):

        task = None
        data = resource.postjson( cls.routes['current'] )

        if data:
            task = cls( data['sheet'], resource )

        return task

    def start(self):

        self.resource.post( self.routes['start'] % {'taskid' : self['id'] } )

    @resourcemethod
    def stop( cls, resource ):

        resource.post( cls.routes['stop'] )

    @resourcemethod
    def updatelog( cls, resource, text ):

        resource.post( cls.routes['updatelog'], {'text' : text} )

