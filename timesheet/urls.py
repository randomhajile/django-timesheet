from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^job_form/$', views.JobCreate.as_view(), name='job_create'),
    url(r'^suggest_job/$', views.SuggestJob.as_view(), name='job_suggest'),
    url(r'^about/$', TemplateView.as_view(template_name='timesheet/about.html'), name='about'),
    url(r'^edit_job/(?P<pk>[a-z0-9\-]+)/$', views.JobEdit.as_view(), name='edit_job'),
    url(r'^delete_job/(?P<pk>[a-z0-9\-]+)/$', views.JobDelete.as_view(), name='delete_job'),
    url(r'^edit_time/(?P<pk>[0-9]+)/$', views.TimeEdit.as_view(), name='edit_time'),
    url(r'^delete_time/(?P<pk>[0-9]+)$', views.TimeDelete.as_view(), name='delete_time'),
    url(r'^(?P<pk>[a-z0-9\-]+)/$', views.JobDetailView.as_view(), name='detail'),
    url(r'^time/(?P<pk>[a-z0-9\-]+)$', views.TimeEntryView.as_view(), name='time'),
    url(r'^(?P<pk>[a-z0-9\-]+)/invoice/$', views.InvoiceView.as_view(), name='invoice'),
    url(r'^(?P<pk>[a-z0-9\-]+)/invoice/(?P<start>\d{2}-\d{2}-\d{4})/(?P<end>\d{2}-\d{2}-\d{4})/$', views.ItemizedInvoice.as_view(), name='itemized_invoice'),
]
