"""Handle download subcommand.

Download commands take a file from a remote service and download them to the local filesystem. They
should raise exceptions in case of failures so that notifiers can handle them.
"""
import os
from .lib import utils

__all__ = ["parse_args", "download", "DownloadError"]

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
ENGINES = utils.load_engines("backwork.downloads")


def parse_args(subparsers):
    """Add parsing rules for the download command and subcommands."""
    description = """Download a file from remote service. Run `backwork download
        {service} -h` for more details on each supported service."""
    download_parser = subparsers.add_parser(
        "download", description=description)
    download_subparsers = download_parser.add_subparsers(dest="service")

    for _, klass in ENGINES.items():
        klass.parse_args(download_subparsers)


def download(args, extra):
    """Route download command to the selected download handler."""
    engine = ENGINES.get(args.service, None)

    if engine is None:
        raise DownloadError("Download method '%s' not found.", args.service)

    engine(args, extra).download()


class DownloadError(Exception):
    """Backwork Download Error"""
    pass
