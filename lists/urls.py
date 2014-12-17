from django.conf.urls import patterns, url

from lists import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^signup', views.signup, name='signup'),
    url(r'^signin', views.signin, name='signin'),
    url(r'^signout', views.signout, name='signout'),
    url(r'^create_item', views.create_item, name='create_item'),
    url(r'^check_item', views.check_item, name='check_item'),
    url(r'^delete_test', views.delete_test, name='delete_test'),
)
