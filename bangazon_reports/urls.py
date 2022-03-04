from django.urls import path
from bangazon_reports.views.customers.favoritesellers import FavoriteSellersList 
from bangazon_reports.views.orders.completedorders import CompletedOrdersList
from bangazon_reports.views.orders.incompleteorders import IncompleteOrders
from bangazon_reports.views.products.expensiveproducts import ExpensiveProductsList
from bangazon_reports.views.products.inexpensiveproducts import InexpensiveProductsList


urlpatterns = [
    path('reports/completed_orders', CompletedOrdersList.as_view()),
    path('reports/incomplete_orders', IncompleteOrders.as_view()),
    path('reports/expensive_product_list', ExpensiveProductsList.as_view()),
    path('reports/inexpensive_product_list', InexpensiveProductsList.as_view()),
    path('reports/favorite_sellers', FavoriteSellersList.as_view())
]
