"""Handle show subcommand.

Show commands take a path or prefix in a remote service and return a list of files that exist
in that location. They are intented to help with the use of the show subcommand.
They should raise exceptions in case of failures so that notifiers can handle them.
"""
import os
from .lib import utils

__all__ = ["parse_args", "show", "ShowError"]

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
ENGINES = utils.load_engines("backwork.shows")


def parse_args(subparsers):
    """Add parsing rules for the show command and subcommands."""
    description = """Shows available backups on a remote service. Run `backwork show
        {service} -h` for more details on each supported service."""
    show_parser = subparsers.add_parser(
        "show", description=description)
    show_subparsers = show_parser.add_subparsers(dest="service")

    for _, klass in ENGINES.items():
        klass.parse_args(show_subparsers)


def show(args, extra):
    """Route show command to the selected show handler."""
    engine = ENGINES.get(args.service, None)

    if engine is None:
        raise ShowError("Show method '%s' not found.", args.service)

    engine(args, extra).show()


class ShowError(Exception):
    """Backwork Show Error"""
    pass
