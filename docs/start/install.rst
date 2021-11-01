##################
Installing the CLI
##################

Tapis3 CLI is available as a Python package. For now, it must be installed 
from source, but will eventually be available via PyPi.

The CLI requires Python 3.7 or higher for core functions. Supplemental 
operations, such as the app and actor *deploy* workflows, require local 
installation of Docker or Docker Desktop and an active DockerHub account. 

***********
From Source
***********

.. code-block:: shell

    $ git clone https://github.com/TACC-Cloud/tapis3-cli.git
    $ cd tapis3-cli
    $ pip install --user .

***************
Container Image
***************

The CLI will also be available as a Docker image when it 
is closer to general release. 
