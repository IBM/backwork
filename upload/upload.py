"""Handle upload subcommand.

Upload commands take a local file and upload them to a remote service. They
should raise exceptions in case of failures so that notifiers can handle them.
"""
import os
from lib import utils
from .upload_base import UploadBase

__all__ = ["parse_args", "upload", "UploadError"]

current_path = os.path.dirname(os.path.realpath(__file__))
engines = utils.load_engines(UploadBase, current_path, "upload.")

def parse_args(subparsers):
    """Add parsing rules for the upload command and subcommands."""
    upload_parser = subparsers.add_parser("upload",
        description="""Upload a file to remote service. Run `monsoon upload
        {service} -h` for more details on each supported service.""")
    upload_subparsers = upload_parser.add_subparsers(dest="service")

    for _, klass in engines.iteritems():
        klass.parse_args(upload_subparsers)

def upload(args, extra):
    """Route upload command to the selected upload handler."""
    engine = engines.get(args.service, None)

    if engine is None:
        raise UploadError("Upload method '%s' not found.", args.service)

    engine(args, extra).upload()

class UploadError(Exception):
    pass
