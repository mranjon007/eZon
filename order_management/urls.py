from django.urls import path
from .views import (
    homepage,
    AdminDashBoardView,
    PriceQueryListView,
    update_price_query,
    place_order_form_view,
    PlacedOrderListView,
)


urlpatterns = [
    path('', homepage, name='home'),
    path('admin_dashboard/', AdminDashBoardView.as_view(), name='admin-dashboard'),
    # future
    path('price_query_list/', PriceQueryListView.as_view(), name='price-query-list'),
    path('price_query_update/<pk>/', update_price_query, name='price-query-update'),
    path('place_order/', place_order_form_view, name='place-order-form'),
    path('placed_order_list/', PlacedOrderListView.as_view(), name='placed-order-list'),

    # path('price_query_result_submitted_list/', name='price query'),
    # path('product_purchase_order_list', name='product-purchase-order-list'),
    # path('product_purchased_complete_list', name='product-purchased-complete-list'),
    # path('order_in_shipping_list/', name='order-in-shipping-list'),
    # path('product_received_from_shipping_list/', name='order-received-from-shipping-list'),
    # path('product_sent_to_customer_list/', name='product-sent-to-customer-list'),
    # path('completed_order_list', name='completed-order-list'),
    # path('canceled_order_list', name='canceled-order-list'),
    # path('refunded_order_list', name='refunded-order-list'),
]
