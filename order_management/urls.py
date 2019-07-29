from django.urls import path
from .views import (
    HomePageView,
    # SignUp,
)


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    # path('signup/', SignUp.as_view(), name='signup'),
]
