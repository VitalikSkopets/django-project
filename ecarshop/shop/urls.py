from django.urls import path

from .views import *

app_name = 'shop'

urlpatterns = [
    path('', Index.as_view(), name="home"),
    path('gallery/', Gallery.as_view(), name="gallery"),
    path('search/', search, name="search"),
    path('weather/', weather, name="weather"),
    path('contact/', Contact.as_view(), name="contact"),
    path('feedback/', feedback, name="feedback"),
    path('register/', RegisterUser.as_view(), name="register"),
    path('login/', login_request, name="login"),
    path('logout/', logout_request, name="logout"),
    path('password_reset/', password_reset_request, name="password_reset"),
    path('vehicle_detail/<slug:vehicle_slug>/', VehicleDetail.as_view(), name="vehicle_detail"),
    path('type_detail/<slug:type_slug>/', TypeDetail.as_view(), name="type_detail"),
    path('<slug:slug>/', Manufacturers.as_view(), name="manufacturers"),

]
