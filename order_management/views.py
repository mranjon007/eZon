import datetime

from django.views.generic import TemplateView, ListView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.forms import ModelForm
from django.contrib.auth.decorators import permission_required
from django.contrib.admin.views.decorators import staff_member_required

from .models import (
    Order,
    OrderProcessingDate,
    COMPANY_LISTING,
    COUNTRY_LIST,
    ORDER_STATUS,
    PAYMENT_STATUS,
    PAYMENT_WAY,
)

from .forms import (
    PriceQueryForm,
    PriceQueryUpdateForm,
    PlaceOrderForm,
)

from .CustomMixin import (
    IsStaffMixin,
    LogoutIfNotStaffMixin,
)

from user.models import CustomUser


def is_tuple_member(a_tuple, member):
    if member in (item[0] for item in a_tuple):
        return True
    else:
        return False


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
                new_order = Order.objects.create(product_url=order.product_url, product_country=order.product_company,
                                                 user=order.user)
                new_order_processing_dates = OrderProcessingDate.objects.create(order=new_order,
                                                                                status=new_order.status)
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
    template_name = 'order_management/admin_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['latest_articles'] = Article.objects.all()[:5]
        return context


class PriceQueryListView(IsStaffMixin, ListView):
    model = OrderProcessingDate
    template_name = 'order_management/price_query_list.html'

    def get_queryset(self):
        return OrderProcessingDate.objects.filter(order__status='price_query')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(PriceQueryListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context


@staff_member_required
def update_price_query(request, pk):
    """View function for update price Query"""
    order = get_object_or_404(Order, pk=pk)

    if request.method == 'POST':

        form = PriceQueryUpdateForm(request.POST)

        if form.is_valid():
            order.product_price = form.cleaned_data['product_price']
            order.product_tax = form.cleaned_data['product_tax']
            order.product_service_fee = form.cleaned_data['product_service_fee']
            if form.cleaned_data['admin_note']:
                order.admin_note = form.cleaned_data['admin_note']

            order_status_element = 'query_result_submitted'
            if is_tuple_member(ORDER_STATUS, order_status_element):
                order.status = order_status_element
            order.save()

            return HttpResponseRedirect(reverse('price-query-list'))

    # If this is a GET (or any other method) create the default form.
    else:
        form = PriceQueryUpdateForm()
    context = {
        'form': form,
        'order': order,
    }

    return render(request, 'order_management/price_query_update.html', context)


class PlacedOrderListView(IsStaffMixin, ListView):
    model = OrderProcessingDate
    template_name = 'order_management/placed_order_list.html'

    def get_queryset(self):
        return OrderProcessingDate.objects.filter(status='placed_order')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(PlacedOrderListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context


@staff_member_required
def place_order_form_view(request):
    """View function for place a new order"""
    if request.method == 'POST':

        form = PlaceOrderForm(request.POST)
        new_order = Order()
        new_customer = CustomUser()
        if form.is_valid():
            # get the cleaned order information
            new_order.product_url = form.cleaned_data['product_url']
            if is_tuple_member(COMPANY_LISTING, form.cleaned_data['product_company']):
                new_order.product_company = form.cleaned_data['product_company']
            if is_tuple_member(COUNTRY_LIST, form.cleaned_data['product_country'])
                new_order.product_country = form.cleaned_data['product_country']
            new_order.product_price = form.cleaned_data['product_price']
            new_order.product_tax = form.cleaned_data['product_tax']
            new_order.product_service_fee = form.cleaned_data['product_service_fee']
            if is_tuple_member(PAYMENT_STATUS, form.cleaned_data['payment_status']):
                new_order.payment_status = form.cleaned_data['payment_status']
            if form.cleaned_data['admin_note']:
                new_order.admin_note = form.cleaned_data['admin_note']
            if form.cleaned_data['customer_note']:
                new_order.customer_note = form.cleaned_data['customer_note']

            # get cleaned customer info
            new_customer.name = form.cleaned_data['customer_name']
            new_customer.phone_number = form.cleaned_data['customer_phone_number']
            new_customer.email = form.cleaned_data['customer_email_address']
            new_customer.address = form.cleaned_data['customer_address']

            order = Order.objects.create(product_url=new_order.product_url,
                                         product_country=new_order.product_country,
                                         product_company=new_order.product_company,
                                         product_price=new_order.product_price,
                                         product_tax=new_order.product_tax,
                                         product_service_fee=new_order.product_service_fee,
                                         payment_status=new_order.payment_status,
                                         admin_note=new_order.admin_note,
                                         customer_note=new_order.customer_note,
                                         )
            # change the order status
            updated_status = 'placed_order'
            order_processing_dates = OrderProcessingDate.objects.create(order=order,
                                                                        status=updated_status,
                                                                        )
            generated_password = 'AB12CD'
            user = CustomUser.objects.create(name=new_customer.name,
                                             email=new_customer.email,
                                             phone_number=new_customer.phone_number,
                                             address=new_customer.address,
                                             )
            # set the user password and save
            user.set_password(generated_password)
            user.save()
            # add user to the order
            order.user = user
            order.save()
            return HttpResponseRedirect(reverse('placed-order-list'))

    else:
        form = PlaceOrderForm()
    context = {
        'form': form,
    }

    return render(request, 'order_management/place_order_form.html', context)
