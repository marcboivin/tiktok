#!/usr/bin/env python2
import pprint
import sys
import argparse

from tiktok.lib.resources import init_resource

from tiktok import commands

config = {
    'url' : 'http://eric.lan.org:3000'
}

def dispatch( command, action, args ):

    module = vars( commands )[ command ]
    func = getattr( module, action )
    func( args )

def argparser():

    parser = argparse.ArgumentParser( 
            description = 'CLI app for interacting with TikTak.',
            prog='tiktok' 
            )

    parser.add_argument('-u', '--username', required = True, dest='username' )
    parser.add_argument('-p', '--password', required = True, dest='password' )

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
    stop.add_argument('-l', '--log', nargs = '+' )

    current = task.add_parser(
            'current',
            description = 'Information about the task you are working on right now',
            #aliases = ['cu']
            )

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

    return parser

def error(message):
    print "ERROR: ", message
    sys.exit(1)

def main():

    parser = argparser()
    args = vars( parser.parse_args() )

    command = args.pop('command')
    action = args.pop('action')

    if not command:
        error("no command found")
    if not action:
        error("no action for command")

    for key in ['username', 'password']:
        if key in args:
            config[key] = args[key]

    init_resource( config['url'], config['username'], config['password'] )

    dispatch( command, action, args )

if __name__ == '__main__':
    main()

