import sys
from raven import Client
from .notifier_base import NotifierBase

class SentryNotifier(NotifierBase):
    """Send messages to a Sentry server."""
    command = "sentry"

    def __init__(self, args, extra):
        """Initialize Sentry notifier with client"""
        super(SentryNotifier, self).__init__(args, extra)

        self.client = Client(self.args.sentry_dsn)

    @classmethod
    def parse_args(cls, parser):
        """Add command line argument parsing rules for Sentry."""
        parser.add_argument("--sentry-dsn", required=False,
            help="""Sentry DSN to be used for notifications. It can also be set
            with the evironment variable $SENTRY_DSN.""")

    def notify(self, msg=""):
        """Send a message to Sentry server.

        The message can be an exception or a simple string. In the first case,
        handle it with `captureException` method to add more context to the
        error.
        """
        if issubclass(msg.__class__, Exception):
            self.client.captureException()
        else:
            self.client.captureMessage(msg)
