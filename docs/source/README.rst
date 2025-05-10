StadtBank
=========

.. image:: https://img.shields.io/badge/Conventional%20Commits-1.0.0-%23FE5196?logo=conventionalcommits&logoColor=white
   :target: https://conventionalcommits.org
   :alt: Conventional Commits

`Documents <https://oemersak.me/StadtBank/>`_

Basic Bank System with Web GUI and database.

Setup
-----

Create Environment (Optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To create a virtual environment, run the following command:

Activate virtual environment (for Unix-based systems)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: shell

   python -m venv .venv
   source .venv/bin/activate

Activate virtual environment (for Windows)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: shell

   python -m venv .venv
   .venv\scripts\activate

Install Requirements
~~~~~~~~~~~~~~~~~~~~

Install the required Python Modules:

.. code-block:: shell

   python -m pip install -r requirements.txt

Create Database
---------------

To set up the database, perform the following step:

- Show up to migration files:

.. code-block:: shell

   python manage.py migrate

Data Samples
------------

You can use the `bin/randCus.py <bin/randCus.py>`_ and `bin/randAct.py <bin/randAct.py>`_ for generating sample data for your database.

Running Server
--------------

After all setup, you can run the program with:

.. code-block:: shell

   python manage.py runserver

.. note::
   Use ``--insecure`` if you can't get Static Files.

Admin GUI
---------

To access the admin GUI, you need to create a superuser account first. Run the following command:

.. code-block:: shell

   python manage.py createsuperuser

.. note::
   Or you can run `bin/userSetup.py <bin/userSetup.py>`_ for Account Setup.

For access, go to ``http://IP_ADDRESS/admin``

.. warning::
   Please ensure that your database migrations are applied before running the ``createsuperuser`` command.

Compile Languages
-----------------

StadtBank has a multi-language system. You can find the translations in `Bank/locale <Bank/locale/>`_.
You need to compile them to see translations:

.. code-block:: shell

   python manage.py compilemessages

Improve or add Translations
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Improve Translations
^^^^^^^^^^^^^^^^^^^^

You can change the ``msgstr`` in the ``*.po`` files. Every text has a ``msgid`` and you can see where it is used above it.

Add Translations
^^^^^^^^^^^^^^^^

.. code-block:: shell

   python manage.py makemessages -l LANGUAGE_CODE

HTTPS Server
------------

It is still in development. I'm not very good with it. Up to now I only did what I found on the internet for it.
You can find the links in `settings.py`.

Create Certificates
~~~~~~~~~~~~~~~~~~~

You can run this command:

.. code-block:: shell

   openssl req -x509 -newkey rsa:4096 -keyout certs/server.key -out certs/server.pem -days 365 -nodes

Or you can use `certs/file.sh <certs/file.sh>`_ for CA certificate.

.. warning::
   CHECK THE CONFIGURATION IN `certs/file.sh <certs/file.sh>`_ BEFORE RUN IT !!!

Run Server
~~~~~~~~~~

.. code-block:: shell

   python manage.py runserver_plus --cert-file certs/server.pem --key-file certs/server.key --insecure 127.0.0.1:443
