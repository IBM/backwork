# monsoon
Backup simplified.

`monsoon` is a toolkit that simplifies the process of backing up databases. It
handles the backup process itself as well as upload and error notification.

## Prerequisites
* Python 2.7

## Installing
Just clone this repository and install the dependencies. In the future the
project will properly packaged so it can be installed with `pip`.

```sh
$ git clone https://github.ibm.com/apset/monsoon.git
$ cd monsoon
$ pip install -r requirements.txt
```

## Running
Just execute the `monsoon.py` script. You can also turn the script into an
executable and create a symlink it to a folder in your `PATH` for easier access.

```sh
$ chmod +x monsoon.py
$ ln -s `pwd`/monsoon.py /usr/local/bin/monsoon
```

## Examples
##### Backup a MongoDB database running locally
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

##### Backup remote MongoDB database
```sh
$ monsoon backup mongo -h <HOST IP>:<PORT> -u <USER> -p<PASSWORD>
```

##### Backup a MongoDB to a specific folder and file name
```sh
$ monsoon backup mongo -o /var/backups --archive=mongo_backup.archive
```

##### Upload a backup file to Softlayer ObjectStorage
```sh
$ monsoon upload softayer -u <USERNAME> -p <API KEY> -d <DATACENTER> -c <CONTAINER> /path/to/file /remote/path/location
```

##### User Sentry to receive error messages
```sh
$ monsoon -n sentry --sentry-dsn <SENTRY DSN> backup mongo -o /var/backups --archive=mongo_backup.archive
```

##### More info
Check the `--help` information for each of the commands for more details.

## Supported databases
* MongoDB

## Supported storage services
* Softlayer ObjectStorage

## Supported notifiers
* Sentry

## Extending
If you want to support other databases, storage services or notifiers, just
create a new file in the correspondig folder and follow the structure provided
by the base classes (`BackupBase`, `UploadBase` and `NotifierBase`).

The files should picked up and loaded automatically.

## Future work
* Add support for more databases, storage services and notifiers
* Package project
* Package all pieces
* Handle backup scheduling
* Support more environment variables
