############
Getting Help
############

The CLI features extensive contextual help. Get a listing of
supported commands and global options via  ``--help``.

.. code-block:: shell

    $ tapis3 --help
    usage: tapis3 [--version] [-v | -q] [--log-file LOG_FILE] [-h] [--debug]

    Tapis v3 CLI: Scripting interface to the Tapis V3 platform. Documentation at https://tapis3-cli.rtfd.io/. For support
    contact None

    optional arguments:
    --version             show program's version number and exit
    -v, --verbose         Increase verbosity of output. Can be repeated.
    -q, --quiet           Suppress output except warnings and errors.
    --log-file LOG_FILE
                            Specify a file to log output. Disabled by default.
    -h, --help            Show help message and exit.
    --debug               Show tracebacks on errors.

    Commands:
    actors aliases create  Create an Alias for an Actor.
    actors aliases delete  Delete an Alias.
    actors aliases list  List Aliases.
    [listing continues...]

Find available commands for a specific API:

.. code-block:: shell

    $ tapis3 actors --help
    Command "actors" matches:
    actors aliases create
    actors aliases delete
    actors aliases list
    actors aliases update
    actors create
    actors delete
    [listing continues...]
    ...

Get help for a specific command:

.. code-block:: shell

    $ tapis3 help actors list
    $ # or
    $ tapis3 actors list --help
