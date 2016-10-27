from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^add$', views.add, name="add" ),
    url(r'^process$', views.process, name='process'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^destination/(?P<trip_id>\d+)$', views.destination, name='destination'),
    url(r'^destination/join/(?P<trip_id>\d+)$', views.join, name='join'),
    url(r'^delete/(?P<trip_id>\d+)$', views.delete, name='delete'),
    url(r'^cancel/(?P<trip_id>\d+)$', views.cancel, name='cancel')
]
