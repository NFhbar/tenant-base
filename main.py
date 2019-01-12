# -*- coding: utf-8 -*-
"""
TenantBase Backend
Key-value server implemented in SQlite and memmcached.

To run the interface:

$ python3 main.py -s database.sqlite

Interface options are:

Interface options:
 - set key value exptime
 - get key
 - delete key
 - exit

To return all key-value pairs in db:

$ python3 main.py -sh database.sqlite

"""
from os import system
import sys
import logging
import argparse
from pymemcache.client import Client
import helpers

# globals
LOG = logging.getLogger()
LOG.setLevel(logging.INFO)
KeyValueHelper = helpers.KeyValueHelper
Color = helpers.Color_Helper
HOST = 'localhost'
PORT = 11211
START_MEMCACHED = 'memcached -d'

# Menu options
DESCRIPTION = '{b}TenantBase -- sqlite3 + memcached interface.{e}'.format(b=Color.BOLD, e=Color.END)
SERVE_HELP = 'starts interface:\n $ python3 -s filename'
SHOW_HELP = 'displays all key-value pairs: \n $ python3 -sh filename'
MEMCAHED_INTERFACE_HELP = '{b}Interface options:{e}\n \
- set key value exptime\n \
- get key\n \
- delete key\n \
- exit\n'.format(b=Color.BOLD, e=Color.END)
DATABASE = 'database.sqlite'

# functions
def run_command(command=None):
    """Wrapper around os.system, will raise exception if command did not exit cleanly"""
    exit_code = system(command)
    if exit_code != 0:
        LOG.error('Cannot execute command: %s. Did you install it?', command)
        raise Exception('Cannot execute command: %s. Did you install it?' % command)

def parse_args(args=None):
    """parses command line arguments"""
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('-s', '--serve', type=str, dest='serve',
                        help=SERVE_HELP, metavar=DATABASE)
    parser.add_argument('-sh', '--show', type=str, dest='show',
                        help=SHOW_HELP, metavar=DATABASE)

    return parser.parse_args(args)

def set_value(user_input=None, client=Client((HOST, PORT)), db_name=DATABASE):
    """sets key-value pair in memcached and sqlite"""
    if user_input is None:
        return []
    client.set(user_input[1], user_input[2])
    db_conn = KeyValueHelper(db_name)
    db_conn[user_input[1]] = user_input[2]
    db_conn.close()

    return [user_input[1], user_input[2]]


def get_value(user_input=None, client=Client((HOST, PORT)), db_name=DATABASE):
    """gets the value from key from memcached or sqlite"""
    if user_input is None:
        return None

    response = client.get(user_input[1])

    if response is None:
        LOG.info('%s not found in memcached, searching sqlite', user_input[1])
        db_conn = KeyValueHelper(db_name)
        try:
            response = db_conn[user_input[1]]
            LOG.info('%s found in sqlite. Adding to memcahed', user_input[1])
            client.set(user_input[1], response)

        except KeyError as error:
            LOG.info('%s not found in sqlite', user_input[1])
            LOG.error(error)

        db_conn.close()

    else:
        response = response.decode('utf-8')

    return response

def delete_value(user_input=None, client=Client((HOST, PORT)), db_name=DATABASE):
    """deletes the value from memcached and sqlite"""
    if user_input is None:
        return False

    response = client.delete(user_input[1])
    try:
        db_conn = KeyValueHelper(db_name)
        del db_conn[user_input[1]]
        db_conn.close()
    except KeyError as error:
        LOG.info('%s not found', user_input[1])
        LOG.error(error)
        response = False

    return response

# main
def main(argv=None):
    """main function"""
    parser = parse_args(argv)

    if parser.serve:
        try:
            run_command(START_MEMCACHED)
            print('{g}Memcached server started on {h}:{p}{e}\n'
                  .format(g=Color.GREEN, h=HOST, p=PORT, e=Color.END))
            client = Client((HOST, PORT))

        except ConnectionRefusedError as error:
            LOG.error('Error: %s', error)
            sys.exit(1)

        exit = False
        while exit is False:
            user_input = [i for i in input(MEMCAHED_INTERFACE_HELP).split()]

            if user_input[0] == 'set':
                if len(user_input) != 4:
                    print('{y}Please include key, value, and exptime ex:\n \
                          set key value exptime.\n{e}'
                          .format(y=Color.YELLOW, e=Color.END))
                else:
                    response = set_value(user_input, client, parser.serve)
                    print('{g}{r} set in memcached and sqlite.\n{e}'
                          .format(g=Color.GREEN, r=response, e=Color.END))

            elif user_input[0] == 'get':
                if len(user_input) != 2:
                    print('{y}Please include key, ex:\n get key{e}'
                          .format(y=Color.YELLOW, e=Color.END))
                else:
                    response = get_value(user_input, client, parser.serve)
                    print('{g}{r}{e}\n'.format(g=Color.GREEN, r=response, e=Color.END))


            elif user_input[0] == 'delete':
                if len(user_input) != 2:
                    print('{y}Please include key, ex:\n delete key{e}'
                          .format(y=Color.YELLOW, e=Color.END))
                else:
                    response = delete_value(user_input, client, parser.serve)
                    print('{g}{r}{e}\n'.format(g=Color.GREEN, r=response, e=Color.END))

            elif user_input[0] == 'exit':
                exit = True
                print('{g}Shutting down...'.format(g=Color.GREEN))

            else:
                print('{y}Incorrect option.{e}\n'.format(y=Color.YELLOW, e=Color.END))


    elif parser.show:
        print('{b}Current key value pairs in sqlite\n{e}'.format(b=Color.BOLD, e=Color.END))
        db_conn = KeyValueHelper(parser.show)
        for key, value in db_conn:
            print('{k} {v}'.format(k=key, v=value))

        print('\n{b}Closing sqlite3 connection...{e}\n'.format(b=Color.BOLD, e=Color.END))
        db_conn.close()
        print('{g}Shutting down...'.format(g=Color.GREEN))

    else:
        print('{y}Run python main.py -h for help{e}'.format(y=Color.YELLOW, e=Color.END))


if __name__ == '__main__':
    main()
