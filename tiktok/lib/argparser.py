import argparse

def argparser( configfile ):

    parser = argparse.ArgumentParser(
            description = 'CLI app for interacting with TikTak.',
            prog='tiktok',
            formatter_class = argparse.ArgumentDefaultsHelpFormatter
            )

    parser.add_argument('-c', '--config', default = configfile, dest='configfile')
    parser.add_argument('-u', '--username', dest='username', default = argparse.SUPPRESS )
    parser.add_argument('-p', '--password', dest='password', default = argparse.SUPPRESS )
    parser.add_argument('--url', dest='url', default = argparse.SUPPRESS )

    commands = parser.add_subparsers(dest='command')

    #Tasks
    task_main = commands.add_parser(
            'task',
            #aliases = ['t', 'ta'],
            description = 'Task related commands'
            )

    task = task_main.add_subparsers(dest='action')

    show = task.add_parser(
            'show',
            description = 'Show detailed information about a task',
            #aliases = ['sh']
            )
    show.add_argument('tasknum', type = int )

    start = task.add_parser(
            'start',
            description = 'Start working on a task',
            #aliases = ['sta']
            )
    start.add_argument( 'tasknum', type = int )

    stop = task.add_parser(
            'stop',
            description = 'Stop working on current task',
            #aliases = ['sto']
            )
    stop.add_argument(
            '-l',
            '--log',
            default = argparse.SUPPRESS
            )

    current = task.add_parser(
            'current',
            description = 'Information about the task you are working on right now',
            #aliases = ['cu']
            )

    updatelog = task.add_parser(
            'updatelog',
            description = 'log a description of the work you are doing for the current task',
            #aliases = ['ul']
            )
    updatelog.add_argument( 'description' )

    cancel = task.add_parser(
            'cancel',
            description = 'cancel the task you are working on right now'
            #aliases = ['cl']
            )

    log = commands.add_parser(
            'log',
            #aliases = ['l', 'lo'],
            description = 'Log related commands'
            ).add_subparsers( dest='action' )

    addlog = log.add_parser(
            'add',
            description = 'add a log of a work period',
            #aliases = ['al']
            )
    addlog.add_argument( 'tasknum' )
    addlog.add_argument( '--start', '-s', dest = 'start', required = True )
    addlog.add_argument( '--end', '-e', dest ='end', default = argparse.SUPPRESS )
    addlog.add_argument( '--duration', '-d', dest = 'duration', default = argparse.SUPPRESS )
    addlog.add_argument( '--log', '-l', dest = 'log', default = argparse.SUPPRESS )

    create = task.add_parser(
            'create',
            description = 'create a new task'
            #aliases = ['cr']
        )
    create.add_argument( '--name', '-n', dest = 'name', required = True )
    create.add_argument( '--project', '-p', dest = 'project', required = True )
    create.add_argument( '--description', '-d', dest = 'description', default = argparse.SUPPRESS )
    create.add_argument( '--estimate', '-e', dest = 'duration', default = argparse.SUPPRESS )
    create.add_argument( '--duedate', '-D', dest = 'due_at', default = argparse.SUPPRESS )
    create.add_argument( '--users', '-u', dest = 'users', nargs = '+', default = argparse.SUPPRESS )
    create.add_argument( '--start', '-s', dest = 'start', action = 'store_const', const = True, default = False )

    interactive = task.add_parser(
            'interactive',
            description = 'create a task interactively'
            #aliases = ['in']
        )
    interactive.add_argument( '--name', '-n', dest = 'name', default = argparse.SUPPRESS )
    interactive.add_argument( '--project', '-p', dest = 'project', default = argparse.SUPPRESS )
    interactive.add_argument( '--description', '-d', dest = 'description', default = argparse.SUPPRESS )
    interactive.add_argument( '--estimate', '-e', dest = 'duration', default = argparse.SUPPRESS )
    interactive.add_argument( '--duedate', '-D', dest = 'due_at', default = argparse.SUPPRESS )
    interactive.add_argument( '--users', '-u', dest = 'users', nargs = '+', default = argparse.SUPPRESS )
    interactive.add_argument( '--start', '-s', dest = 'start', action = 'store_const', const = True, default = False )

    cancel = task.add_parser(
            'cancel',
            description = 'cancel the task you are working on right now'
            #aliases = ['cl']
            )
            
    search = task.add_parser(
            'search',
            description = 'search keyword in the task database'
            )
            
    search.add_argument( 'keyword')

    #Widget
    widget_main = commands.add_parser(
            'widget',
            description = 'Widget commands',
            #aliases = ['wi']
            )
    widget = widget_main.add_subparsers(dest='action')

    tasks = widget.add_parser(
            'tasks',
            description = 'List of tasks inside a widget',
            #aliases = ['ta']
            )
    tasks.add_argument('widget_id', type = int )

    w_list = widget.add_parser(
            'list',
            description = 'List of available widgets',
            #aliases = ['li']
            )

    w_tasktable = widget.add_parser(
            'tasktable',
            description = 'print a parse-friendly list of widgets and their tasks'
            )

    #Project
    project = commands.add_parser(
            'project',
            description = 'Project commands',
            #aliases = ['p']
            ).add_subparsers( dest = 'action' )

    p_list = project.add_parser(
            'list',
            description = 'List of available projects'
            #aliases = ['li']
            )

    #User
    user = commands.add_parser(
            'user',
            description = 'User commands',
            #aliases = ['u']
            ).add_subparsers( dest = 'action' )

    u_list = user.add_parser(
            'list',
            description = 'List of available users'
            #aliases = ['li']
            )
    url = commands.add_parser(
            'url',
            description = 'Clock time based on a system URL (Very Libeo specific)',
            #aliases = ['u']
            ).add_subparsers( dest = 'action' )
            
    clock = url.add_parser(
            'clock',
            description = 'List of available users'
            #aliases = ['li']
            )
    
    clock.add_argument('source_url')
            
    clock.add_argument( '--date', '-d', dest = 'date', default = argparse.SUPPRESS )
    clock.add_argument( '--start_time', '-stt', dest = 'start_time', default = argparse.SUPPRESS )
    clock.add_argument( '--stop_time', '-spt', dest = 'stop_time', default = argparse.SUPPRESS )
    
    live = url.add_parser(
            'live',
            description = 'List of available users'
            #aliases = ['li']
            )
            
    live.add_argument('source_url')
    
    return parser


