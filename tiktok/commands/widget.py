from tiktok.model.widget import Widget
from tiktok.model.task import Task

import pprint
import sys

def process_command( resource, info ):

    widget = Widget( resource )

    command, (opts, args) = info

    if command == 'tasks':

        if len(args) == 0:
            print "ERROR: please give a task number"
            sys.exit(1)

        widget_id = int(args[0])
        tasks = widget.tasks( widget_id )
        for task in tasks:
            print Task.format( task )

    elif command == 'list':

        widgets = widget.list()
        for widget in widgets:
           print Widget.format( widget )
            

