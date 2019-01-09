#!/usr/bin/env python3
"""
TenantBase Backend
Key-value storage server implemented in SQlite and memmcached.


"""
import logging

__author__ = 'Nicolas Ferga'
__version__ = "0.1.0"

LOG = logging.getLogger()
LOG.setLevel(logging.INFO)

def main():
    """main function"""
    LOG.info('tenant-base')

if __name__ == '__main__':
    main()
