from django.contrib import admin

from .models import Supplier, Customer, Articul, Product, ProductImage

admin.site.register(Supplier)
admin.site.register(Customer)
admin.site.register(Articul)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'articul', 'price', 'is_available')

admin.site.register(Product, ProductAdmin)

admin.site.register(ProductImage)