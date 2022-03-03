from django.urls import path 
from bangazon_reports.views.orders.completedorders import CompletedOrdersList
from bangazon_reports.views.orders.incompleteorders import IncompleteOrders


urlpatterns = [
    path('reports/completed_orders', CompletedOrdersList.as_view()),
    path('reports/incomplete_orders', IncompleteOrders.as_view())
]
