from basemodel import BaseModel

class Task( BaseModel ):

    fmt = u"#%(task_num)d %(name)s - %(w_hour)02d:%(w_min)02d / %(d_hour)02d:%(d_min)02d"

    routes = {
        'show' : '/tasks/%(tasknum)d/edit',
        'start' : '/tasks/start_work_ajax/%(taskid)d.js',
        'stop' : '/tasks/stop_work_ajax/%(taskid)d.js',
        'current' : '/tasks/update_sheet_info',
    }

    def show(self, tasknum):
        return self.resource.getjson( self.routes['show'] % {'tasknum' : tasknum} )['task']

    def start(self, tasknum):
        task = self.show( tasknum )
        task_id = task['id']
        self.resource.post( self.routes['start'] % {'taskid' : task_id} )

    def stop(self, tasknum):
        task = self.show( tasknum )
        task_id = task['id']
        self.resource.post( self.routes['stop'] % {'taskid' : task_id} )

    def current(self):
        return self.resource.postjson( self.routes['current'] )['sheet']

    @classmethod
    def format( cls, task ):
        data = {'w_hour' : task['worked_minutes'] / 60,
                'w_min' : task['worked_minutes'] % 60,
                'd_hour' : task['duration'] / 60,
                'd_min' : task['duration'] % 60 }
        data.update( task )
        return cls.fmt % data

