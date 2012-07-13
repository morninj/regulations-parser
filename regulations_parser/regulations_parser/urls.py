from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'regulations_parser.views.home', name='home'),
    # url(r'^regulations_parser/', include('regulations_parser.foo.urls')),
    url(r'^$', 'parser_tools.views.index'),
    url(r'^tools/$', 'parser_tools.views.index'),
    url(r'^tools/scrape/$', 'parser_tools.views.scrape'),
    url(r'^tools/review/$', 'parser_tools.views.review'),
    url(r'^tools/add-by-hand/$', 'parser_tools.views.add_by_hand'),
    url(r'^tools/flush/$', 'parser_tools.views.flush'),
    url(r'^tools/edit-incorporation/$', 'parser_tools.views.edit_incorporation'),
    url(r'^tools/edit-incorporation/(?P<pk>\d+)/$', 'parser_tools.views.edit_incorporation'),
    url(r'^tools/update-incorporation/(?P<pk>\d+)/$', 'parser_tools.views.update_incorporation'),
    url(r'^tools/edit-standards-organization/$', 'parser_tools.views.edit_standards_organization'),
    url(r'^tools/edit-standards-organization/(?P<pk>\d+)/$', 'parser_tools.views.edit_standards_organization'),
    url(r'^tools/edit-regulation/$', 'parser_tools.views.edit_regulation'),
    url(r'^tools/edit-regulation/(?P<pk>\d+)/$', 'parser_tools.views.edit_regulation'),
    url(r'^tools/delete-regulation/(?P<pk>\d+)/$', 'parser_tools.views.delete_regulation'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
