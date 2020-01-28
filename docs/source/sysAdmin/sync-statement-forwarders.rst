########################################
Synchronising Statement Forwarders
########################################

In the event that statement forwarders from Learning Locker get desynchronized from the Mofa database, we have created a command that will synchronize them again.
This will remove the excess Statement Forwarders in Learning Locker and add Statement Forwarders that are missing in Learning Locker.

Windows
======================

.. code-block:: powershell

    py manage.py sync_statement_forwarders

Linux
======================

.. code-block:: powershell

    ./manage.py sync_statement_forwarders
