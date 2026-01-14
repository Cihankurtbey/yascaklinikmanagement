from django.contrib import admin
from .models import Payment, PriceList


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'amount', 'payment_date', 'created_by', 'created_at')
    list_filter = ('payment_date', 'created_at')
    search_fields = ('patient__first_name', 'patient__last_name', 'description')
    date_hierarchy = 'payment_date'
    readonly_fields = ('created_at',)


@admin.register(PriceList)
class PriceListAdmin(admin.ModelAdmin):
    list_display = ('treatment_type', 'price', 'updated_at')
    search_fields = ('treatment_type__name',)
    readonly_fields = ('updated_at',)
