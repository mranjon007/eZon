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
    ProductPurchaseCancelFrom,
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
                new_order = Order.objects.create(product_url=order.product_url,
                                                 product_country=order.product_company,
                                                 user=order.user)
                new_order_processing_dates = \
                    OrderProcessingDate.objects.create(order=new_order,
                                                       status=new_order.status)
                return HttpResponseRedirect(reverse('login'))  # user-dashboard e return korbe
        else:
            context['message'] = 'Please Login/Register to place a product price Query'

    form = PriceQueryForm()
    print(form)
    context['form'] = form
    return render(request, template_name='order_management/home.html', context=context)


class AdminDashBoardView(LoginRequiredMixin, IsStaffMixin, TemplateView):
    template_name = 'order_management/admin_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['latest_articles'] = Article.objects.all()[:5]
        return context


class PriceQueryListView(IsStaffMixin, ListView):
    model = Order
    template_name = 'order_management/price_query_list.html'

    def get_queryset(self):
        return Order.objects.filter(status='price_query')

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
            order.admin_note = form.cleaned_data['admin_note']

            order_status = 'price_query_submitted'
            if is_tuple_member(ORDER_STATUS, order_status):
                order.status = order_status
            order.save()
            OrderProcessingDate.objects.create(order=order, status=order.status)
            return HttpResponseRedirect(reverse('price-query-list'))

    # If this is a GET (or any other method) create the default form.
    else:
        form = PriceQueryUpdateForm()
    context = {
        'form': form,
        'order': order,
    }

    return render(request, 'order_management/price_query_update.html', context)


class PriceQuerySubmittedList(IsStaffMixin, ListView):
    model = Order
    template_name = 'order_management/price_query_submitted_list.html'

    def get_queryset(self):
        return Order.objects.filter(status='price_query_submitted')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(PriceQuerySubmittedList, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context


class PlacedOrderListView(IsStaffMixin, ListView):
    model = Order
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
            if is_tuple_member(COUNTRY_LIST, form.cleaned_data['product_country']):
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

            generated_password = 'AB12CD'
            # check if the email or phone number already exist. later only phone check will work
            user, is_created = \
                CustomUser.objects.get_or_create(email=new_customer.email,
                                                 )
            user.phone_number = new_customer.phone_number
            user.address = new_customer.address
            user.name = new_customer.name
            # set the user password and save
            user.set_password(generated_password)
            user.save()
            print(user.phone_number)
            order = Order.objects.create(product_url=new_order.product_url,
                                         product_country=new_order.product_country,
                                         product_company=new_order.product_company,
                                         product_price=new_order.product_price,
                                         product_tax=new_order.product_tax,
                                         product_service_fee=new_order.product_service_fee,
                                         payment_status=new_order.payment_status,
                                         admin_note=new_order.admin_note,
                                         customer_note=new_order.customer_note,
                                         user=user,
                                         status='product_purchase_request',
                                         )

            # change the order status to placed order
            updated_status = 'placed_order'
            new_order_processing_date = OrderProcessingDate.objects.create(order=order,
                                                                           status=updated_status)
            # change the order status to product purchase request
            updated_status = 'product_purchase_request'
            new_order_processing_date = OrderProcessingDate.objects.create(order=order,
                                                                           status=updated_status)
            return HttpResponseRedirect(reverse('placed-order-list'))
    else:
        form = PlaceOrderForm()
    context = {
        'form': form,
    }
    return render(request, 'order_management/place_order_form.html', context)


class ProductPurchaseRequestListView(IsStaffMixin, ListView):
    model = Order
    template_name = 'order_management/product_purchase_request_list.html'

    def get_queryset(self):
        return Order.objects.filter(status='product_purchase_request')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(ProductPurchaseRequestListView, self).get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context


@staff_member_required
def product_purchase_view(request, order_id):
    context = {}
    order = Order.objects.get(id=order_id)
    order.status = 'product_purchased'
    order.save()
    OrderProcessingDate.objects.create(order=order,
                                       status='product_purchased',
                                       )
    return HttpResponseRedirect(reverse('product-purchase-request-list'))


@staff_member_required
def purchase_cancel_view(request, order_id):
    context = {}
    order = Order.objects.get(id=order_id)
    context['order'] = order

    if request.POST:
        form = ProductPurchaseCancelFrom(request.POST)
        if form.is_valid():
            note = form.cleaned_data['note']

            OrderProcessingDate.objects.create(order=order,
                                               status='purchase_canceled',
                                               note=note)
            order.status = 'purchase_canceled'
            order.save()
            return HttpResponseRedirect(reverse('product-purchase-request-list'))

    else:
        form = ProductPurchaseCancelFrom()
        context['form'] = form
        return render(request, template_name='order_management/purchase_cancel_form.html',
                      context=context)


class PurchasedProductListView(IsStaffMixin, ListView):
    model = Order
    template_name = 'order_management/purchased_product_list.html'

    def get_queryset(self):
        return Order.objects.filter(status='product_purchased')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(PurchasedProductListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context


class PurchaseCanceledListView(IsStaffMixin, ListView):
    model = Order
    template_name = 'order_management/purchase_canceled_list.html'

    def get_queryset(self):
        return Order.objects.filter(status='purchase_canceled')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(PurchaseCanceledListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context


@staff_member_required
def purchased_product_send_to_shipping_view(request, order_id):
    context = {}
    order = Order.objects.get(id=order_id)
    order.status = 'product_in_shipping'
    order.save()
    OrderProcessingDate.objects.create(order=order,
                                       status='product_in_shipping',
                                       )
    return HttpResponseRedirect(reverse('purchased-product-list'))


class ProductInShippingListView(IsStaffMixin, ListView):
    model = Order
    template_name = 'order_management/product_in_shipping_list.html'

    def get_queryset(self):
        return Order.objects.filter(status='product_in_shipping')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(ProductInShippingListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context


@staff_member_required
def shipping_to_arrived_in_bangladesh_view(request, order_id):
    context = {}
    order = Order.objects.get(id=order_id)
    order.status = 'product_arrived_in_ezon_office'
    order.save()
    OrderProcessingDate.objects.create(order=order,
                                       status='product_arrived_in_ezon_office',
                                       )
    return HttpResponseRedirect(reverse('product-in-shipping-list'))


class ArrivedProductListView(IsStaffMixin, ListView):
    model = Order
    template_name = 'order_management/product_arrived_in_bangladesh_list.html'

    def get_queryset(self):
        return Order.objects.filter(status='product_in_shipping')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(ArrivedProductListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context

