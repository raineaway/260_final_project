from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'list.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url('', include('lists.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
