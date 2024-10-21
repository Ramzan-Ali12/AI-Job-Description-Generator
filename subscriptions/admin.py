from django.contrib import admin
from subscriptions.models import Product, Price,Subscription

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'uuid', 's_id')  # Display these fields in the admin list view
    search_fields = ('name', 's_id')  # Add a search box to search products by name or s_id
    readonly_fields = ('uuid', 's_id')  # Make uuid and s_id read-only in the admin form

@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ("uuid", "s_id",'product', 'price',)
    search_fields = ('product__name', 's_id')  # Allow searching by related product name or price s_id
    list_filter = ('currency', 'recurring_interval')  # Add filters for currency and recurring interval
    readonly_fields = ('uuid', 's_id')  # Make uuid and s_id read-only

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("uuid",'user', 's_id', 'status')
    search_fields = ('user__username', 's_id')
    list_filter = ('status',)
    readonly_fields = ('uuid', 's_id')