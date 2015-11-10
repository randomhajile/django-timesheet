Timesheet
---------

Timesheet is a simple Django app for invoicing built as a code challenge for Hire an Esquire. The requirements were

 * "TimeEntry" CRUD (Create/Read/Update/Delete) for model with follow fields:
     * Time spent in minutes
     * Date of entry
     * Summary of work completed
     * Associated job (via UUID)

 * "Job" CRUD for model with fields:
     * Title
     * Hourly rate
     * Tax rate

 * Dynamic creation of "Invoice" parameterized on job and date range returning the following fields:
     * Job
     * Date range
     * Time entries in range
     * $ subtotal (hourly_rate * total_minutes/60)
     * $ tax (subtotal * tax_rate)
     * $ total

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
3. Run `python manage.py migrate` to create the models.

4. Visit http://127.0.0.1:8000/timesheet/

Installation Instructions
-------------------------
1. Clone this repository.

2. Run `python setup.py sdist`.

3. Install the package using `pip install django-timesheet/dist/django-timesheet-0.1.tar.gz`.

4. Follow the Quick Start section.
