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

