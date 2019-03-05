from django.contrib.auth import views as authViews
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings

from product import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/', authViews.LoginView.as_view(), name='login'),
    url(r'^accounts/logout/', authViews.LogoutView.as_view(), name='logout'),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^supplier-regular-page', views.SupplierRegularView.as_view(),
    	name='supplier-regular-page'),
    url(r'^supplier-comparative-page', views.SupplierRegularView.as_view(),
    	name='supplier-comparative-page'),
    url(r'^test_data/', views.test_data_view)
] 
