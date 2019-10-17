from django.urls import path
from .views import (
    signup,
    SignUp,
)


urlpatterns = [
    path('signup/', signup, name='signup'),
]
