# -*- coding: utf-8 -*-
"""
TenantBase Backend
Key-value storage server implemented in SQlite and memmcached.
"""
from os import system
import sys
import logging
import argparse
from pymemcache.client import Client
import sqlite3

# globals
log = logging.getLogger()
log.setLevel(logging.INFO)
description = 'TenantBase -- sqlite+memcached service.'
serve_help = 'starts database.sqlite.'
show_help = 'displays all stored key-value pairs.'
host = 'localhost'
port = 11211
start_memcached = 'memcached -d -vv'

# functions
def run_command(command):
    """Wrapper around os.system, will raise exception if command did not exit cleanly"""
    exit_code = system(command)
    if exit_code is not 0:
        raise Exception('Cannot execute command: %s. Did you install it?' % command)

def parse_args(args):
    """parses command line arguments"""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-s', '--serve', type=str, dest='serve',
                        help=serve_help)
    parser.add_argument('-sh', '--show', type=str, dest='show',
                            help=show_help)

    return parser.parse_args(args)

# main
def main(argv=None):
    """main function"""
    log.info('tenant-base main starting')

    parser = parse_args(argv)

    if parser.serve:
        log.info('Starting memcached server')
        print('Starting memcached server')
        try:
            run_command(start_memcached)
            log.info('Memcached server listening on: %s:%s', host, str(port))
            print('Memcached server listening on: {}:{}'.format(host, port))

        except (Exception, ConnectionRefusedError) as error:
            log.error('Error: %s', error)
            sys.exit(1)

    elif parser.show:
        print('showing')

    else:
        print('Run python main.py -h for help')



if __name__ == '__main__':
    main()
