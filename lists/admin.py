from django.contrib import admin
from lists.models import Item

# Register your models here.
#class ItemAdmin(admin.modelAdmin):
    #pass
admin.site.register(Item)
