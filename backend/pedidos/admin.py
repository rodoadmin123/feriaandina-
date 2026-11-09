from django.contrib import admin

from .models import LineaPedidoModelo, PedidoModelo


class LineaEnLinea(admin.TabularInline):
    model = LineaPedidoModelo
    extra = 0


@admin.register(PedidoModelo)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ["id", "comprador", "metodo_pago", "estado", "total"]
    inlines = [LineaEnLinea]
