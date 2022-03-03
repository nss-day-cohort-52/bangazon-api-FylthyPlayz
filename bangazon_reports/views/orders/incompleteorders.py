from django.shortcuts import render
from django.db import connection
from django.views import View

from bangazon_reports.views.helpers import dict_fetch_all

class IncompleteOrders(View):
    def get(self, request):
        with connection.cursor() as db_cursor:
            db_cursor.execute("""
                SELECT
                    o.id,
                    o.created_on,
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
                GROUP By created_on 
            """)

            dataset = dict_fetch_all(db_cursor)
        
        incomplete_orders = []

        for row in dataset:
            order = {
                'order_id': row['id'],
                'full_name': row['full_name'],
                'total': row['Total'],
                'created_on': row['created_on'],
                'completed_on': row['completed_on'],
            }

            if order['completed_on'] is None:
                incomplete_orders.append(order)

        template = 'list_with_incomplete_orders.html'

        context = {
            "incompleteorder_list": incomplete_orders
        }

        return render(request, template, context)