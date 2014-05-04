from django.db import models

from decimal import Decimal


class CurrencyField(models.DecimalField):

    def __init__(self, *args, **kwargs):
        kwargs['max_digits'] =  10
        kwargs['decimal_places'] = 2
        super(CurrencyField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        try:
            return super(CurrencyField, self).to_python(value).quantize(Decimal('0.01'))
        except AttributeError:
            return None


class SeasonCode(models.Model):

    value = models.CharField(max_length=15, blank=True, null=True)
    label = models.CharField(max_length=50, blank=True, null=True)

    def __unicode__(self):
        return '{0}'.format(self.label)

class ColorCode(models.Model):

    value = models.CharField(max_length=15, blank=True, null=True)
    label = models.CharField(max_length=50, blank=True, null=True)

    def __unicode__(self):
        return '{0}'.format(self.label)

class Category(models.Model):

    name = models.CharField(max_length=100, blank=False, null=False)
    level = models.PositiveIntegerField(blank=False, null=False)
#     parent = models.ForeignKey(Category, related_name='parent', blank=True, null=True)
    parent = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return '{0} - {1}'.format(self.level, self.name)

    @property
    def children(self):
        return Category.objects.filter(parent=self.id)

    @property
    def get_parent(self):
        try:
            return Category.objects.get(id=self.parent)
        except:
            return

class Product(models.Model):

    name = models.CharField(max_length=100, blank=False, null=False)
    sku = models.CharField(max_length=100, blank=False, null=False)
    taxable = models.BooleanField(blank=True, default=False)
    price = CurrencyField(blank=False, null=False, default=0.00)
    quantity = models.PositiveIntegerField(max_length=15, blank=False, null=False, default=0)
    description = models.CharField(max_length=1000, blank=True, null=True)
    sale_price = CurrencyField(blank=False, null=False, default=0.00)
    on_sale = models.BooleanField(blank=True, default=False)
    category = models.ForeignKey(Category, blank=True, null=True, related_name="products")
    season = models.CharField(max_length=25, blank=True, null=True)
    season_code = models.ForeignKey(SeasonCode, blank=True, null=True)

    def __unicode__(self):
        return '{0} - ${1}'.format(self.name, self.price)

    @property
    def category_breadcrumb(self):
        categories = list()
        parent = self.category.get_parent
        categories.append(self.category.name)
        while parent:
            categories.append(parent.name)
            parent = parent.get_parent
        categories.reverse()
        return " &gt; ".join(categories)


class Option(models.Model):

    product = models.ForeignKey(Product, related_name='options')
    type = models.CharField(max_length=15, blank=True, null=True)
    label = models.CharField(max_length=50, blank=True, null=True)

    def __unicode__(self):
        return '{0} - {1}'.format(self.product, self.label)

    def option_value_list(self):
        option_value_list = self.option_value.values('upc').distinct()
        options = list()
        for option_value in option_value_list:
            option_values = self.option_value.filter(upc=option_value['upc']).all()
            values = [ ov.label for ov in option_values ]
            values.append(option_value['upc'])
            options.append(values)
        return options


class OptionValue(models.Model):

    option = models.ForeignKey(Option, related_name='option_value')
    upc = models.PositiveIntegerField(blank=False, null=False)
    color_code = models.ForeignKey(ColorCode, blank=True, null=True)
    value = models.CharField(max_length=15, blank=True, null=True)
    label = models.CharField(max_length=50, blank=True, null=True)

    def __unicode__(self):
        return '{0} - {1}'.format(self.upc, self.label)
