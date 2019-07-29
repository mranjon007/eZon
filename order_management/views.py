from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView


#from .forms import CustomUserCreationForm


class HomePageView(TemplateView):
    template_name = 'order_management/home.html'


# class SignUp(CreateView):
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy('login')
#     template_name = 'registration/signup.html'

