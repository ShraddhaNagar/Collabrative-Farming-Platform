from django.contrib import admin
from .models import Customer
from .models import * 

admin.site.register(Address)
admin.site.register(Resource)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'unique_id',)  # Add 'unique_id' to the list display
