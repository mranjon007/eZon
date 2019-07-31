from django.contrib.auth.mixins import UserPassesTestMixin


# Check if the user is a staff
class IsStaffMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

