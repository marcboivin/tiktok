from tiktok.model.widget import Widget
from tiktok.model.task import Task

import pprint
import sys

def tasks( args, helpers ):

    tasks = Widget.tasks( args['widget_id'] )
    for task in tasks:
        helpers.pprint( task, helpers.config['task']['format'] )

def list( args, helpers ):

    for widget in Widget.list():
        helpers.pprint( widget, helpers.config['widget']['format'] )

def tasktable( args, helpers ):

    widgets = Widget.list()
    lines = []
    printer = helpers.printer
    widget_fmt = helpers.config['widget']['format']
    task_fmt = helpers.config['task']['format']

    for widget in widgets:
        lines.append( (
            'widget',
            widget['id'],
            printer.format( widget, widget_fmt )
        ) )

        lines.extend( (
            (   'task',
                widget['id'],
                task['task_num'],
                printer.format( task, task_fmt )
            )   for task in widget.tasks( widget['id'] )
        ) )

    for line in lines:
        print "\t".join( ( unicode(x) for x in line ) )

