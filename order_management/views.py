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

from .models import(
    Order,
    OrderProcessingDate,
    COMPANY_LISTING,
    COUNTRY_LIST,
    ORDER_STATUS,
)

from .forms import (
    PriceQueryForm,
    PriceQueryUpdateForm,
)

from .CustomMixin import (
    IsStaffMixin,
    LogoutIfNotStaffMixin,
)


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
                new_order = Order.objects.create(product_url=order.product_url, product_country=order.product_company, user=order.user)
                new_order_processing_dates = OrderProcessingDate.objects.create(order=new_order, status=new_order.status)
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
    """View function for renewing a specific BookInstance by librarian."""
    order = get_object_or_404(Order, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = PriceQueryUpdateForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            order.product_price = form.cleaned_data['product_price']
            order.product_tax = form.cleaned_data['product_tax']
            order.product_service_fee = form.cleaned_data['product_service_fee']
            if form.cleaned_data['admin_note']:
                order.admin_note = form.cleaned_data['admin_note']

            # check if the the element is a member of tuple
            order_status_element = 'query_result_submitted'
            if is_tuple_member(ORDER_STATUS, order_status_element):
                print('........... True')
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

