# -*- coding: utf-8 -*-
"""
TenantBase Backend
Key-value storage server implemented in SQlite and memmcached.
"""
from os import system
import sys
import logging
import argparse
import sqlite3
from pymemcache.client import Client

# globals
LOG = logging.getLogger()
LOG.setLevel(logging.INFO)
DESCRIPTION = 'TenantBase -- sqlite+memcached service.'
SERVE_HELP = 'starts database.sqlite.'
SHOW_HELP = 'displays all stored key-value pairs.'
HOST = 'localHOST'
PORT = 11211
START_MEMCACHED = 'memcached -d -vv'

# functions
def run_command(command):
    """Wrapper around os.system, will raise exception if command did not exit cleanly"""
    exit_code = system(command)
    if exit_code != 0:
        raise Exception('Cannot execute command: %s. Did you install it?' % command)

def parse_args(args):
    """parses command line arguments"""
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('-s', '--serve', type=str, dest='serve',
                        help=SERVE_HELP)
    parser.add_argument('-sh', '--show', type=str, dest='show',
                        help=SHOW_HELP)

    return parser.parse_args(args)

# main
def main(argv=None):
    """main function"""
    LOG.info('tenant-base main starting')

    parser = parse_args(argv)

    if parser.serve:
        LOG.info('Starting memcached server')
        print('Starting memcached server')
        try:
            run_command(START_MEMCACHED)
            LOG.info('Memcached server listening on: %s:%s', HOST, str(PORT))
            print('Memcached server listening on: {}:{}'.format(HOST, PORT))

        except (Exception, ConnectionRefusedError) as error:
            LOG.error('Error: %s', error)
            sys.exit(1)

    elif parser.show:
        print('showing')

    else:
        print('Run python main.py -h for help')



if __name__ == '__main__':
    main()
