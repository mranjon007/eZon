from django.urls import path
from .views import (
    login_view,
    signup,
    SignUp,
    verify_phone_number,
    update_user_profile,
)


urlpatterns = [
    path('signup/', signup, name='signup'),
    path('verify_phone_number/<int:user_id>/', verify_phone_number, name='verify-phone-number'),
    path('user_profile/', update_user_profile, name='user-profile'),
    path('login/', login_view, name='login')
]
