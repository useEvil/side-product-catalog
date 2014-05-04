from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sideproductcatalog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'sideproductcatalog.views.index', name='index'),
    url(r'^product/(?P<product_id>[\d]+)$', 'sideproductcatalog.views.product', name='product'),
)
