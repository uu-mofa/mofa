..    include:: <isonum.txt>

########################
Environment file
########################

Variables that need to be changed per developer or deployment are configurable in an .env file. Examples could be a Moodle API token, or the location of the Learning Locker server.
The repository contains an example version of the environment.

MOODLE_BASE_URL
    The URL of the Learning Locker instance is located without http or trailing forward slash.

MOODLE_URL
    The complete Moodle URL to the restful API.

MOODLE_TOKEN
    Moodle token is the token you generated in the `Moodle configuration step 8 <moodle.html#configuration>`_.

LL_URL
    The URL of the Learning Locker instance is located.

LL_AUTH_KEY
    The auth key for Learning Locker can be found in ``Learning Locker`` |rarr| ``Settings`` |rarr| ``Clients`` |rarr| ``<Client Name>`` |rarr| ``Use this Basic Auth value in your Authorization header for requests``
    It is the whole string, without the ``Basic`` at the front.

ORGANISATION
    The organisation is in the URL when you open your Learning Locker page. For example, it would be ``5de0d238565cfd001ecc1b90`` in http://Learning Locker/organisation/5de0d238565cfd001ecc1b90/data/dashboards.

DJANGO_PORT
    The port where the Mofa instance is located.

DJANGO_URL
    The URL where the Mofa instance is located.

TIME_ZONE
    The time zone of the place where the Mofa instance is located. See the list of `time zones <https://en.wikipedia.org/wiki/List_of_tz_database_time_zones>`_.

.. attention::
    Make sure you edit these to your environment specific values, do not just take the defaults!
