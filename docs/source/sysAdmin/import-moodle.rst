########################
Importing Moodle
########################
Before starting to use Mofa, you first need to have the courses and teachers from Moodle. Mofa will do this for you. The only thing you have to do is run the following command in the ``src`` directory:

.. danger::
    This command will wipe all your existing courses, everything linked to those courses (e.g. assistants, resources and activities) and all the non-superuser users in Mofa. The command will prompt you to confirm this.
    **You will probably only want to run this during the setup!**

Windows
======================

.. code-block:: powershell

    py manage.py import_moodle

Linux
======================

.. code-block:: powershell

    ./manage.py import_moodle

After running the command you will see how many courses / activities / resources / teachers were imported. The teachers of the courses will be able to log in with their Moodle username and standard password ``Test123!``.

.. important::
    In a later stage of development this would be linked with the Solis-ID. This is why we chose to do it this unsecure way during development.
