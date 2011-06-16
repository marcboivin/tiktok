from tiktok.model.task import Task
from tiktok.lib.resources import get_resource
import pprint

def show( args ):

    task = Task( get_resource() )
    task_id = int(args[0])
    pprint.pprint( task.show( task_id ) )


def start( args ):

    task = Task( get_resource() )
    task_id = int(args[0])
    task.start( task_id )


def stop( args ):

    task = Task( get_resource() )
    task_id = int(args[0])
    task.stop( task_id )


def current( args ):

    task = Task( get_resource() )
    pprint.pprint( task.current() )

