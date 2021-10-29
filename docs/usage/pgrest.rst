######
PgREST
######

Support for Tapis PgREST_, our PostgreSQL-as-a-service API, is is provided 
by the **pg** command set.

********
Data API
********

Create, retrieve, update, delete rows from tables you have access to.

.. autoprogram-cliff:: tapis3.cli
   :command: pg rows *

Retrieve data from views you have access to.

.. autoprogram-cliff:: tapis3.cli
   :command: pg views *

**************
Management API
**************

All management API calls require that you hold a PgREST administrative role_. 

Create, retrieve, update, delete tables and table definitions.

.. autoprogram-cliff:: tapis3.cli
   :command: pg tables man *

Create, retrieve, update, delete tables and view definitions.

.. autoprogram-cliff:: tapis3.cli
   :command: pg views man *

Manage access roles.

.. autoprogram-cliff:: tapis3.cli
   :command: pg roles man *

.. _role: https://tapis.readthedocs.io/en/latest/technical/pgrest.html#permissions-and-roles
.. _PgREST: https://tapis.readthedocs.io/en/latest/technical/pgrest.html
