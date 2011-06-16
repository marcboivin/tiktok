from tiktok.model.widget import Widget
from tiktok.model.task import Task

from tiktok.lib.resources import get_resource

import pprint
import sys

def tasks( args ):

    widget = Widget( get_resource() )
    tasks = widget.tasks( args['widget_id'] )
    for task in tasks:
        print Task.format( task )

def list( args ):

    widget = Widget( get_resource() )
    widgets = widget.list()
    for widget in widgets:
       print Widget.format( widget )

