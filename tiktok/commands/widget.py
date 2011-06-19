from tiktok.model.widget import Widget
from tiktok.model.task import Task

import pprint
import sys

def tasks( args ):

    tasks = Widget.tasks( args['widget_id'] )
    for task in tasks:
        print task.format()

def list( args ):

    for widget in Widget.list():
        print widget.format()

