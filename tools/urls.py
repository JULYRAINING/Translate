from django.conf.urls import url
from . import views
app_name = 'tools'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^long/$', views.index_long, name='index_long'),
    url(r'^translate/(?P<material>[a-zA-Z]+)/$', views.translate, name = 'translate'),
    url(r'^saveRecord/$', views.saveRecord, name = 'save')
]