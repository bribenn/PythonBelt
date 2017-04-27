from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^logout$', views.logout),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^remove/(?P<id>\d+)$', views.remove),
    url(r'^add_wish/(?P<id>\d+)$', views.add_wish),
    url(r'^create$', views.create),
    url(r'^add_item$', views.add_item),
    url(r'^products/(?P<id>\d+)$', views.show_product),

]