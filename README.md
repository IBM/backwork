# monsoon
Backup simplified.

`monsoon` is a toolkit that simplifies the process of backing up databases. It
handles the backup process itself as well as upload and error notification.

## Prerequisites
* Python 2.7

## Installing
You can install `monsoon` from GHE using `pip`:
```sh
$ pip install git+ssh://git@github.ibm.com/apset/monsoon
```

## Running
After installing you should have a `monsoon` command available.
```
$ monsoon --help
usage: monsoon [-h] [-n NOTIFIERS] {backup,upload} ...

positional arguments:
  {backup,upload}

optional arguments:
  -h, --help            show this help message and exit
  -n NOTIFIERS, --notify NOTIFIERS
                        enable a notifier, it can be used multiple times
```

## Plug-ins
Just having `monsoon` is not enough. You will need to the plug-ins that better
suite your needs.

Plug-ins are divided into three categories:

### Backup
Backup plugins are responsible for connecting to a databases and doing the
actual backup process.

Once you install a backup plug-in it will be available via the `monsoon backup`
command:
```sh
$ monsoon backup --help
usage: monsoon backup [-h] [-U] {mongo} ...

Perform database backups. Run `monsoon backup {database_type} -h` for more
details on each supported database.

positional arguments:
  {mongo}

optional arguments:
  -h, --help    show this help message and exit
  -U, --upload  output backup data to stdout to allow piping it to an upload
                command
```

#### Available plugin-ins:
* [monsoon-backup-mongo](https://github.ibm.com/apset/monsoon-backup-mongo)

### Upload
Upload plug-ins store your backup files securely in a remote storage.

You can use them with the `monsoon upload` command:
```sh
$ monsoon upload --help
usage: monsoon upload [-h] {softlayer} ...

Upload a file to remote service. Run `monsoon upload {service} -h` for more
details on each supported service.

positional arguments:
  {softlayer}

optional arguments:
  -h, --help   show this help message and exit
```
#### Available plugin-ins:
* [monsoon-upload-softlayer](https://github.ibm.com/apset/monsoon-upload-softlayer)

### Notifiers
Notifiers tell you when things go wrong. More important than having a backup
process configured is knowing when this process fails.

Notifiers are enabled on the `monsoon` command using the `-n` or `--notify`
arguments. They may also require some extra values, such API keys.

```sh
$ monsoon --help
usage: monsoon [-h] [-n NOTIFIERS] [--sentry-dsn SENTRY_DSN]
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
* [monsoon-notify-sentry](https://github.ibm.com/apset/monsoon-notify-sentry)

## Examples
#### Backup a MongoDB database running locally
```sh
$ monsoon backup mongo
2017-01-15 03:58:15,270 backup.mongo INFO    starting mongo backup...
2017-01-15 03:58:15,270 backup.mongo INFO    saving file to /Users/laoqui/Projects/monsoon/dumps/mongo_backup_20170115-035815.archive.gz
2017-01-15 03:58:15,350 backup.mongo INFO    output:

        2017-01-15T03:58:15.342-0500    writing app.products to archive '/Users/laoqui/Projects/monsoon/dumps/mongo_backup_20170115-035815.archive.gz'
        2017-01-15T03:58:15.347-0500    done dumping app.products (1 document)

2017-01-15 03:58:15,350 backup.mongo INFO    backup complete
```
This will create an archived backup, compressed and timestamped, and stored in a
folder called `dumps` in the current directory.

#### Backup remote MongoDB database
```sh
$ monsoon backup mongo -h <HOST IP>:<PORT> -u <USER> -p<PASSWORD>
```

#### Backup a MongoDB to a specific folder and file name
```sh
$ monsoon backup mongo -o /var/backups --archive=mongo_backup.archive
```

#### Upload a backup file to Softlayer ObjectStorage
```sh
$ monsoon upload softayer -u <USERNAME> -p <API KEY> -d <DATACENTER> -c <CONTAINER> /path/to/file /remote/path/location
```

#### User Sentry to receive error messages
```sh
$ monsoon -n sentry --sentry-dsn <SENTRY DSN> backup mongo -o /var/backups --archive=mongo_backup.archive
```

#### More info
Check the `--help` information for each of the commands for more details.

## Extending
The best way to extend `monsoon` is by creating new plugi-ins. They are simple
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

```

```python
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
```

```python
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

To make your package visible to `monsoon` you will also need to declare an
[`entry_point`](https://setuptools.readthedocs.io/en/latest/setuptools.html#dynamic-discovery-of-services-and-plugins)
in your `setup.py` file.

Each plug-in type has a different `entry_point` key:

#### Backups:
```python
setup(
    ...
    entry_points={
        "monsoon.backups": [
            "<COMMAND NAME>": "module:BackupClass"
        ]
    },
    ...
```

#### Uploads:
```python
setup(
    ...
    entry_points={
        "monsoon.uploads": [
            "<COMMAND NAME>": "module:UploadClass"
        ]
    },
    ...
```

#### Notifiers:
```python
setup(
    ...
    entry_points={
        "monsoon.notifiers": [
            "<COMMAND NAME>": "module:NotifierClass"
        ]
    },
    ...
```

Once your plug-in is ready you can use `pip` to install it and it should be
available to be used be `monsoon`.

## Future work
* Add support for more databases, storage services and notifiers
* Handle backup scheduling
* Support more environment variables
