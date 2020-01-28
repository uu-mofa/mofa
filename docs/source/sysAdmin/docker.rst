########################
Docker
########################

.. note::
    If you already have an instance of Moodle, you don't need to install Docker and can skip to `2. Learning Locker <learning-locker.html>`_.
    You will have to manually install Learning Locker using the `Learning Locker installation guide <https://docs.learninglocker.net/guides-installing/>`_ though.

This page explains on how to get started with Docker.

Installation
********************
The Docker folder in the repository contains a Docker configuration, which sets up a Docker environment in which an instance of Moodle and Learning Locker run side by side.
When set up, the environment provides the connection needed between them to let Moodle send events to Learning Locker.
Learning Locker can then be opened up to the virtual assistant component for testing.

If any problems occur during the Docker installation, please consult the `Docker documentation. <https://docs.docker.com/>`_

Windows
===========
.. note:: Docker for Windows only runs on 64-bit Windows 10 Pro, Enterprise, and Education.

* Download `Docker for Windows <https://download.docker.com/win/stable/Docker%20Desktop%20Installer.exe>`_.
* During configuration **do not** check *"Use Windows containers instead of Linux containers"*.
* After the installation of Docker, the installation will prompt you to install HyperV. Follow the instruction on screen.

Mac
===========
* Download `Docker for Mac <https://download.docker.com/mac/stable/Docker.dmg>`_.

Linux
===========
To install Docker on Linux:

.. code-block:: sh

    sudo apt install docker.io
    sudo curl -L https://github.com/docker/compose/releases/download/1.18.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose

.. _docker-configuration:


Configuration
************************
After installing Docker is complete, it is time to start using it:

* Clone the Mofa git on `Github <https://github.com/uu-mofa/mofa>`_.
* Start Docker Desktop.
* Open a Powershell or Terminal window and navigate to the Docker folder inside the project folder.
* Run  ``build-dev.bat`` on Windows or ``./build-dev.sh`` on Linux, this will take a while.
* This script builds the Learning Locker app and engine for Docker.
* To start the containers run ``docker-compose up -d``. Moodle still needs to install the first time running this, please be very patient and do not touch it untill Moodle works.



URLs
========================
Now you will be able to view your own Moodle and Learning Locker instances at:

* Moodle: http://localhost:8002
* Learning Locker: http://localhost:8001

Login credentials
========================

Log in to Moodle with the following credentials:

* User: user
* Password: bitnami

For Learning Locker, create a new superuser using the following command. Replace the brackets with your own information:

.. code-block:: sh

    docker-compose exec api node cli/dist/server createSiteAdmin [email] [organisation] [password]

    For example: docker-compose exec api node cli/dist/server createSiteAdmin mofa@gmail.com Utrecht_University welcome123!


Troubleshooting Docker commands
======================================

If you have any trouble with Docker, here are some of the basic commands.

* ``docker ps``: shows all the Docker containers by name and their current status.
* ``docker-compose down``: shuts off all the containers.
* ``docker-compose down --rmi all -v``: shuts off all the containers and deletes all images. Use when you've made an irreversible error.
* ``docker exec -it <container-name> /bin/powershell``: opens the Powershell command shell for the container.
* ``docker logs -f <container-id>``: shows the log of the container.
