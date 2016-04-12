from django.conf.urls import include, url
from voting import views

urlpatterns = [
    url(r'^$', views.poll_list, name='poll_list'),
]
