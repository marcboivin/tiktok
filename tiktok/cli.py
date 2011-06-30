#!/usr/bin/env python2
import pprint
import sys
import argparse
import os.path

from pkg_resources import resource_stream
from ConfigParser import RawConfigParser

import tiktok.config
from tiktok import model
from tiktok import commands

from lib.resources import TikTakResource
from lib import durations
from lib.prettyprinter import PrettyPrinter

CONFIG_FILE = '~/.tiktok/config.cfg'

def load_config( path ):

    config = {}

    defaults = resource_stream('tiktok.config', 'defaults.cfg')
    parser = RawConfigParser(allow_no_value = True)
    parser.readfp( defaults, 'defaults.cfg' )

    if os.path.exists( path ):
        parser.read( path )

    sections = [ x for x in parser.sections() if x != 'general' ]

    config.update( dict( parser.items('general') ) )
    for section in sections:
        config[section] = dict( parser.items( section ) )

    return config

def initialize( config ):

    resource = TikTakResource( config['url'], config['username'], config['password'] )
    resource.login()

    d_format = config['duration_format']

    d_items = {
        'alarmclock' : (durations.ClockParser, durations.ClockFormat),
        'decimal' : (durations.DecimalParser, durations.DecimalFormat),
        'standard' : (durations.StandardParser, durations.StandardFormat),
        'compact' : (durations.CompactParser, durations.CompactFormat),
        'colons' : (durations.ColonParser, durations.ColonFormat)
    }

    d_config = {}

    if d_format in ('alarmclock', 'decimal'):
        d_config = {
            'parser' : d_items[d_format][0](),
            'formatter' : d_items[d_format][1]()
        }
    else:
        d_config = {
            'parser' : d_items[d_format][0](
                int( config['days_in_week'] ),
                int( config['minutes_in_day'] )
            ),
            'formatter' : d_items[d_format][1](
                int( config['days_in_week'] ),
                int( config['minutes_in_day'] )
            ),
        }

    utils = {
        'resource' : resource,
        'duration_parser' : d_config['parser'],
        'duration_formatter' : d_config['formatter'],
        'datetime_format' : config['datetime_format'],
        'printer' : PrettyPrinter( d_config['formatter'], config['datetime_format'] ),
    }

    model.basemodel.set_utils( utils )
    tiktok.config.set_utils( utils )

def dispatch( command, action, args, config ):

    module = vars( commands )[ command ]
    func = getattr( module, action )
    func( args, config, **tiktok.config.get_utils() )

def argparser():

    parser = argparse.ArgumentParser(
            description = 'CLI app for interacting with TikTak.',
            prog='tiktok',
            formatter_class = argparse.ArgumentDefaultsHelpFormatter
            )

    parser.add_argument('-c', '--config', default = CONFIG_FILE , dest='configfile')
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

    addlog = task.add_parser(
            'addlog',
            description = 'add a log of a work period',
            #aliases = ['al']
            )
    addlog.add_argument( 'tasknum')
    addlog.add_argument( 'start' )
    addlog.add_argument( '--end', '-e', dest ='end', default = argparse.SUPPRESS )
    addlog.add_argument( '--duration', '-d', dest = 'duration', default = argparse.SUPPRESS )
    addlog.add_argument( '--log', '-l', dest = 'log', default = argparse.SUPPRESS )

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
    argparser().parse_args(['--help'])
    sys.exit(1)

def main():

    parser = argparser()
    args = vars( parser.parse_args() )

    command = args.pop('command')
    action = args.pop('action')
    configfile = os.path.expanduser( args.pop('configfile') )

    config = load_config( configfile )

    if not command:
        error("no command found")
    if not action:
        error("no action for command")

    required = ['url', 'username', 'password']
    for key in required:
        if key in args:
            config[key] = args.pop(key)

    missing = [x for x in required if not config.get(x) ]
    if len(missing) > 0:
        msg = "Missing arguments : %s\n" % ', '.join(missing)
        msg += "Please add them to the config file or pass them as arguments to the command line\n"
        error(msg)

    initialize( config )

    dispatch( command, action, args, config )

if __name__ == '__main__':
    main()

