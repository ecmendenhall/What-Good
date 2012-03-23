from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.views import login, logout
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from whatgood.views import todaysgood, done_today, done_all, about, landing_page, delete_today, delete_all, show_allthethings
from whatgood.forms import UserProfileForm
from goodthings.models import GoodThing
import profiles
import registration 

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^$', landing_page),
	(r'^allthings/$', show_allthethings),
	(r'^about/$', about),
	(r'^login/$', login),
	(r'^logout/$', logout),
	(r'^todaysgood/$', todaysgood),
	(r'^accounts/', include('registration.urls')),
	('^profiles/edit', 'profiles.views.edit_profile', {'form_class': UserProfileForm,}),
	(r'^profiles/', include('profiles.urls'),),
	(r'^todaysgood/done/(on|off)/(\d*)/$', done_today),
	(r'^allthings/done/(on|off)/(\d*)/$', done_all),
	(r'^todaysgood/delete/(\d*)/$', delete_today),
	(r'^allthings/delete/(\d*)/$', delete_all),
	
	
    # Examples:
    # url(r'^$', 'whatgood.views.home', name='home'),
    # url(r'^whatgood/', include('whatgood.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()