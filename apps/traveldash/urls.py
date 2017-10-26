from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^main$', views.index),
    url(r'^register$', views.register),
    url(r'^trips$', views.trips),
    url(r'^add$', views.add),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^addtrip$', views.addtrip),
    url(r'^join/(?P<trip_id>\d+)$', views.jointrip)
]
