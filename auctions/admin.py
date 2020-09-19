from django.contrib import admin

from .models import *
# Register your models here.

class CtaegoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class WatchlistAdmin(admin.ModelAdmin):
    filter_horizontal = ('listing',)

admin.site.register(AuctionListing)
admin.site.register(Category, CtaegoryAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
admin.site.register(Bid)
admin.site.register(Comment)