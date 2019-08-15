# backwork [![Build Status](https://travis-ci.org/IBM/backwork.svg?branch=master)](https://travis-ci.org/IBM/backwork) [![PyPI version](https://badge.fury.io/py/backwork.svg)](https://badge.fury.io/py/backwork)
Backup simplified.

`backwork` is a toolkit that simplifies the process of backing up and restoring databases. It
handles the backup process itself as well as upload, download, restoration, and error notification.

## Prerequisites
* Python 2.7

## Installing
You can install `backwork` using `pip`:
```sh
$ pip install backwork
```

## Running
After installing you should have a `backwork` command available.
```
$ backwork --help
usage: backwork [-h] [-n NOTIFIERS] {backup,restore,upload,download} ...

positional arguments:
  {backup,restore,upload,download}

optional arguments:
  -h, --help            show this help message and exit
  -n NOTIFIERS, --notify NOTIFIERS
                        enable a notifier, it can be used multiple times
```

## Plug-ins
Just having `backwork` is not enough. You will need to the plug-ins that
suit your needs. You can install plug-ins by running:
```sh
$ pip install <plug-in_name>
```

Plug-ins are divided into three categories:

### Backup
Backup plug-ins are responsible for connecting to databases and doing the
actual backup process, as well as the restore process for the backups.

Once you install a backup plug-in it will be available via the `backwork backup` and `backwork restore` commands:
```sh
$ backwork backup --help
usage: backwork backup [-h] [-U] {mongo} ...

Perform database backups. Run `backwork backup {database_type} -h` for more
details on each supported database.

positional arguments:
  {mongo}

optional arguments:
  -h, --help    show this help message and exit
  -U, --upload  output backup data to stdout to allow piping it to an upload
                command
```

```
usage: backwork restore [-h] [-U] {mongo} ...

Perform database restores. Run `backwork restore {database_type} -h` for more
details on each supported database.

positional arguments:
  {mongo}

optional arguments:
  -h, --help    show this help message and exit
```


#### Available plug-ins:
* `backwork-backup-mongo`

### Upload
Upload plug-ins store and retrieve your backup files securely from remote storage.

You can use them with the `backwork upload` and `backwork download` commands:
```sh
$ backwork upload --help
usage: backwork upload [-h] {softlayer} ...

Upload a file to remote service. Run `backwork upload {service} -h` for more
details on each supported service.

positional arguments:
  {softlayer}

optional arguments:
  -h, --help   show this help message and exit
```

```sh
$ backwork download --help
usage: backwork download [-h] {softlayer} ...

Download a file from a remote service. Run `backwork upload {service} -h` for more
details on each supported service.

positional arguments:
  {softlayer}

optional arguments:
  -h, --help   show this help message and exit
```

#### Available plug-ins:
* `backwork-upload-softlayer`

### Notifiers
Notifiers tell you when things go wrong. More important than having a backup
process configured is knowing when this process fails.

Notifiers are enabled on the `backwork` command using the `-n` or `--notify`
arguments. They may also require some extra values, such API keys.

```sh
$ backwork --help
usage: backwork [-h] [-n NOTIFIERS] [--sentry-dsn SENTRY_DSN]
               {backup,upload} ...

positional arguments:
  {backup,upload}

optional arguments:
  -h, --help            show this help message and exit
  -n NOTIFIERS, --notify NOTIFIERS
                        enable a notifier, it can be used multiple times
  --sentry-dsn SENTRY_DSN
                        Sentry DSN to be used for notifications. It can also
                        be set with the evironment variable $SENTRY_DSN.
```

You can enable as many notifiers as you want on a command.

**Available plug-ins:**
* `backwork-notify-sentry`

## Examples
#### Backup a MongoDB database running locally
```sh
$ backwork backup mongo
2017-01-15 03:58:15,270 backup.mongo INFO    starting mongo backup...
2017-01-15 03:58:15,270 backup.mongo INFO    saving file to /Users/laoqui/Projects/backwork/dumps/mongo_backup_20170115-035815.archive.gz
2017-01-15 03:58:15,350 backup.mongo INFO    output:

        2017-01-15T03:58:15.342-0500    writing app.products to archive '/Users/laoqui/Projects/backwork/dumps/mongo_backup_20170115-035815.archive.gz'
        2017-01-15T03:58:15.347-0500    done dumping app.products (1 document)

2017-01-15 03:58:15,350 backup.mongo INFO    backup complete
```
This will create an archived backup, compressed and timestamped, and stored in a
folder called `dumps` in the current directory.

#### Backup remote MongoDB database
```sh
$ backwork backup mongo -h <HOST IP>:<PORT> -u <USER> -p<PASSWORD>
```

#### Backup a MongoDB to a specific folder and file name
```sh
$ backwork backup mongo -o /var/backups --archive=mongo_backup.archive
```

#### Upload a backup file to Softlayer ObjectStorage
```sh
$ backwork upload softayer -u <USERNAME> -p <API KEY> -d <DATACENTER> -c <CONTAINER> /path/to/file /remote/path/location
```

#### User Sentry to receive error messages
```sh
$ backwork -n sentry --sentry-dsn <SENTRY DSN> backup mongo -o /var/backups --archive=mongo_backup.archive
```

#### More info
Check the `--help` information for each of the commands for more details.

## Extending
The best way to extend `backwork` is by creating new plugi-ins. They are simple
Python packages that implement a few set of methods. Here are some base classes
you can use as a starting point:

```python
class BackupBase(object):
    """Base class that describes the interface a backup command must implement.

    Attributes:
        command     the value used in the command line to invoke this command,
                    usually is the name of the database (e.g.: mongo, mysql)
    """
    command = ""

    def __init__(self, args, extra):
        """Initialize a backup command given the arguments passed to CLI"""
        self.args = args
        self.extra = extra

    @classmethod
    def parse_args(cls, subparsers):
        """Parse CLI arguments specific to this subcommand"""
        raise NotImplementedError("Base method not overriden.")

    def backup(self):
        """Backup a database given the arguments specified.

        All the values passed via the CLI are available at `self.args` and
        `self.extra`. The first object stores known arguments that have been
        explicitly parsed. The second object is a list of arguments that are
        unkown to the parser and can be useful for invoking other commands
        withouht having to re-define its parser's arguments.

        This method should raise exceptions in case of errors so any active
        notifier can hadle it.
        """
        raise NotImplementedError("Base method not overriden.")


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


class NotifierBase(object):
    """Base class for notifiers

    Notifiers are responsible for sending messages to external services to
    report relevant events that may happen during the execution of a command.

    Attributes:
        command     the value used to enable a notifier in the command line,
                    e.g.: `backwork -n {command}`
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
        """Handle an incoming message.

        The `msg` object could be either a `string` or an `Exception`. You may
        want to handle them differently with something like:

            if issubclass(msg.__class__, Exception):
              handle_exception(msg)
            else:
              handle_string(msg)

        If `msg` is an exception, the call to this method will be in the context
        of an `except`, meaning you will be able to access `sys.exc_info()`.
        """
        raise NotImplementedError("Base method not overriden.")
```

To make your package visible to `backwork` you will also need to declare an
[`entry_point`](https://setuptools.readthedocs.io/en/latest/setuptools.html#dynamic-discovery-of-services-and-plug-ins)
in your `setup.py` file.

Each plug-in type has a different `entry_point` key:

#### Backups:
```python
setup(
    ...
    entry_points={
        "backwork.backups": [
            "<COMMAND NAME>": "module:BackupClass"
        ],
        "backwork.restores": [
            "<COMMAND NAME>": "module:RestoreClass"
        ]
    },
    ...
```

#### Uploads:
```python
setup(
    ...
    entry_points={
        "backwork.uploads": [
            "<COMMAND NAME>": "module:UploadClass"
        ],
        "backwork.downloads": [
            "<COMMAND NAME>": "module:DownloadClass"
        ]
    },
    ...
```

#### Notifiers:
```python
setup(
    ...
    entry_points={
        "backwork.notifiers": [
            "<COMMAND NAME>": "module:NotifierClass"
        ]
    },
    ...
```

Once your plug-in is ready you can use `pip` to install it and it should be
available to be used be `backwork`.

## Future work
* Add support for more databases, storage services and notifiers
* Handle backup scheduling
* Support more environment variables
