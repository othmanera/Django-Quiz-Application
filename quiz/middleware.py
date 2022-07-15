from django.urls import reverse
from django.http import Http404

class RestrictStaffToAdminMiddleware(object):
    """
    A middleware that restricts staff members access to administration panels.
    """
    def process_request(self, request):
        if request.path.startswith(reverse('admin:index')):
            if request.user.is_authenticated():
                if not request.user.is_staff:
                    raise Http404
            else:
                raise Http404