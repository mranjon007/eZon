from django.urls import path
from .views import (
    signup,
    SignUp,
    verify_phone_number,
    user_profile,
)


urlpatterns = [
    path('signup/', signup, name='signup'),
    path('verify_phone_number/<int:user_id>/', verify_phone_number, name='verify-phone-number'),
    path('user_profile/', user_profile, name='user-profile'),
]
