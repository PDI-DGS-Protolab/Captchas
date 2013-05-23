from django.conf.urls import patterns, include, url
import mollom.views as mollom
import recaptcha.views as recaptcha

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^mollom/$', mollom.serveCaptcha),
                       url(r'^mollom/check$', mollom.checkCaptcha),
                       url(r'^recaptcha/$', recaptcha.serveCaptcha),
                       url(r'^recaptcha/check$', recaptcha.checkCaptcha),
    # Examples:
    # url(r'^$', 'captchas.views.home', name='home'),
    # url(r'^captchas/', include('captchas.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
