from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm, PhoneNumberVerificationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from .models import PhoneNumberVerification, CustomUser
from django.urls import reverse
import random
# print(random.randint(1,101))


class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=email, password=raw_password)
            #login(request, user)
            return HttpResponseRedirect(reverse('verify-phone-number', kwargs={'user_id': user.id}))
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def user_profile(request):
    pass


def verify_phone_number(request, user_id):
    context = {}
    user = CustomUser.objects.filter(id=user_id).first()
    context['user'] = user
    verification_instance = PhoneNumberVerification.objects.filter(user=user).first()

    if request.method == 'GET':
        form = PhoneNumberVerificationForm()
        context['form'] = form
        if verification_instance is None or verification_instance.count < 5:
            #code = random.randint(1000, 9999)
            code = 4444
            verification_instance, is_created =\
                PhoneNumberVerification.objects.get_or_create(user=user,
                                                              )

            verification_instance.verification_code = code
            # is_sent = send_verificaiton_code(user.phone_number)
            verification_instance.count += 1
            verification_instance.save()
        else:
            context['message'] = "We sent verification code to your phone for 5 times already. Please Call eZon support for more information"
        return render(request, template_name='user/phone_number_verification.html',
                      context=context)
    else:
        form = PhoneNumberVerificationForm(request.POST)
        if form.is_valid():
            verification_code = form.cleaned_data.get('verification_code')

            if str(verification_instance.verification_code) == verification_code:
                login(request, user)
                verification_instance.is_verified = True
                return HttpResponseRedirect(reverse('user-dashboard', kwargs={'user_id': user.id}))
            else:
                context["message"] = "Code is not match"
                print(context["message"])
                return render(request, template_name='user/phone_number_verification.html',
                              context=context)


# def send_code(request, )



