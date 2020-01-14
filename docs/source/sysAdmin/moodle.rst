..    include:: <isonum.txt>

########################
Moodle
########################

This page explains how to configure Moodle.

.. note::

    If you are using the default configuration, log in to Moodle with the following credentials:

    * User: user
    * Password: bitnami

RESTful plugin
*****************

For Mofa to be able to properly communicate with Moodle, you need to install the RESTful API plugin, do the following steps:

* Log in to an administrator account in Moodle.
* Open your Moodle instance, and navigate to ``Site administrations`` |rarr| ``Plugins`` |rarr| ``Install plugins``.
* Drag & drop the ``moodle-webservice_restful-master.zip`` into the box.
* Follow the instructions in Moodle.

Webservice configuration
***************************

The Moodle webservice is used to communicate with Moodle. For example, Mofa uses it to import courses from Moodle.

To enable the webservice, follow the following steps:

* Log in to an administrator account in Moodle.
* Go to Site Administration.
* Go to the Plugins tab and scroll down to Web services and press Overview.
* Follow the steps found there.

    1. Enable web services.
    2. Enable protocols, enable only the restful protocol.
    3. Create a specific user.
    4. Check user capability. (you can skip this)
    5. Select a service. Add a new service. Check Enabled and Authorized users only.
    6. Add functions. Add the functions you need.

    core_message_send_instant_messages
        This function is needed to send the messages to a user in Moodle. Used for every functionality that sends messages in Moodle.

    core_course_get_courses_by_field
        This function is needed to gather course information from Moodle for the course with the given ID. It is used for the inactivity check.

    core_enrol_get_enrolled_users
        This function is needed to gather all the enrolled users for a specific course. It is used for the inactivity and deadline check.

    core_completion_get_activities_completion_status
        This function is needed to gather the status of all activities for a specific user in a specific course. It is used for the deadline check.

    mod_assign_get_assignments
        This function is needed to get all the assignments for a specific course. It is used for the deadline check.

    core_course_get_courses
        This function is needed to get all the courses from Moodle. This is used to import them into Mofa.

    core_course_get_contents
        This function is needed to get all the contents from one course. This is used to import all the course contents into Mofa.

    core_enrol_get_enrolled_users_with_capability
        This function is needed to get all the teachers from all the courses.

    7. Select a specific user, press Authorised users and add your new user.
    8. Create a token for a user.
    9. Enable developer documentation.
    10. Test the service. (you can skip this)

    .. _token-creation:

* Go to ``Site administration`` |rarr| ``Users`` |rarr| ``Permissions`` |rarr| ``Define roles``.
* Click ``Add a new role``.
* Select ``Manager`` in the ``Use role or archetype`` field.
* Click Continue.
* Allow the Use RESTFUL Protocol option in ``Site administration`` |rarr| ``Users`` |rarr| ``Permission`` |rarr| ``Assign system roles``. Add the user to the new role.

xAPI Installation
***********************

To be able to link Moodle and Learning Locker to each other, the logstore xAPI plugin must be installed on Moodle. We use our own modified version of this plugin.

* Download `xapi.zip <https://github.com/uu-mofa/mofa/releases>`_.
* Open your Moodle instance, and navigate to ``Site administrations`` |rarr| ``Plugins`` |rarr| ``Install plugins``.
* Drag & drop the ``xapi.zip`` into the box.
* Follow the instructions in Moodle.
* When the installation has completed, you need the fill in the following fields. These are used to let the plugin know where it needs to send the xAPI statements:

**Endpoint**: fill in the location of the xAPI-endpoint. For the default Docker connection with Learning Locker, it is: http://172.30.0.8/data/xAPI/.

**Username**: fill in the ``Key`` of the client you created in the `Learning Locker configuration <learning-locker.html#creating-a-client>`_.

**Password**: fill in the ``Secret`` of the client you created in the `Learning Locker configuration <learning-locker.html#creating-a-client>`_.

After that, make sure the following boxes are checked:

* Send course and activity id number.
* Identify users by id.
* Send response choices.
* Click save.

Now we still need to enable the plugin:

* Scroll to the top of the page.
* Under your site name it will show: ``Dashboard / Site administration / Plugins / Logging / Logstore xAPI``. Click ``Logging``.
* This will show the available log stores.
* Click the |eye-slash| behind Logstore xAPI to enable it.

To test the configuration, log in to Moodle and view a course. These two actions should both result in Learning Locker receive an xAPI statement.

.. note:: Logstore xAPI has an option called ``Send statements by scheduled task?``. This will force Moodle to send the statements to Learning Locker in the background, via a cron task to avoid blocking page responses.
This will make the process less close to real time, but will help to prevent unpredictable Moodle performance linked to the performance of Learning Locker.

Manually creating the xAPI.zip
======================================
If you need to alter the xAPI plugin for some reason, you can do so as it is present in the xAPI folder. To create a new installation zip file, we need to manually create one. If this is not of your concern, you can skip this chapter.

Windows
------------

- Make sure git is installed.
- In ``/docker/zip-dependencies/``, copy ``zip.exe`` and ``bzip2.dll`` to ``C:\Program Files\Git\mingw64\bin\``.
- Make sure php is installed and present in PATH. Instructions here: `php manual <https://www.php.net/manual/en/install.windows.legacy.index.php#install.windows.legacy.manual>`_.
- Run ``create-zip.sh`` in your Docker folder with git bash.

Linux
------------

- Make sure php and zip are installed.
- Run ``./create-zip.sh``.
