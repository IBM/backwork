"""Handle restore subcommand.

Restore commands should receive an argument specifying where to look for the
file to restore from.
"""

import os
from .lib import utils

__all__ = ["parse_args", "restore", "RestoreError"]

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
ENGINES = utils.load_engines("backwork.restores")


def parse_args(subparsers):
    """Parse command line arguments passed to the restore command."""
    restore_parser = subparsers.add_parser("restore",
                                           description="""Perform database
                                        restores. Run `backwork restore
                                        {database_type} -h` for more details
                                        on each supported database.""")

    # load engines' parsers
    restore_subparsers = restore_parser.add_subparsers(dest="type")
    for _, klass in ENGINES.items():
        klass.parse_args(restore_subparsers)


def restore(args, extra):
    """Invoke the restore method from the specified database type."""
    engine = ENGINES.get(args.type, None)

    if engine is None:
        raise RestoreError("Restore method '%s' not found.", args.type)

    engine(args, extra).restore()


class RestoreError(Exception):
    """Custom Exception raised by restore engines."""
    pass
