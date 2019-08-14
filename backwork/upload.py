"""Handle upload subcommand.

Upload commands take a local file and upload them to a remote service. They
should raise exceptions in case of failures so that notifiers can handle them.
"""
import os
from .lib import utils

__all__ = ["parse_args", "upload", "UploadError"]

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
ENGINES = utils.load_engines("backwork.uploads")


def parse_args(subparsers):
    """Add parsing rules for the upload command and subcommands."""
    description = """Upload a file to remote service. Run `backwork upload
        {service} -h` for more details on each supported service."""
    upload_parser = subparsers.add_parser("upload", description=description)
    upload_subparsers = upload_parser.add_subparsers(dest="service")

    for _, klass in ENGINES.items():
        klass.parse_args(upload_subparsers)


def upload(args, extra):
    """Route upload command to the selected upload handler."""
    engine = ENGINES.get(args.service, None)

    if engine is None:
        raise UploadError("Upload method '%s' not found.", args.service)

    engine(args, extra).upload()


class UploadError(Exception):
    """Backwork Upload Error"""
    pass
