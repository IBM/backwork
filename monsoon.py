#!/usr/bin/env python

import argparse
import logging
import sys

import backup
import notifiers
import upload

from raven import Client

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)-7s %(message)s")

def parse_args(args=sys.argv[1:]):
    parser = argparse.ArgumentParser()

    # parse notifier arguments
    notifiers.parse_args(parser)

    # parse subcommand
    subparsers = parser.add_subparsers(dest="command")
    backup.parse_args(subparsers)
    upload.parse_args(subparsers)

    return parser.parse_known_args()

if __name__ == "__main__":
    args, extra = parse_args()
    notifiers.initialize(args, extra)

    try:
        if args.command == "backup":
            backup.backup(args, extra)

        elif args.command == "upload":
            upload.upload(args,extra)

    except Exception as e:
        notifiers.notify(e)

