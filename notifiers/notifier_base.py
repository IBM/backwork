class NotifierBase(object):
    """Base class for notifiers

    Notifiers are responsible for sending messages to external services to
    report relevant events that may happen during the execution of a command.

    Attributes:
        command     the value used to enable a notifier in the command line,
                    e.g.: `monsoon -n {command}`
    """
    command = ""

    def __init__(self, args, extra):
        self.args = args
        self.extra = extra

    @classmethod
    def parse_args(cls, parser):
        """Add command line argument parsing rules relevant to the notifier.

        This method is not required to be implemented as it might not be
        necessary to add more arguments to the parser in some cases.
        """
        pass

    def notify(self, msg=""):
        """Handle an incoming message."""
        raise NotImplementedError("Base method not overriden.")
