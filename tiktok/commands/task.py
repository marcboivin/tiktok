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
    pprint.pprint( task )

def addlog( args, config, **kwargs ):

    args['start'] = datetime.datetime.strptime( args['start'], config['datetime_format'] )

    if 'duration' in args:
        args['duration'] = kwargs['duration_parser'].parse( args['duration'] )
    if 'end' in args:
        args['end'] = datetime.datetime.strptime( args['end'], config['datetime_format'] )

    task = Task.get( int( args['tasknum'] ) )
    task.addlog( **args )

