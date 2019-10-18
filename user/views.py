from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm, PhoneNumberVerificationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
import random
from zeep import Client

from .models import (
    PhoneNumberVerification,
    CustomUser,
    CustomUserProfile,
)
from .forms import (
    CustomUserProfileForm
)


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


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            verification_instance = PhoneNumberVerification.objects.filter(user=user).first()
            if verification_instance.is_verified is not True:
                return redirect(reverse('verify-phone-number', kwargs={'user_id': user.id}))
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})



@login_required
def update_user_profile(request):
    context = {}
    user = request.user
    profile, is_created = CustomUserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = CustomUserProfileForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            address_line_1 = form.cleaned_data.get('address_line_1')
            address_line_2 = form.cleaned_data.get('address_line_2')
            city = form.cleaned_data.get('city')
            district = form.cleaned_data.get('district')
            postcode = form.cleaned_data.get('postcode')

            # update name of the user
            custom_user = CustomUser.objects.filter(id=user.id).first()
            custom_user.name = name
            custom_user.save()

            # update CustomUserProfile
            profile.address_line_1 = address_line_1
            profile.address_line_2 = address_line_2
            profile.city = city
            profile.district = district
            profile.postcode = postcode
            profile.save()

            form = CustomUserProfileForm(initial={
                'email': custom_user.email,
                'name': custom_user.name,
                'phone_number': custom_user.phone_number,
                'address_line_1': profile.address_line_1,
                'address_line_2': profile.address_line_2,
                'city': profile.city,
                'district': profile.district,
                'postcode': profile.postcode}
            )
            context['form'] = form
            context['message'] = "Updated Successfully"
            return render(request, 'user/user_profile.html', context=context)
    else:
        form = CustomUserProfileForm(initial={
                                     'email': user.email,
                                     'name': user.name,
                                     'phone_number': user.phone_number,
                                     'address_line_1': profile.address_line_1,
                                     'address_line_2': profile.address_line_2,
                                     'city': profile.city,
                                     'district': profile.district,
                                     'postcode': profile.postcode}
                                     )
        print(form)
        context['form'] = form
    return render(request, 'user/user_profile.html', context=context)


def verify_phone_number(request, user_id):
    context = {}
    user = CustomUser.objects.filter(id=user_id).first()
    print("---------- "+user.phone_number)
    context['user'] = user
    verification_instance = PhoneNumberVerification.objects.filter(user=user).first()

    if request.method == 'GET':
        form = PhoneNumberVerificationForm()
        context['form'] = form
        if verification_instance is None or verification_instance.count < 5:
            code = random.randint(1000, 9999)
            print(code)
            verification_instance, is_created =\
                PhoneNumberVerification.objects.get_or_create(user=user,
                                                              )

            verification_instance.verification_code = code
            # is_sent = send_verificaiton_code(user.phone_number)
            verification_instance.count += 1
            verification_instance.save()
            #send_code(user_id)
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
                verification_instance.save()
                return HttpResponseRedirect(reverse('user-dashboard', kwargs={'user_id': user.id}))
            else:
                context["message"] = "Code is not match"
                print(context["message"])
                return render(request, template_name='user/phone_number_verification.html',
                              context=context)


def send_code(user_id, phone_number, code):
    url = 'https://api2.onnorokomsms.com/sendsms.asmx?WSDL'
    client = Client(url)
    user_name = '01680139372'
    password = 'Life@123!'
    recipient_number = phone_number
    sms_text = str(code)
    sms_type = 'TEXT'
    mask_name = ''
    campaign_name = ''
    response = client.service.OneToOne(user_name, password, recipient_number, sms_text, sms_type, mask_name, campaign_name)
    print(response)



