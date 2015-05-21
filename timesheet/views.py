import datetime
from decimal import Decimal
import uuid

from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from django.views.generic.base import TemplateView

from .models import Job, TimeEntry

class IndexView(ListView):
    template_name = 'timesheet/index.html'
    context_object_name = 'job_list'

    def get_queryset(self):
        return Job.objects.all().order_by('-date_added')


class JobDetailView(DetailView):
    model = Job
    template_name = 'timesheet/detail.html'

    def get_queryset(self):
        return Job.objects.filter(date_added__lte=timezone.now())

    def get_context_data(self, **kwargs):
        context = super(JobDetailView, self).get_context_data(**kwargs)
        context['times'] = self.time_events()
        return context

    def time_events(self):
        return tuple(TimeEntry.objects.filter(job=self.kwargs.get('pk')).order_by('-date'))


class TimeEntryView(CreateView):
    model = TimeEntry
    template_name = 'timesheet/time.html'
    fields = ['date',
              'total_time',
              'summary']

    def form_valid(self, form):
        self.update_job(form)
        return super(TimeEntryView, self).form_valid(form)

    def update_job(self, form):
        job = get_object_or_404(Job, uuid=self.kwargs.get('pk'))
        form.instance.job = job
        job.last_activity = timezone.now()
        job.save()

    def get_success_url(self):
        return reverse('timesheet:index')


class InvoiceView(DetailView):
    model = Job
    template_name = 'timesheet/invoice.html'

    def get_context_data(self, **kwargs):
        context = super(InvoiceView, self).get_context_data(**kwargs)
        self.start = None
        self.end = None
        context.update(self.extra_values())
        return context

    def extra_values(self):
        res = {}
        res.update(self.time_events())
        res['subtotal'] = self.object.hourly_rate * (res['total_time']/60.0)
        res['tax'] = res['subtotal'] * self.object.tax_rate
        res['total'] = res['subtotal'] + res['tax']
        return res

    def time_events(self):
        times = TimeEntry.objects.filter(job=self.kwargs.get('pk')).order_by('-date')
        if self.start is not None:
            times = times.filter(date__gte=self.start)
        if self.end is not None:
            times = times.filter(date__lt=self.end)
        start_date = self.get_start_date(times)
        end_date = self.get_end_date(times)
        date_range = [time.date for time in times]
        total_time = sum([time.total_time for time in times])
        times = [(time, int(round(float(time.total_time)/total_time, 2)*100)) for time in times]
        res = {}
        res['start_date'] = start_date
        res['end_date'] = end_date
        res['total_time'] = total_time
        res['times'] = times
        return res

    def get_start_date(self, times):
        if self.start:
            return self.start
        if times:
            return min([time.date for time in times]).date
        return timezone.now()

    def get_end_date(self, times):
        if self.end:
            return self.end
        if times:
            return max([time.date for time in times]).date
        return timezone.now()


class ItemizedInvoice(InvoiceView):
    model = Job
    template_name = 'timesheet/itemized_invoice.html'

    def get_context_data(self, **kwargs):
        self.set_dates()
        context = super(DetailView, self).get_context_data(**kwargs)
        context.update(self.extra_values())
        return context

    def set_dates(self):
        self.start = datetime.datetime.strptime(self.kwargs.get('start'), '%m-%d-%Y')
        self.end = datetime.datetime.strptime(self.kwargs.get('end'), '%m-%d-%Y')
        self.end += datetime.timedelta(days=1)
        self.end = self.end.replace(hour=0, minute=0, second=0, microsecond=0)


class JobCreate(CreateView):
    model = Job
    fields = ['title',
              'hourly_rate',
              'tax_rate']

    def get_success_url(self):
        return reverse('timesheet:index')


class JobEdit(UpdateView):
    template_name = 'timesheet/edit_job.html'
    model = Job
    fields = ['title',
              'hourly_rate',
              'tax_rate']

    def get_success_url(self):
        return reverse('timesheet:index')

    def get_context_data(self, **kwargs):
        context = super(JobEdit, self).get_context_data(**kwargs)
        context['times'] = self.time_events()
        return context

    def time_events(self):
        return tuple(TimeEntry.objects.filter(job=self.kwargs.get('pk')).order_by('-date'))


class TimeEdit(UpdateView):
    template_name = 'timesheet/edit_time.html'
    model = TimeEntry
    fields = ['total_time',
              'summary']

    def get_success_url(self):
        return reverse('timesheet:index')


class JobDelete(DeleteView):
    template_name = 'timesheet/delete_job.html'
    model = Job

    def get_success_url(self):
        return reverse('timesheet:index')


class TimeDelete(DeleteView):
    template_name = 'timesheet/delete_time.html'
    model = TimeEntry

    def get_success_url(self):
        job = get_object_or_404(TimeEntry, id=self.kwargs.get('pk')).job
        return reverse('timesheet:edit_job', kwargs={'pk': job.uuid})


class SuggestJob(ListView):
    template_name = 'timesheet/jobs_grid.html'
    context_object_name = 'job_list'

    def get_queryset(self):
        if self.request.method == 'GET':
            contains = self.request.GET['suggestion']
        suggested_jobs = self.get_job_list(0, contains)
        return suggested_jobs

    def get_job_list(self, max_results=0, contains=''):
        if contains:
            # suggested_jobs = Job.objects.filter(title__istartswith=starts_with)
            suggested_jobs = Job.objects.filter(title__icontains=contains)
        else:
            suggested_jobs = Job.objects.all()
        if max_results:
            suggested_jobs = suggested_jobs[:max_results]
        return suggested_jobs
