from django.contrib.auth import views as authViews
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.urls import static

from product import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/', authViews.LoginView.as_view(), name='login'),
    url(r'^accounts/logout/', authViews.LogoutView.as_view(), name='logout'),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^supplier-regular-page', views.SupplierRegularView.as_view(),
    	name='supplier-regular-page'),
    url(r'^supplier-comparative-page', views.SupplierComparativeView.as_view(),
    	name='supplier-comparative-page'),
    url(r'^customer-page', views.CustomerView.as_view(), name='customer-page'),
    url(r'^create_images_for_products/', views.create_images_for_products_view, name='create-images')
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)