from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'query$', 'config.sg-app.query'), #ending with url pattern should be used
    url(r'refresh$', 'config.sg-app.refresh'), #ending with url pattern should be used
    url(r'blocktableupdate$', 'config.sg-app.blocktableupdate'), #ending with url pattern should be used
    url(r'busstoptableupdate$', 'config.busdata.busstoptableupdate'), #ending with url pattern should be used
    url(r'busroutetableupdate$', 'config.busdata.busroutetableupdate'), #ending with url pattern should be used
    url(r'route$', 'config.sg-app.refreshRoute'),
)
