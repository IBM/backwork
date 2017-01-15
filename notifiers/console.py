"""Sample implementation of a notifier.

Send notification to stdout using `print`.
"""
from .notifier_base import NotifierBase

class ConsoleNotifier(NotifierBase):
    command = "console"

    def notify(self, msg=""):
        print msg
