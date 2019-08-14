#!/usr/bin/env python
"""Backup simplified.

backwork is a toolkit that simplifies the process of backing up databases. It
handles the backup process itself as well as upload and error notification.
"""

import argparse
import logging
import sys

from . import backup
from . import notifiers
from . import upload

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s %(name)s %(levelname)-7s %(message)s")

LOG = logging.getLogger(__name__)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()

    # parse notifier arguments
    notifiers.parse_args(parser)

    # parse subcommand
    subparsers = parser.add_subparsers(dest="command")
    backup.parse_args(subparsers)
    upload.parse_args(subparsers)

    return parser.parse_known_args()


def main():
    """Core functionality."""
    args, extra = parse_args()
    notifiers.initialize(args, extra)

    try:
        if args.command == "backup":
            backup.backup(args, extra)

        elif args.command == "upload":
            upload.upload(args, extra)

    except Exception as error:  # pylint: disable=broad-except
        notifiers.notify(error)
        LOG.exception(error)
        sys.exit(1)
