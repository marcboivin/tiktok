from tiktok.model.task import Task
import pprint

def process_command( resource, info ):

    task = Task( resource )
    command, (opts, args) = info

    if command == 'show':

        if len(args) == 0:
            print "ERROR: please give a task number"
            sys.exit(1)
        task_id = int(args[0])

        pprint.pprint( task.show( task_id ) )

    elif command == 'start':

        if len(args) == 0:
            print "ERROR: please give a task number"
            sys.exit(1)
        task_id = int(args[0])

        task.start( task_id )

    elif command == 'stop':

        if len(args) == 0:
            print "ERROR: please give a task number"
            sys.exit(1)
        task_id = int(args[0])

        task.stop( task_id )

    elif command == 'current':

        pprint.pprint( task.current() )

