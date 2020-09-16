from django.contrib import admin

from .models import *
# Register your models here.

class CtaegoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(AuctionListing)
admin.site.register(Category, CtaegoryAdmin)
admin.site.register(Watchlist)