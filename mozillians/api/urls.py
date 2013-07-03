from django.conf.urls.defaults import include, patterns, url

from tastypie.api import Api

import mozillians.users.api

v1_api = Api(api_name='v1')
v1_api.register(mozillians.users.api.UserResource())

urlpatterns = patterns('',
    url(r'', include(v1_api.urls)),
)
