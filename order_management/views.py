import datetime

from django.views.generic import TemplateView, ListView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.forms import ModelForm
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.admin.views.decorators import staff_member_required

from .models import (
    Order,
    OrderProcessingDate,
    DeliveryInfo,
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
    ProductPurchaseForm,
    ProductPurchaseCancelForm,
    ProductSendToDeliveryForm,
    ProductDeliveryCancelFrom,
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



######### User #########

@login_required
def user_dashboard(request, user_id):
    context = {}
    user = CustomUser.objects.get(id=user_id)
    if request.method == 'POST':
        form = PriceQueryForm(request.POST)
        if form.is_valid():
            product_url = form.cleaned_data['product_url']
            new_order = Order.objects.create(product_url=product_url,
                                             user=user)
            new_order_processing_dates = \
                OrderProcessingDate.objects.create(order=new_order,
                                                   status=new_order.status)
            order_list = Order.objects.filter(user=user).all()
            context['order_list'] = order_list
            return HttpResponseRedirect(reverse('user-dashboard', kwargs={'user_id':user_id}))  # user-dashboard e return korbe
    else:
        form = PriceQueryForm()
        context['form'] = form
        order_list = Order.objects.filter(user=user).all()
        context['order_list'] = order_list
        return render(request, template_name='order_management/user/user_dashboard.html', context=context)


def user_order_detail_view(request, primary_key):
    try:
        order = Order.objects.get(pk=primary_key)
    except Order.DoesNotExist:
        raise Http404('Order does not exist')
    return render(request, 'order_management/user/user_order_detail.html', context={'order': order })

########## END_USER ##########

def homepage(request):
    context = {}
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = PriceQueryForm(request.POST)
            if form.is_valid():
                order = Order()
                order.product_url = form.cleaned_data['product_url']
                # if form.cleaned_data['product_company']:
                #     order.product_company = form.cleaned_data['product_company']
                order.user = request.user
                new_order = Order.objects.create(product_url=order.product_url,
                                                 #product_country=order.product_company,
                                                 user=order.user)
                new_order_processing_dates = \
                    OrderProcessingDate.objects.create(order=new_order,
                                                       status=new_order.status)
                return HttpResponseRedirect(reverse('signup'))  # user-dashboard e return korbe
        else:
            context['message'] = 'Please Login/Register to place a product price Query'

    form = PriceQueryForm()
    # print(form)
    context['form'] = form
    return render(request, template_name='order_management/home.html', context=context)


class AdminDashBoardView(LoginRequiredMixin, IsStaffMixin, TemplateView):
    template_name = 'order_management/admin_dashboard.html'

    # def get_context_data(self, **kwargs):
    #     context = super(AdminDashBoardView).get_context_data(**kwargs)
    #     context['latest_articles'] = Article.objects.all()[:5]
    #     return context


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
            order.foreign_tax = form.cleaned_data['foreign_tax']
            order.foreign_shipping = form.cleaned_data['foreign_shipping']
            order.bd_shipping = form.cleaned_data['bd_shipping']
            order.bd_custom = form.cleaned_data['bd_custom']
            order.service_charge = form.cleaned_data['service_charge']
            order.mobile_or_bank_charge = form.cleaned_data['mobile_or_bank_charge']
            order.currency = form.cleaned_data['currency']
            order.exchange_rate = form.cleaned_data['exchange_rate']
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
        if form.is_valid():
            # get the cleaned order information
            product_url = form.cleaned_data['product_url']
            if is_tuple_member(COMPANY_LISTING, form.cleaned_data['product_company']):
                product_company = form.cleaned_data['product_company']
            if is_tuple_member(COUNTRY_LIST, form.cleaned_data['product_country']):
                product_country = form.cleaned_data['product_country']

            product_price = form.cleaned_data['product_price']
            foreign_tax = form.cleaned_data['foreign_tax']
            foreign_shipping = form.cleaned_data['foreign_shipping']
            bd_shipping = form.cleaned_data['bd_shipping']
            bd_custom = form.cleaned_data['bd_custom']
            service_charge = form.cleaned_data['service_charge']
            mobile_or_bank_charge = form.cleaned_data['mobile_or_bank_charge']
            currency = form.cleaned_data['currency']
            exchange_rate = form.cleaned_data['exchange_rate']
            if is_tuple_member(PAYMENT_STATUS, form.cleaned_data['payment_status']):
                payment_status = form.cleaned_data['payment_status']
            if form.cleaned_data['admin_note']:
                admin_note = form.cleaned_data['admin_note']
            if form.cleaned_data['customer_note']:
                customer_note = form.cleaned_data['customer_note']

            # get cleaned customer info
            name = form.cleaned_data['customer_name']
            phone_number = form.cleaned_data['customer_phone_number']
            email = form.cleaned_data['customer_email_address']
            address = form.cleaned_data['customer_address']

            generated_password = 'AB12CD'
            # check if the email or phone number already exist. later only phone check will work
            user, is_created = \
                CustomUser.objects.get_or_create(email=email,
                                                 )
            user.phone_number = phone_number
            user.address = address
            user.name = new_customer.name
            # set the user password and save
            user.set_password(generated_password)
            user.save()
            print(user.phone_number)
            order = Order.objects.create(product_url=product_url,
                                         product_country=product_country,
                                         product_company=product_company,
                                         product_price=product_price,
                                         foreign_tax=foreign_tax,
                                         foreign_shipping=foreign_shipping,
                                         bd_shipping=bd_shipping,
                                         bd_custom=bd_custom,
                                         service_charge=service_charge,
                                         mobile_or_bank_charge=mobile_or_bank_charge,
                                         currency=currency,
                                         exchange_rate=exchange_rate,
                                         payment_status=payment_status,
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
def product_purchase_form_view(request, order_id):
    context = {}
    order = Order.objects.get(id=order_id)
    context['order'] = order

    if request.POST:
        form = ProductPurchaseForm(request.POST)
        if form.is_valid():
            purchase_id = form.cleaned_data['purchase_id']

            OrderProcessingDate.objects.create(order=order,
                                               status='product_purchased',
                                               )
            order.status = 'product_purchased'
            order.purchase_id = purchase_id
            order.save()
            return HttpResponseRedirect(reverse('product-purchase-request-list'))

    else:
        form = ProductPurchaseForm()
        context['form'] = form
        return render(request, template_name='order_management/product_purchase_form.html',
                      context=context)


@staff_member_required
def purchase_cancel_view(request, order_id):
    context = {}
    order = Order.objects.get(id=order_id)
    context['order'] = order

    if request.POST:
        form = ProductPurchaseCancelForm(request.POST)
        if form.is_valid():
            note = form.cleaned_data['note']

            OrderProcessingDate.objects.create(order=order,
                                               status='purchase_canceled',
                                               note=note)
            order.status = 'purchase_canceled'
            order.save()
            return HttpResponseRedirect(reverse('product-purchase-request-list'))

    else:
        form = ProductPurchaseCancelForm()
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


@staff_member_required
def purchased_product_arrived_in_usa_office_view(request, order_id):
    context = {}
    order = Order.objects.get(id=order_id)
    order.status = 'product_arrived_in_usa_office'
    order.save()
    OrderProcessingDate.objects.create(order=order,
                                       status='product_arrived_in_usa_office',
                                       )
    return HttpResponseRedirect(reverse('purchased-product-list'))


class PurchasedProductArrivedInUsaOfficeListView(IsStaffMixin, ListView):
    model = Order
    template_name = 'order_management/product_arrived_in_usa_office_list.html'

    def get_queryset(self):
        return Order.objects.filter(status='product_arrived_in_usa_office')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(PurchasedProductArrivedInUsaOfficeListView, self).get_context_data(**kwargs)
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
    print('Send to shipping........')
    order.status = 'product_in_shipping'
    order.save()
    OrderProcessingDate.objects.create(order=order,
                                       status='product_in_shipping',
                                       )
    return HttpResponseRedirect(reverse('product-arrived-in-usa-office-list'))


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
        return Order.objects.filter(status='product_arrived_in_ezon_office')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(ArrivedProductListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context


##################
@staff_member_required
def product_send_to_delivery_person_form_view(request, order_id):
    context = {}
    order = Order.objects.get(id=order_id)
    context['order'] = order

    if request.POST:
        form = ProductSendToDeliveryForm(request.POST)
        if form.is_valid():
            delivery_person = form.cleaned_data['delivery_person']
            note = form.cleaned_data['note']

            OrderProcessingDate.objects.create(order=order,
                                               status='product_send_to_delivery_person',
                                               )

            order.status = 'product_send_to_delivery_person'
            order.save()

            # get the custom user instance of delivery person
            delivery_person_db_instance = CustomUser.objects.get(id=delivery_person)
            DeliveryInfo.objects.create(order=order, delivery_person=delivery_person_db_instance,
                                        note = note)
            return HttpResponseRedirect(reverse('arrived-product-list'))

    else:
        form = ProductSendToDeliveryForm()
        context['form'] = form
        return render(request, template_name='order_management/product_send_to_delivery_person_form.html',
                      context=context)


class ProductSendToDeliveryPersonList(IsStaffMixin, ListView):
    model = Order
    template_name = 'order_management/product_sent_to_delivery_person_list.html'

    def get_queryset(self):
        return Order.objects.filter(status='product_send_to_delivery_person')

    def get_context_data(self, **kwargs):
        context = super(ProductSendToDeliveryPersonList, self).get_context_data(**kwargs)
        #context['some_data'] = 'This is just some data'
        return context


@staff_member_required
def product_delivery_cancle_form_view(request, order_id):
    context = {}
    order = Order.objects.get(id=order_id)
    context['order'] = order

    if request.POST:
        form = ProductDeliveryCancelFrom(request.POST)
        if form.is_valid():
            note = form.cleaned_data['note']

            OrderProcessingDate.objects.create(order=order,
                                               status='product_delivery_canceled',
                                               )
            order.status = 'product_delivery_canceled'
            order.save()
            return HttpResponseRedirect(reverse('product-send-to-delivery-person-list'))

    else:
        form = ProductDeliveryCancelFrom()
        context['form'] = form
        return render(request, template_name='order_management/product_send_to_delivery_person_form.html',
                      context=context)


class ProductDeliveryCanceledList(IsStaffMixin, ListView):
    model = Order
    template_name = 'order_management/product_delivery_canceled_list.html'

    def get_queryset(self):
        return Order.objects.filter(status='product_delivery_canceled')

    def get_context_data(self, **kwargs):
        context = super(ProductDeliveryCanceledList, self).get_context_data(**kwargs)
        return context


@staff_member_required
def product_delivered_to_customer_view(request, order_id):
    context = {}
    order = Order.objects.get(id=order_id)
    order.status = 'product_delivered_to_the_customer'
    order.save()
    OrderProcessingDate.objects.create(order=order,
                                       status='product_delivered_to_the_customer',
                                       )
    return HttpResponseRedirect(reverse('product-send-to-delivery-person-list'))


class ProductDeliveredToCustomerList(IsStaffMixin, ListView):
    model = Order
    template_name = 'order_management/product_delivered_to_customer_list.html'

    def get_queryset(self):
        return Order.objects.filter(status='product_delivered_to_the_customer')

    def get_context_data(self, **kwargs):
        context = super(ProductDeliveredToCustomerList, self).get_context_data(**kwargs)
        return context