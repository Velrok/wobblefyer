#!/usr/bin/env python
""" Wobblefyer. A liaison between the wobble api and the command line.

Usage:
    wobblefyer.py <cli-script>

Options:
    -h --help       Show this screen.
    -v --version    Show version.
"""
from docopt import docopt
from wobble import WobbleService
from bs4 import BeautifulSoup
import subprocess

import logging
logging.basicConfig(level=logging.INFO)

arguments = None

USERNAME = u'velroktestuser@example.com'
PASSWORD = u'VelrokTestUser'


def post_changed_msg_processor(msg, service):
    if "source" in msg and "lock" in msg['source']:
        return  # skipp lock related messages for now

    # print msg
    topic = service.topic_get_details(msg['topic_id'])
    post = filter(lambda p: p['id'] == msg['post_id'],
                  topic['posts'])[0]

    soup = BeautifulSoup(post['content'])
    caller_args = map(str, [arguments['<cli-script>'],
                           soup.get_text(),
                           msg['type']])
    subprocess.Popen(caller_args)


def process_message(msg, service):
    type_processor_fn_name = "{}_msg_processor".format(msg['type'])
    try:
        type_processor_fn = globals()[type_processor_fn_name]
        type_processor_fn(msg, service)
    except KeyError:
        logging.debug("No processor for message type: {}".format(msg['type']))


def main():
    with WobbleService().connect(USERNAME, PASSWORD) as service:
        while (True):
            logging.debug("Checking for messages.")
            for msg in service.get_notifications():
                logging.debug("Got message: {}".format(msg))
                process_message(msg, service)


if __name__ == '__main__':
    arguments = docopt(__doc__, version="0.0.0")
    main()
