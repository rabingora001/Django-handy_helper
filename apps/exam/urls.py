from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$', views.index),
    url(r'^registration$', views.registration_process),
    url(r'^login$', views.login_process),
    url(r'^dashboard$', views.dashboard),
    url(r'^addJob$', views.addJob),
    url(r'^add_job$', views.add_job),
    url(r'^user_job/(?P<id>[0-9]+)$', views.user_job),
    url(r'^edit_job_page/(?P<id>[0-9]+)$', views.edit_job_page),
    url(r'^edit_job_page/edit_job/(?P<id>[0-9]+)$', views.edit_job),
    # url(r'^edit_job/(?P<id>[0-9]+)$', views.edit_job),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    # url(r'^claim/(?P<id>\d+)$', views.claim),
    url(r'^log_off$', views.log_off),
]