from django.shortcuts import render
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect

from sideproductcatalog.models import Product, Option, OptionValue, Category, SeasonCode, ColorCode

def index(request):
    c = Context(
            dict(
                page_title='Products',
                categories=Category.objects.filter(parent=None).all()
            )
        )
    return render_to_response('index.html', c, context_instance=RequestContext(request))

def product(request, product_id=None):
    try:
        product=Product.objects.get(id=product_id)
    except:
        return HttpResponseRedirect('/')
    c = Context(
            dict(
                page_title=product.name,
                product=product,
            )
        )
    return render_to_response('product.html', c, context_instance=RequestContext(request))
