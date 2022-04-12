from django.apps import AppConfig
import os


class ShopifyAppConfig(AppConfig):
    name = 'shopify_app'
    # Replace the API Key and Shared Secret with the one given for your
    # App by Shopify.
    #
    # To create an application, or find the API Key and Secret, visit:
    # - for private Apps:
    #     https://${YOUR_SHOP_NAME}.myshopify.com/admin/api
    # - for partner Apps:
    #     https://www.shopify.com/services/partners/api_clients
    #
    # You can ignore this file in git using the following command:
    #   git update-index --assume-unchanged shopify_settings.py
    # SHOPIFY_API_KEY = os.environ.get('SHOPIFY_API_KEY')
    # SHOPIFY_API_SECRET = os.environ.get('SHOPIFY_API_SECRET')

    # # API_VERSION specifies which api version that the app will communicate with
    # SHOPIFY_API_VERSION = os.environ.get('SHOPIFY_API_VERSION', 'unstable')



    # # See http://api.shopify.com/authentication.html for available scopes
    # # to determine the permisssions your app will need.
    # SHOPIFY_API_SCOPE = os.environ.get('SHOPIFY_API_SCOPE', 'read_products,read_orders').split(',')

    # print("SHOPIFY_API_SCOPE!!1")
    # print(SHOPIFY_API_SCOPE)`
    SHOPIFY_API_VERSION = 'unstable'
    SHOPIFY_API_KEY='2ca4708c0587a4e79c9ff3ecae247b71'
    SHOPIFY_API_SECRET='b485e0c72bfdb12408a909e58d20bf6e'
    # SHOPIFY_API_SCOPE=['read_products', 'read_orders','unauthenticated_read_product_listings','unauthenticated_read_collection_listings','unauthenticated_write_checkouts','unauthenticated_write_customers']
    SHOPIFY_API_SCOPE=['read_orders','read_products,write_products,unauthenticated_read_content,unauthenticated_read_customer_tags,unauthenticated_read_product_tags,unauthenticated_read_product_listings,unauthenticated_write_checkouts,unauthenticated_read_checkouts,unauthenticated_write_customers,unauthenticated_read_customers','read_products','write_products','unauthenticated_read_content','unauthenticated_read_customer_tags','unauthenticated_read_product_tags','unauthenticated_read_product_listings','unauthenticated_write_checkouts','unauthenticated_read_checkouts','unauthenticated_write_customers','unauthenticated_read_customers']




