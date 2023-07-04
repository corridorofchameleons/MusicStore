from django import forms
from django_filters import OrderingFilter, FilterSet, RangeFilter, MultipleChoiceFilter
from .models import Product, Brand


def get_choices():
    return [(bnd.pk, bnd.brand) for bnd in Brand.objects.all()]


class ProductFilter(FilterSet):
    price = RangeFilter()
    brand = MultipleChoiceFilter(
        label='Manufacturer',
        choices=get_choices(),
        widget=forms.CheckboxSelectMultiple()
    )

    o = OrderingFilter(choices=(('title', 'title'), ('price', 'price'), ('-price', '-price')))

    class Meta:
        model = Product
        fields = ['brand', 'price']
