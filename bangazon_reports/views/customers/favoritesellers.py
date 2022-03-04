from django.shortcuts import render
from django.db import connection
from django.views import View

from bangazon_reports.views.helpers import dict_fetch_all

class FavoriteSellersList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            db_cursor.execute("""
                SELECT
                    u.id as user_id,
                    u.first_name || " " || u.last_name as full_name,
                    s.id as store_id,
                    s.name as store
                FROM
                    bangazon_api_store as s
                JOIN 
                    bangazon_api_favorite as f,
                    auth_user as u
                    ON s.id = f.store_id
                    AND f.customer_id = u.id
            """)

            dataset = dict_fetch_all(db_cursor)

            customers = []

            for row in dataset:
                store = {
                    "id": row["store_id"],
                    "name": row['store']
                }

                user_dict = next(
                    (
                        customer for customer in customers
                        if customer['user_id'] == row['user_id']
                    ),
                    None
                )
                
                if user_dict:
                    user_dict['stores'].append(store)
                else:
                    customers.append({
                        "user_id": row['user_id'],
                        "full_name": row['full_name'],
                        "stores": [store]
                    })
                print(customers)
        template = 'favorite_sellers.html'

        context = {
            "favorite_sellers": customers
        }

        return render(request, template, context)