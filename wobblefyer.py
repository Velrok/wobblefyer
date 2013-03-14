#!/usr/bin/env python
"""Usage: wobblefyer.py

"""
# from docopt import docopt
from wobble import WobbleService

import logging
logging.basicConfig(level=logging.DEBUG)

USERNAME = u'velroktestuser@example.com'
PASSWORD = u'VelrokTestUser'


def main():
    with WobbleService().connect(USERNAME, PASSWORD) as service:
        for i in range(1):
            for msg in service.get_notifications():
                if 'source' not in msg or msg['source'] != 'post_change_lock':
                    print msg


if __name__ == '__main__':
    main()
