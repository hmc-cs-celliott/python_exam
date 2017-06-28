from django.conf.urls import url
from . import views           
urlpatterns = [
url(r'^$', views.index), 
url(r'^login_attempt$', views.login_attempt),
url(r'^register_attempt$', views.register_attempt),
url(r'^travels', views.travels), #goes to main page w recent reviews
url(r'^trip/(?P<trip_id>\d+)', views.trip),
url(r'^join_trip/(?P<trip_id>\d+)', views.join_trip),
url(r'^add_trip$', views.add_trip),
url(r'^add_attempt$', views.add_attempt),
url(r'^logout$', views.logout),
]