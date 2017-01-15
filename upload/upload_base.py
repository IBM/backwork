class UploadBase(object):
    """Base class that describes the interface an upload command must implement.

    Attributes:
        command     the value used in the command line to invoke this command,
                    usually is the name of the service (e.g.: softlayer, s3)
    """
    command = ""

    def __init__(self, args, extra):
        """Initialize an upload command given the arguments passed to CLI"""
        self.args = args
        self.extra = extra

    @classmethod
    def parse_args(cls, subparsers):
        """Parse CLI arguments specific to this subcommand"""
        raise NotImplementedError("Base method not overriden.")

    def upload(self):
        """Upload a file to the remote service.

        All the values passed via the CLI are available at `self.args` and
        `self.extra`. The first object stores known arguments that have been
        explicitly parsed. The second object is a list of arguments that are
        unkown to the parser and can be useful for invoking other commands
        withouht having to re-define its parser's arguments.

        This method should raise exceptions in case of errors so any active
        notifier can hadle it.
        """
        raise NotImplementedError("Base method not overriden.")
