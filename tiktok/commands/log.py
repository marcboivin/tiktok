import datetime

from tiktok.model.log import Log
from tiktok.model.task import Task

def add( args, helpers ):

    if 'duration' in args and 'end' in args:
        raise ValueError("please use either duration OR end, not both")
    elif not( 'duration' in args or 'end' in args ):
        raise ValueError("duration OR end is required")

    for key in ( x for x in ('start', 'end') if x in args ):
        try:
            args[key] = helpers.datetime.parse( args[key] )
        except ValueError:
            time = datetime.datetime.strptime( args[key], helpers.config['time_format'] ).time()
            args[key] = datetime.datetime.combine( datetime.date.today(), time )

    if 'duration' in args:
        duration = helpers.duration.parse( args['duration'] )
    elif 'end' in args:
        duration = args['end'] - args['start']

    args['duration'] = duration

    task = Task.get( int( args['tasknum'] ) )

    log = Log.add( task['id'], **args )
    helpers.pprint( log, helpers.config['log']['format'] )

