from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm, PhoneNumberVerificationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
import random
print(random.randint(1,101))


class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(user)
            login(request, user)
            send()
            return redirect('phone-number-verification')
            # username = form.cleaned_data.get('username')
            # raw_password = form.cleaned_data.get('password1')
            # user = authenticate(username=username, password=raw_password)
            # user.username = username
            # user.password = set_password(raw_password)
            # login(request, user)

            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def verify_phone_number(request, user_id):
    context = {}
    user = User.objects.get(user_id)
    context['user'] = user
    verification_instance = PhoneNumberVerificationForm.objects.filters(user=user)

    if verification_instance.is_varified is not None:
        context['message'] = "this phone number is not verified"
    else:
        if request.POST & is_verified is None:
            form = PhoneNumberVerificationForm(request.POST)
            if form.is_valid():
                verification_code = form.cleaned_data['verification_code']

                PhoneNumberVerification.objects.create(user=user,
                                                       verification_code=verification_code,
                                                       )
                return HttpResponseRedirect(reverse('login'))

        else:
            form = ProductSendToDeliveryForm()

            context['form'] = form
            return render(request, template_name='user/phone_number_verification.html',
                          context=context)


# def send_code(request, )

