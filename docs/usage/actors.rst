######
Actors
######

Support for Tapis Actors_ is is provided by the **actors** command set. 

*******
General
*******

List and inspect all Actors the currently authenticated user can access.

.. autoprogram-cliff:: tapis3.cli
   :command: actors list

.. autoprogram-cliff:: tapis3.cli
   :command: actors show

Messaging
=========

Send a message to an Actor's mailbox, resulting in an Execution. This can 
be done asynchronously (default) or synchronously. For the latter case, it 
is possible to save the result to a file.

.. autoprogram-cliff:: tapis3.cli
   :command: actors submit

.. autoprogram-cliff:: tapis3.cli
   :command: actors run

Executions
==========

List and inspect Executions for a given Actor. It is also possible 
to view the logs for a specific Execution.

.. autoprogram-cliff:: tapis3.cli
   :command: actors execs *

*******
Sharing
*******

Assign and manage human-readable nicknames for Actors that 
can be used in lieu of their unique IDs. 

Aliases
=======

.. autoprogram-cliff:: tapis3.cli
   :command: actors aliases *

Nonces
======

Generate and manage Nonces, which are a kind of API key for 
Actors that allow them to be used without authenticating to the 
Tapis platform. Nonces can be issued against individual actorIds 
but can also be issued for aliases. The ``-A`` option must be 
passed to specify that the Actor identifier is an alias.

.. autoprogram-cliff:: tapis3.cli
   :command: actors nonces *

Permissions
===========

Grant and manage update and execution rights for an 
Actor to other Tapis platform users. 

.. autoprogram-cliff:: tapis3.cli
   :command: actors pems *

**************
Administration
**************

Create and manage Actors. This can be accomplished by interacting 
directly with the Abaco APIs via ``create``, ``update``, and 
``delete`` or via Tapis CLI workflows ``init`` and ``deploy``. 

.. autoprogram-cliff:: tapis3.cli
   :command: actors create

.. autoprogram-cliff:: tapis3.cli
   :command: actors update

.. autoprogram-cliff:: tapis3.cli
   :command: actors delete

.. autoprogram-cliff:: tapis3.cli
   :command: actors deploy


Workers
=======

View and manage an Actor's workers, which control the extent 
to which the Actor can scale to accomodate additional concurrent 
messages. 

.. autoprogram-cliff:: tapis3.cli
   :command: actors workers *


.. _Actors: https://tapis.readthedocs.io/en/latest/technical/actors.html
