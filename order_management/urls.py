from django.urls import path
from .views import (
    homepage,
    price_query_login_form_view,
    price_query_signup_form_view,
    AdminDashBoardView,

    user_dashboard,
    user_order_detail_view,
    price_query_for_loggedIn_user_form_view,

    PriceQueryListView,
    update_price_query,
    PriceQuerySubmittedList,
    place_order_form_view,
    PlacedOrderListView,
    ProductPurchaseRequestListView,
    product_purchase_form_view,
    purchase_cancel_view,
    PurchasedProductListView,
    PurchaseCanceledListView,
    purchased_product_arrived_in_usa_office_view,
    PurchasedProductArrivedInUsaOfficeListView,
    purchased_product_send_to_shipping_view,
    ProductInShippingListView,
    shipping_to_arrived_in_bangladesh_view,
    ArrivedProductListView,
    product_send_to_delivery_person_form_view,
    ProductSendToDeliveryPersonList,
    product_delivery_cancle_form_view,
    ProductDeliveryCanceledList,
    product_delivered_to_customer_view,
    ProductDeliveredToCustomerList,
)


urlpatterns = [
    path('', homepage, name='home'),
    path('price_query_and_login', price_query_login_form_view, name='price-query-and-login'),
    path('price_query_and_signup', price_query_signup_form_view, name='price-query-and-signup'),
    path('user_dashboard/', user_dashboard, name='user-dashboard'),
    path('price_query_for_loggedin_user/', price_query_for_loggedIn_user_form_view, name='price-query-for-loggedin-user'),
    path('user_dashboard/order/<int:primary_key>', user_order_detail_view, name='user-order-detail'),


    path('admin_dashboard/', AdminDashBoardView.as_view(), name='admin-dashboard'),
    path('price_query_list/', PriceQueryListView.as_view(), name='price-query-list'),
    path('price_query_update/<pk>/', update_price_query, name='price-query-update'),
    path('price_query_submitted_list/', PriceQuerySubmittedList.as_view(), name='price-query-submitted-list'),
    path('place_order/', place_order_form_view, name='place-order-form'),
    path('placed_order_list/', PlacedOrderListView.as_view(), name='placed-order-list'),
    path('product_purchase_request_list/', ProductPurchaseRequestListView.as_view(), name='product-purchase-request-list'),
    path('product_purchase_form/<int:order_id>/', product_purchase_form_view, name='product-purchase'),
    path('purchase_cancel/<int:order_id>/', purchase_cancel_view, name='purchase-cancel'),
    path('purchased_product_list/', PurchasedProductListView.as_view(), name='purchased-product-list'),
    path('purchase_canceled_list/', PurchaseCanceledListView.as_view(), name='purchase-canceled-list'),
    path('product_arrived_in_usa_office/<int:order_id>/', purchased_product_arrived_in_usa_office_view, name='product-arrived-in-usa-office-view'),
    path('product_arrived_in_usa_office_list/', PurchasedProductArrivedInUsaOfficeListView.as_view(), name='product-arrived-in-usa-office-list'),
    path('purchased_product_send_to_shipping/<int:order_id>/', purchased_product_send_to_shipping_view, name='purchased-product-send-to-shipping'),
    path('product_in_shipping_list/', ProductInShippingListView.as_view(), name='product-in-shipping-list'),
    path('shipping_to_arrived_in_bangladesh/<int:order_id>/', shipping_to_arrived_in_bangladesh_view, name='shipping-to-arrived-in-bangladesh'),
    path('arrived_product_list/', ArrivedProductListView.as_view(), name='arrived-product-list'),
    path('arrived_product_send_to_delivery/<int:order_id>/', product_send_to_delivery_person_form_view, name='arrived-product-send-to-delivery-person'),
    path('product_send_to_delivery_person_list/', ProductSendToDeliveryPersonList.as_view(), name='product-send-to-delivery-person-list'),
    path('product_delivery_cancel_form/<int:order_id>', product_delivery_cancle_form_view, name='product-delivery-cancel-form'),
    path('product_delivery_canceled_list/', ProductDeliveryCanceledList.as_view(), name='product-delivery-canceled-list'),
    path('product_delivered_to_customer/<int:order_id>', product_delivered_to_customer_view, name='product-delivered-to-customer'),
    path('product_delivered_to_customer_list/', ProductDeliveredToCustomerList.as_view(), name='product-delivered-to-customer-list')

    #path('arrived_product_cancel_delivery/<int:order_id>/'),
    #path('canceled_after_arrive_list/')
]
