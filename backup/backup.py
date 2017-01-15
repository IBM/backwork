"""Handle backup subcommand.

Backup commands should receive an argument specifying where to store the backup
file. It should also provide the options to archive, compress and timestamp the
backup into a single file to facilitate storage.
"""
from lib import utils
from .backup_base import BackupBase

__all__ = ["parse_args", "backup", "BackupError"]

engines = utils.load_engines(BackupBase, './backup', 'backup.')

def parse_args(subparsers):
    """Parse command line arguments passed to the backup command."""
    backup_parser = subparsers.add_parser("backup",
        description="""Perform database backups. Run `monsoon backup
        {database_type} -h` for more details on each supported database.""")

    backup_parser.add_argument("-U", "--upload", action="store_true",
        help="""output backup data to stdout to allow piping it to an upload
        command""")

    # load engines' parsers
    backup_subparsers = backup_parser.add_subparsers(dest="type")
    for _, klass in engines.iteritems():
        klass.parse_args(backup_subparsers)

def backup(args, extra):
    """Invoke the backup method from the specified database type."""
    engine = engines.get(args.type, None)

    if engine is None:
        raise BackupError("Backup method '%s' not found.", args.type)

    engine(args, extra).backup()

class BackupError(Exception):
    """Custom Exception raised by backup engines."""
    pass
