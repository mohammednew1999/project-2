from django.urls import path
from .views import *



urlpatterns = [
    path('login/',login_user,name='login_user'),
    path('logout/',logout_user,name='logout_user'),
    path('sign_up/',sign_up_user,name='sign_up_user'),
    path('change_password/',change_password,name='change_password'),
    path('edit_information/',edit_account_information,name='edit_account_information'),


]

