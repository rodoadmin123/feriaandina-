from django.contrib import admin

from .models import ProductoModelo


@admin.register(ProductoModelo)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ["nombre", "artesano", "categoria", "precio", "stock"]
    list_filter = ["categoria"]
