from django.contrib import admin
from .models import Country, Vendor, Wine, VendorWine, Rater, WineRating


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code_iso2', 'code_iso3',)


admin.site.register(Country, CountryAdmin)


class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'is_active', 'is_test', 'plugin',
                    'max_pages', )


admin.site.register(Vendor, VendorAdmin)


class RaterAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'is_active', 'is_test', 'plugin', 'limit', )


admin.site.register(Rater, RaterAdmin)


class WineRatingInline(admin.TabularInline):
    model = WineRating
    extra = 0
    readonly_fields = ('rater', 'rating', 'num_ratings',)


class VendorWineInline(admin.TabularInline):
    model = VendorWine
    extra = 0
    readonly_fields = ('price_per_75cl', 'modified',)


class WineAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'winetype', 'country', 'region',
                    'winery', 'min_rating', 'min_price', 'modified',)

    list_filter = ['country', 'color', 'winetype', ]
    search_fields = ['name', 'winetype']
    readonly_fields = ('min_price', 'min_rating', 'modified',)
    inlines = [VendorWineInline, WineRatingInline]


admin.site.register(Wine, WineAdmin)
