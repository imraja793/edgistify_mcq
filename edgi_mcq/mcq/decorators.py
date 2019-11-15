from django.core.exceptions import PermissionDenied
from mcq.models import UserProfile


def user_is_applicant(function):
    def wrap(request, *args, **kwargs):
        if request.user.user_profile.applicant == True:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap


def user_is_admin(function):
    def wrap(request, *args, **kwargs):
        if request.user.user_profile.applicant == False:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap
