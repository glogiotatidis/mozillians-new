import re

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.urlresolvers import is_valid_path, reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

from tower import ugettext as _

from mozillians.common.middleware import safe_query_string


class RegisterMiddleware():
    """Redirect authenticated users with incomplete profile to register view."""
    def process_request(self, request):
        user = request.user
        path = request.path
        allow_urls = [r'^/[\w-]+{0}'.format(reverse('phonebook:logout')),
                      r'^/[\w-]+{0}'.format(reverse('browserid_logout')),
                      r'^/[\w-]+{0}'.format(reverse('phonebook:register')),
                      r'^/[\w-]+/jsi18n/']

        if settings.DEBUG:
            allow_urls.append(settings.MEDIA_URL)

        if (user.is_authenticated() and not user.userprofile.is_complete
            and not filter(lambda url: re.match(url, path), allow_urls)):
            messages.warning(request, _('Please complete registration '
                                        'before proceeding.'))
            return redirect('phonebook:register')


class UsernameRedirectionMiddleware():
    """
    Redirect requests for user profiles from /<username> to
    /u/<username> to avoid breaking profile urls with the new url
    schema.

    """

    def process_response(self, request, response):
        if (response.status_code == 404
            and not request.path_info.startswith('/u/')
            and not is_valid_path(request.path_info)
            and User.objects.filter(
                username__iexact=request.path_info[1:].strip('/')).exists()
            and request.user.is_authenticated()
            and request.user.userprofile.is_vouched):

            newurl = '/u' + request.path_info
            if request.GET:
                with safe_query_string(request):
                    newurl += '?' + request.META['QUERY_STRING']
            return HttpResponseRedirect(newurl)
        return response
