from tiktok.model.task import Task
from tiktok.lib.resources import resource
import pprint

def show( args ):

    task = Task( resource )
    task_id = int(args[0])
    pprint.pprint( task.show( task_id ) )


def start( args ):

    task = Task( resource )
    task_id = int(args[0])
    task.start( task_id )


def stop( args ):

    task = Task( resource )
    task_id = int(args[0])
    task.stop( task_id )


def current( args ):

    task = Task( resource )
    pprint.pprint( task.current() )

