from django.shortcuts import render
from django.db import connection
from django.views import View

from bangazon_reports.views.helpers import dict_fetch_all

class InexpensiveProductsList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            db_cursor.execute("""
                SELECT
                    p.name as product_name,
                    p.price as product_price,
                    p.description as product_description,
                    p.quantity,
                    p.location,
                    c.name as category
                FROM
                    bangazon_api_product as p
                JOIN
                    bangazon_api_category as c ON p.category_id = c.id
                WHERE p.price <= 1000
                ORDER By product_price
            """)

            dataset = dict_fetch_all(db_cursor)

            inexpensive_product_list = []

            for row in dataset:
                product = {
                    "name": row['product_name'],
                    "price": row['product_price'],
                    "description": row['product_description'],
                    "quantity": row['quantity'],
                    "location": row['location'],
                    "category": row['category']
                }

                inexpensive_product_list.append(product)

        template = 'product_list_inexpensive.html'

        context = {
            "inexpensive_product_list": inexpensive_product_list
        }

        return render(request, template, context)