================
Learning Locker
================

This page explains how to configure Learning Locker. Learning Locker is located at http://localhost:8001 when you are using the default configuration.

Creating a store
*****************
Learning Locker needs a store for it to save the statement to. So we will create one:

* Log in to Learning Locker with the credentials you created in `1.2.2. Login credentials <docker.html#login-credentials>`_.
* Go to your created organisation.
* Using the menu on the left, open ``Settings``.
* Open ``Stores``.
* Click the ``Add new`` button in the top right of your screen.
* Fill in the ``Name`` and ``Description`` fields.

Creating a client
********************
To let Mofa interface with Learning Locker, we need a user that is authenticated for Learning Locker.

* Log in to Learning Locker.
* Using the menu on the left, open ``Settings``.
* Open ``Clients``.
* Click ``New xAPI store client``.
* Fill in the ``Name`` field.
* Check the ``API All`` and ``Delete statements`` checkboxes under ``Overall Scopes``.
* Click the ``LRS (optional)`` and select the store you just created.
