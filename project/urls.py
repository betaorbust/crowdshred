from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

admin.autodiscover()
urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    # Homepage
    url(r'^$', TemplateView.as_view(template_name='homepage.html'), name='index'),
    (r'^shredder/', include('project.apps.shredder.urls')),
    (r'^auth/', include('social_auth.urls')),
    # testing hacks
    # url(r'^game/', TemplateView.as_view(template_name='game.html'), name='game'),
    url(r'^game/$', 'project.apps.shredder.views.game', name='game'),
    url(r'^login/$', 'project.apps.shredder.views.login', name='login'),
    url(r'^about/', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^faq/', TemplateView.as_view(template_name='faq.html'), name='faq'),
    url(r'^winnings/', TemplateView.as_view(template_name='winnings.html'), name='winnings'),
    #git testing
    #url(r'^login/', TemplateView.as_view(template_name='login.html'), name='login'),
)

# Static URLs
urlpatterns += staticfiles_urlpatterns()
