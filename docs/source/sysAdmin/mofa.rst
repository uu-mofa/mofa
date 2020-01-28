########################
Mofa
########################

This page explains on how to get started with Mofa.

To use Mofa, you need to have a python version 3.6 or higher installed.

* Download and install `Python <https://www.python.org/downloads/>`_.
* Optional: create and start your `virtual environment <https://docs.python.org/3/tutorial/venv.html>`_.

Installing requirements
******************************
Windows

.. code-block:: powershell

    cd /path/to/project/src/
    pip install -r requirements.txt


Linux

.. code-block:: powershell

    cd /path/to/project/src/
    pip3 install -r requirements.txt

Running the server
******************************


Windows

.. code-block:: sh

    py manage.py runserver 0.0.0.0:8000

Linux

.. code-block:: sh

    ./manage.py runserver 0.0.0.0:8000

Creating a user
******************************


In order to log in, an account is needed. This can be created by doing:

Windows

.. code-block:: powershell

    py manage.py createsuperuser

Linux

.. code-block:: powershell

    python3 manage.py createsuperuser

