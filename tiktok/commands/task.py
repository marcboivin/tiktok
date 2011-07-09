from tiktok.model.task import Task
from tiktok.model.user import User
from tiktok.model.project import Project

import pprint
import datetime
import sys

def show( args, config, **kwargs ):

    task = Task.get( args['tasknum'] )
    pprint.pprint( task )

def start( args, config, **kwargs ):

    task = Task.get( args['tasknum'] )
    task.start()

def updatelog( args, config, **kwargs ):

    Task.updatelog( args['description'] )

def stop( args, config, **kwargs ):

    if 'log' in args:
        updatelog( {'description' :  args['log']}, config )

    Task.stop()

def current( args, config, **kwargs ):

    task = Task.current()

    if task:
        kwargs['printer'].pprint( task, config['task']['format'] )
        print "Description: %s" % task['body']

def addlog( args, config, **kwargs ):

    for key in ( x for x in ('start', 'end') if x in args ):
        try:
            args[key] = datetime.datetime.strptime( args[key], config['datetime_format'] )
        except ValueError:
            time = datetime.datetime.strptime( args[key], config['time_format'] ).time()
            args[key] = datetime.datetime.combine( datetime.date.today(), time )

    if 'duration' in args:
        args['duration'] = kwargs['duration_parser'].parse( args['duration'] )

    task = Task.get( int( args['tasknum'] ) )
    task.addlog( **args )

def cancel( args, config, **kwargs ):

    Task.cancel()

def create( args, config, **kwargs ):

    duration_parser = kwargs['duration_parser']
    date_format = config['date_format']

    start = args.pop('start')

    creator_id = User.find_id_by_username( config['username'] )

    #Parse duration and date
    if 'duration' in args:
        args['duration'] = duration_parser.parse( args['duration'] )
    if 'due_at' in args:
        args['due_at'] = datetime.datetime.strptime( args['due_at'], date_format )

    #Transform project name into project id
    found = Project.find_id_by_name( args.pop( 'project') )
    if len( found ) == 0:
        print "ERROR: project does not exist (project name not found)"
        sys.exit( 1 )
    elif len ( found ) > 1:
        print "ERROR: more than one project with the same name (try putting in a longer project name for searching)"
        sys.exit( 1 )

    args['project_id'] = found[0]

    #Transform usernames into user ids
    user_ids = [ creator_id[0] ]

    for username in args.pop( 'users', '' ):

        user_id = User.find_id_by_username( username )

        if len( user_id ) == 0:
            print "ERROR: no user found for username %s" % username
            sys.exit( 1 )
        elif len( user_id ) > 1:
            print "ERROR: more than one user found with username '%s' (try a longer username)"
            sys.exit( 1 )

        if not user_id:
            print "ERROR: user does not exist (username not found)"
            sys.exit( 1 )

        user_ids.append( user_id[0] )

    user_ids = list( set( user_ids ) )

    args['user_ids'] = user_ids

    task = Task.create( **args )

    if start:
        task.start()

    kwargs['printer'].pprint( task, config['task']['format'] )

def interactive( args, config, **kwargs ):

    formats = {
        'standard' : '1w 2d 3h 4m',
        'compact' : '1w2d3h4m',
        'colons' : '1:2:3:4',
        'alarmclock' : '42:34',
        'decimal' : '12.95',
    }

    d_format = formats[ config['duration_format'] ]

    #Task name
    if 'name' not in args:
        name = ''
        while name == '':
            name = raw_input( "Task name: " ).strip()
        args['name'] = name

    if 'project' not in args:
        project = ''
        while project == '':
            project = raw_input( "Project name: ").strip()

            found = Project.find_id_by_name( project )
            if len( found ) == 0:
                print "Project name not found. Please try again"
                project = ''
            elif len( found ) > 2:
                print "More than one project with the same name. Please enter a longer project name"
                project = ''

        args['project'] = project

    if 'description' not in args:
        description = raw_input( "Description (leave blank for nothing):" ).strip()
        if description != '':
            args['description'] = description

    if 'duration' not in args:
        duration = raw_input( "Duration (%s) (leave blank for nothing): " % d_format ).strip()
        if duration != '':
            args['duration'] = duration

    if 'due_at' not in args:
        due_at = raw_input( "Due date (%s) (leave blank for nothing): " % config['date_format'] ).strip()
        if due_at != '':
            args['due_at'] = due_at

    if 'users' not in args:

        retry = True
        while retry:

            retry = False

            users = raw_input( "User assignments (space seperated list of usernames, blank for nobody): ").strip()
            users = [ u for u in users.split(" ") if u != '' ]

            for user in users:

                found = User.find_id_by_username( user )
                if len( found ) == 0:
                    print "No user with username '%s' found. please try again" % user
                    retry = True
                elif len( found ) > 2:
                    print "More than one user with '%s' in their username. Please try a longer username" % user
                    retry = True

        if len( users ) > 0:
            args['users'] = users

    start = raw_input( "Should I start the task right now ? [y/N]: ").strip()
    if start.lower() == 'y':
        args['start'] = True

    create( args, config, **kwargs )

