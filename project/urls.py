from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

admin.autodiscover()
urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    # Homepage
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    (r'^shredder/', include('project.apps.shredder.urls')),
)

# Static URLs
urlpatterns += staticfiles_urlpatterns()
