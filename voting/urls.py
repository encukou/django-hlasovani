from django.conf.urls import url
from voting import views

urlpatterns = [
    url(r'^$', views.poll_list, name='poll_list'),
    url(r'^polls/(?P<pk>\d+)$', views.poll_detail, name='poll_detail'),
]
