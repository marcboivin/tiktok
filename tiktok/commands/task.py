from tiktok.model.task import Task
import pprint
import datetime

def show( args, config, **kwargs ):

    task = Task.get( args['tasknum'] )
    pprint.pprint( task )

def start( args, config, **kwargs ):

    task = Task.get( args['tasknum'] )
    task.start()

def updatelog( args, config, **kwargs ):

    Task.updatelog( args['description'] )

def stop( args, config, **kwargs ):

    if 'log' in args:
        updatelog( {'description' :  args['log']}, config )

    Task.stop()

def current( args, config, **kwargs ):

    task = Task.current()

    if task:
        kwargs['printer'].pprint( task, config['task']['format'] )
        print "Description: %s" % task['body']

def addlog( args, config, **kwargs ):

    for key in ( x for x in ('start', 'end') if x in args ):
        try:
            args[key] = datetime.datetime.strptime( args[key], config['datetime_format'] )
        except ValueError:
            time = datetime.datetime.strptime( args[key], config['time_format'] ).time()
            args[key] = datetime.datetime.combine( datetime.date.today(), time )

    if 'duration' in args:
        args['duration'] = kwargs['duration_parser'].parse( args['duration'] )

    task = Task.get( int( args['tasknum'] ) )
    task.addlog( **args )

