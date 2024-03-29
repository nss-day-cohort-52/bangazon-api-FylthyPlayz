"""Module for generating games by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from bangazon_reports.views.helpers import dict_fetch_all

class CompletedOrdersList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            db_cursor.execute("""
                SELECT
                    o.id,
                    pt.merchant_name,
                    o.completed_on,
                    u.first_name || ' ' || u.last_name AS full_name,
                    SUM(p.price) AS Total
                FROM bangazon_api_order o
                Join bangazon_api_orderproduct op
                    ON op.order_id = o.id
                Join bangazon_api_product p
                    ON op.product_id = p.id
                Join auth_user u
                    ON o.user_id = u.id
                Join bangazon_api_paymenttype pt
                    ON o.payment_type_id = pt.id
                GROUP By order_id
            """)

            dataset = dict_fetch_all(db_cursor)

        completed_orders = []

        for row in dataset:
            order = {
                'order_id': row['id'],
                'full_name': row['full_name'],
                'total': row['Total'],
                'merchant': row['merchant_name'],
                'completed_on': row['completed_on'],
            }

            if order['completed_on'] is not None:
                completed_orders.append(order)
            
        template = 'list_with_completed_orders.html'

        context = {
            "completedorder_list": completed_orders
        }

        return render(request, template, context)