import datetime

from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import(
    Order,
    OrderProcessingDate,
)

from user.models import (
    CustomUser,
)

from .forms import (
    PriceQueryForm,
)

from .CustomMixin import (
    IsStaffMixin,
)


def homepage(request):
    context = {}
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = PriceQueryForm(request.POST)
            if form.is_valid():
                order = Order()
                order.product_url = form.cleaned_data['product_url']
                if form.cleaned_data['product_company']:
                    order.product_company = form.cleaned_data['product_company']
                order.user = request.user
                print('user name : {}', order.user.email)
                new_order = Order.objects.create(product_url=order.product_url, product_country=order.product_company, user=order.user)
                return HttpResponseRedirect(reverse('login'))  # user-dashboard e return korbe
        else:
            context['message'] = 'Please Login/Register to place a product price Query'

    form = PriceQueryForm()
    print(form)
    context['form'] = form
    return render(request, template_name='order_management/home.html', context=context)


# class HomePageView(TemplateView):
#     template_name = 'order_management/home.html'


class AdminDashBoardView(LoginRequiredMixin, IsStaffMixin, TemplateView):
    template_name = 'order_management/admin_dashboard'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['latest_articles'] = Article.objects.all()[:5]
        return context


