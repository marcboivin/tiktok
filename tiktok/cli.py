#!/usr/bin/env python2
import pprint
import sys
from tiktok import commands
from tiktok.commands import widget, task

from tiktok.lib.resource import TikTakResource

from opts import Parser, Option, Command

parser = Parser(
    description="TikTak CLI interface", 
    options = {
        'username' : Option('u', 'username'),
        'password' : Option('p', 'password'),
    },
    commands = {
        'task' : Command(
            allow_abbreviated_commands = True,
            allow_abbreviated_options = True,
            short_description="Task commands",
            commands = {
                'show' : Command(
                    short_description="Show detailed information about a task",
                    takes_arguments = True
                ),
                'start' : Command(
                    short_description="Start working on a task",
                    takes_arguments = True
                ),
                'stop' : Command(
                    short_description="Stop working on a task",
                    takes_arguments = True
                ),
                'current' : Command(
                    short_description="Get info aboue the task you are working on right now",
                    takes_arguments = False
                )
            }
        ),
        'widget' : Command(
            short_description = 'Widget commands',
            allow_abbreviated_commands = True,
            allow_abbreviated_options = True,
            commands = {
                'tasks' : Command(
                    short_description="list all tasks in widget",
                    takes_arguments = True
                ),
                'list' : Command(
                    short_description="list all available widgets",
                    takes_arguments = False
                ),
            }
        ),
    }
)

def main():

    opts, args = parser.evaluate( sys.argv[1:] )

    username = opts.pop('username', 'gregory')
    password = opts.pop('password', '1qaz')

    resource = TikTakResource( "http://eric.lan.org:3000", username, password)
    resource.login()

    if len(opts) == 0:
        print "ERROR: no command given"
        sys.exit(1)

    command, (sub_opts, sub_args) = opts.items()[0]

    #mod = getattr( commands, command )
    #if not mod:
    #    print "ERROR: processor not found"
    #    sys.exit(1)
    #mod.process_command( resource, options[0] )
    
    if command == 'widget':
        widget.process_command( resource, sub_opts.items()[0] )
    elif command == 'task':
        task.process_command( resource, sub_opts.items()[0] )

if __name__ == '__main__':
    main()

