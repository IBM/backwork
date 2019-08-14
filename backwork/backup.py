"""Handle backup subcommand.

Backup commands should receive an argument specifying where to store the backup
file. It should also provide the options to archive, compress and timestamp the
backup into a single file to facilitate storage.
"""
import os
from .lib import utils

__all__ = ["parse_args", "backup", "BackupError"]

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
ENGINES = utils.load_engines("backwork.backups")

def parse_args(subparsers):
    """Parse command line arguments passed to the backup command."""
    backup_parser = subparsers.add_parser("backup",
                                          description="""Perform database
                                        backups. Run `backwork backup
                                        {database_type} -h` for more details
                                        on each supported database.""")

    backup_parser.add_argument("-U", "--upload", action="store_true",
                               help="""output backup data to stdout to allow
                               piping it to an upload command""")

    # load engines' parsers
    backup_subparsers = backup_parser.add_subparsers(dest="type")
    for _, klass in ENGINES.items():
        klass.parse_args(backup_subparsers)

def backup(args, extra):
    """Invoke the backup method from the specified database type."""
    engine = ENGINES.get(args.type, None)

    if engine is None:
        raise BackupError("Backup method '%s' not found.", args.type)

    engine(args, extra).backup()

class BackupError(Exception):
    """Custom Exception raised by backup engines."""
    pass
