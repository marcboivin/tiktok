from tiktok.model.task import Task
import pprint
import datetime

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

def create_interactive( args, config ):

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
        users = raw_input( "User assignments (space seperated list of usernames, blank for nobody): ").strip()
        users = users.split(" ")
        if len( users ) > 0:
            args['users'] = users

    start = raw_input( "Should I start the task right now ? [y/N]: ").strip()
    if start.lower() == 'y':
        args['start'] = True

    return args

def create( args, config, **kwargs ):

    interactive = args.pop('interactive')
    start = args.pop('start')
    creator_id = User.find_id_by_username( config['username'] )

    duration_parser = kwargs['duration_parser']
    date_format = config['date_format']

    if interactive:
        args = create_interactive( args, config )

    #Parse duration and date
    if 'duration' in args:
        args['duration'] = duration_parser.parse( args['duration'] )
    if 'due_at' in args:
        args['due_at'] = datetime.datetime.strftime( args['due_at'], date_format )

    #Transform project name into project id
    project_id = Project.find_id_by_name( args.pop('project') )
    if not project_id:
        print "ERROR: project does not exist (project name not found)"
        sys.exit( 1 )
    args['project_id'] = project_id

    #Transform usernames into user ids
    user_ids = [ creator_id ]
    if 'users' in args:
        for username in args['users']:
            user_id = User.find_id_by_username( username )
            if not user_id:
                print "ERROR: user does not exist (username not found)"
                sys.exit( 1 )
            user_ids.append( user_id )
        args.pop('users')
        args['user_ids'] = user_ids

    task = Task.create( args )

    if start:
        task.start()

    kwargs['printer'].pprint( task, config['task']['format'] )

