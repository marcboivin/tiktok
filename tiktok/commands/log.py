from tiktok.model.log import Log
from tiktok.model.task import Task
import pprint
import datetime

def add( args, config, **kwargs ):

    if 'duration' in kwargs and 'end' in kwargs:
        raise ValueError("please use either duration OR end, not both")
    elif not( 'duration' or 'end' in kwargs ):
        raise ValueError("duration OR end is required")

    for key in ( x for x in ('start', 'end') if x in args ):
        try:
            args[key] = datetime.datetime.strptime( args[key], config['datetime_format'] )
        except ValueError:
            time = datetime.datetime.strptime( args[key], config['time_format'] ).time()
            args[key] = datetime.datetime.combine( datetime.date.today(), time )

    if 'duration' in args:
        duration = kwargs['duration_parser'].parse( args['duration'] )
    elif 'end' in args:
        duration = args['end'] - args['start']

    args['duration'] = duration

    task = Task.get( int( args['tasknum'] ) )

    log = Log.add( task['id'], **args )
    kwargs['printer'].pprint( log, config['log']['format'] )

