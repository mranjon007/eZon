from django.urls import path
from .views import (
    homepage,
    AdminDashBoardView,
    PriceQueryListView,
    update_price_query,
    PriceQuerySubmittedList,
    place_order_form_view,
    PlacedOrderListView,
    ProductPurchaseRequestListView,
    product_purchase_view,
    purchase_cancel_view,
    PurchasedProductListView,
    PurchaseCanceledListView,
    purchased_product_send_to_shipping_view,
    ProductInShippingListView,
    shipping_to_arrived_in_bangladesh_view,
    ArrivedProductListView,
)


urlpatterns = [
    path('', homepage, name='home'),
    path('admin_dashboard/', AdminDashBoardView.as_view(), name='admin-dashboard'),
    # future
    path('price_query_list/', PriceQueryListView.as_view(), name='price-query-list'),
    path('price_query_update/<pk>/', update_price_query, name='price-query-update'),
    path('price_query_submitted_list/', PriceQuerySubmittedList.as_view(), name='price-query-submitted-list'),
    path('place_order/', place_order_form_view, name='place-order-form'),
    path('placed_order_list/', PlacedOrderListView.as_view(), name='placed-order-list'),
    path('product_purchase_request_list/', ProductPurchaseRequestListView.as_view(), name='product-purchase-request-list'),
    path('product_purchase/<int:order_id>/', product_purchase_view, name='product-purchase'),
    path('purchase_cancel/<int:order_id>/', purchase_cancel_view, name='purchase-cancel'),
    path('purchased_product_list/', PurchasedProductListView.as_view(), name='purchased-product-list'),
    path('purchase_canceled_list/', PurchaseCanceledListView.as_view(), name='purchase-canceled-list'),
    path('purchased_product_send_to_shipping/<int:order_id>/', purchased_product_send_to_shipping_view, name='purchased-product-send-to-shipping'),
    path('product_in_shipping_list/', ProductInShippingListView.as_view(), name='product-in-shipping-list'),
    path('shipping_to_arrived_in_bangladesh/<int:order_id>/', shipping_to_arrived_in_bangladesh_view, name='shipping-to-arrived-in-bangladesh'),
    path('arrived_product_list/', ArrivedProductListView.as_view(), name='arrived-product-list'),
]
