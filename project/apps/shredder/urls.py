from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('project.apps.shredder.views',
    url(r'pair_api/', 'pair_api', name='pair_api'),
    url(r'vote/', 'vote', name='vote'),
)
