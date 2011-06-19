from tiktok.model.task import Task
import pprint

def show( args ):

    task = Task.get( args['tasknum'] )
    pprint.pprint( task )

def start( args ):

    task = Task.get( args['tasknum'] )
    task.start()

def stop( args ):

    Task.stop()

def current( args ):

    task = Task.current()
    pprint.pprint( task )

