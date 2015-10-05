from django.conf.urls import url

from .views import add_reception

urlpatterns = [
    url(r'^$', add_reception, name='add_reception'),
]
