from django.contrib.auth.mixins import UserPassesTestMixin, AccessMixin
from django.contrib.auth import logout


# Check if the user is a staff
class IsStaffMixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_staff:
            return True
        else:
            False


class LogoutIfNotStaffMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            logout(request)
            return self.handle_no_permission()
        return super(LogoutIfNotStaffMixin, self).dispatch(request, *args, **kwargs)

