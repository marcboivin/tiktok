from tiktok.model.widget import Widget
from tiktok.model.task import Task

import pprint
import sys

def tasks( args, config, **kwargs ):

    printer = kwargs['printer']

    tasks = Widget.tasks( args['widget_id'] )
    for task in tasks:
        printer.pprint( task, config['task']['format'] )

def list( args, config, **kwargs ):
    
    printer = kwargs['printer']

    for widget in Widget.list():
        printer.pprint( widget, config['widget']['format'] )

