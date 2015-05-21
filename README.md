Timesheet
---------

Timesheet is a simple Django app for invoicing.

Quick Start
-----------

1. Add "timesheet" to your INSTALLED_APPS setting like this::
```
    INSTALLED_APPS = (
        ...
        'timesheet',
    )
```
2. Include the timesheet URLconf in your project urls.py like this:
```
    url(r'^timesheet/', include('timesheet.urls', namespace='timesheet')),
```
3. Run `python manage.py migrate` to create the polls models.

4. Visit http://127.0.0.1:8000/timesheet/ to participate in the poll.

Installation Instructions
-------------------------
1. Clone this repository.

2. Run `python setup.py sdist`.

3. Install the package using `pip install django-timesheet/dist/django-timesheet-0.1.tar.gz`.

4. Follow the Quick Start section.