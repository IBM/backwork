"""Upload file to Softlayer storage options."""
import logging
import os
import sys
import object_storage
from .upload_base import UploadBase

log = logging.getLogger(__name__)

class ObjectStorageUpload(UploadBase):
    """Upload a file to Softlayer ObjectStorage."""
    command = "softlayer"

    def __init__(self, args, extra):
        super(ObjectStorageUpload, self).__init__(args, extra)

        self.client = object_storage.get_client(self.args.username, self.args.api_key, datacenter=self.args.datacenter)

    @classmethod
    def parse_args(cls, subparsers):
        """Add Softlayer ObjectStorage arguments to command line parser."""
        sl_oo_parser = subparsers.add_parser("softlayer", description=cls.__doc__)

        sl_oo_parser.add_argument("-u", "--username",
            help="username for Softlayer ObjectStorage API")
        sl_oo_parser.add_argument("-p", "--api-key",
            help="api key for Softlayer ObjectStorage API")
        sl_oo_parser.add_argument("-d", "--datacenter",
            help="datacenter where the file will be stored")
        sl_oo_parser.add_argument("-c", "--container",
            help="target container")

        sl_oo_parser.add_argument("local_path", nargs="?", default=None,
            help="path in the local file system of the file to be uploaded")
        sl_oo_parser.add_argument("remote_path",
            help="""path on Softlayer ObjectStorage container where the file
            will be stored""")

    def upload(self):
        """Upload a file from `local_path` to `remote_path` on ObjectStorage."""
        log.info("uploading '%s' to Softlayer ObjectStorage", self.args.local_path)
        log.info("target path: '%s/%s' at '%s'", self.args.container, self.args.remote_path, self.args.datacenter)

        container = self.client[self.args.container]

        # make sure target container exists
        if container.name not in [c.name for c in self.client.containers()]:
            log.info("container '%s' not found. creating it...", self.args.container)
            container.create()

        with open(self.args.local_path) as f:
            container[self.args.remote_path].send(f)

        log.info("upload complete")
