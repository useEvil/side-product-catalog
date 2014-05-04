from django.contrib import admin

from sideproductcatalog.models import Product, Option, OptionValue, Category, SeasonCode, ColorCode

# Register your models here.


class OptionValueAdmin(admin.ModelAdmin):

    list_display = ['option', 'upc', 'label']
    ordering = ('option', 'value')


class OptionValueInline(admin.TabularInline):
    model = OptionValue
    extra = 10
    verbose_name_plural = 'optionvalues'


class OptionAdmin(admin.ModelAdmin):

    list_display = ['product', 'label']
    ordering = ('product', 'type')
    inlines = [OptionValueInline]


class OptionInline(admin.TabularInline):
    model = Option
    extra = 10
    verbose_name_plural = 'options'


class ProductAdmin(admin.ModelAdmin):

    list_display = ['category', 'name', 'sku', 'taxable', 'price', 'quantity', 'sale_price']
    list_editable = ['sku', 'taxable', 'quantity']
    ordering = ('category', 'name')
    inlines = [OptionInline]


class CategoryAdmin(admin.ModelAdmin):

    # create a payment link for the total amount
    def top_level(obj):
        try:
            parent = Category.objects.get(id=obj.parent)
            return parent.name
        except:
            return "Home"
    top_level.allow_tags = True
    top_level.short_description = "Parent"

    list_display = [top_level, 'name', 'level']
    ordering = ('level', 'name')
    verbose_name_plural = 'Categories'


admin.site.register(Product, ProductAdmin)
admin.site.register(Option, OptionAdmin)
admin.site.register(OptionValue, OptionValueAdmin)
admin.site.register(Category, CategoryAdmin)
# admin.site.register(SeasonCode, SeasonCodeAdmin)
# admin.site.register(ColorCode, ColorCodeAdmin)
