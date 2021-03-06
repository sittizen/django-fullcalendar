====================
django-fullcalendar
====================

A rewrite of atiberghien/django-fullcalendar-examples, using:
-----------------------------------------------
* Django 1.5
* llazzaro/django-scheduler
* Bower

Project is configured to use Vagrant (1.2.2) on VirtualBox (4.2.12) during development, tested with PyCharm on Ubuntu and MacOSX.


================
Deployment
================

To deploy this application, you need to follow these steps:
-----------------------------------------------------------

Local deployment::

    git clone https://github.com/sittizen/django-fullcalendar.git
    cd django-fullcalendar/bin
    python bootstrap.py [dev|production|staging|test]

default for the project environment is 'dev', environment types are:

 * 'dev' ( the usual stuff; embedded static files serving, debug toolbar, django extensions )
 * 'test' ( todo description )
 * 'staging' ( todo description )
 * 'production' ( todo description )

If using Vagrant:
-----------------

( note that currently VirtualBox 4.2.14 seems bugged and will fail when importing the vagrant box )::

    cd ..
    vagrant up

This initialize a virtual machine with a user 'django' (password 'd') providing a virtualenv connected to the project.
Debian packages are kept upgraded by the provisioning as long PRJ_DEB_UPGRADE=TRUE in .env file.
The same for Pip packages in the virtualenv with PRJ_PIP_UPGRADE=TRUE.

If not using Vagrant:
---------------------

TODO

When deploying:
---------------

TODO



================
Acknowledgements
================

    - https://github.com/atiberghien/django-fullcalendar-examples
    - https://github.com/llazzaro/django-scheduler
    - http://arshaw.com/fullcalendar/
