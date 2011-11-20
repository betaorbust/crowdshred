from django.conf.urls.defaults import patterns, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

admin.autodiscover()
urlpatterns = patterns('',
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	(r'^admin/', include(admin.site.urls)),
	# Homepage
	(r'^$', TemplateView.as_view(template_name='homepage.html')),
)

# Static URLs
urlpatterns += staticfiles_urlpatterns()
