487-Project
===========

487 Video Uploading Project

Django install instructions: https://docs.djangoproject.com/en/dev/topics/install/

To start, navigate to the CS487Project folder, containing manage.py, and run the following command:

./manage.py syncdb
When prompted to set up a superuser account, type "no"

This creates the SQL database. Then run:

./manage.py runserver

Open a web browser and navigate to one of the following addresses:

For admin functions: http://127.0.0.1:8000/admin
For video/user functions: http://127.0.0.1:8000/videos

The superuser to access the administrative functions is:
Username: su
Password: su

A normal user
Username: nu
Password: nu

An uploader
Username: up
Password: up

In order to use keywords, journals, and authors with video uploads, the admin must add them to the master list of the respective type, under the admin functions page.