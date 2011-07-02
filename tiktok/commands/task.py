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

def cancel( args, config, **kwargs ):

    Task.cancel()

