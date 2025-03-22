from django.contrib import admin
from django.urls import path, include

from fruitipediaApp.fruits.views import index, dashboard, create_fruit_view, create_category_view, fruit_details_view, \
    edit_fruit_view, delete_fruit_view

urlpatterns = [
    path('', index, name='index'),
    path('dashboard/', dashboard, name='dashboard'),
    path('create-fruit/', create_fruit_view, name='create_fruit'),
    path('<int:pk>/', include([
        path('fruit-detail/', fruit_details_view, name='fruit_detail'),
        path('edit-fruit/', edit_fruit_view , name='edit_fruit'),
        path('delete-fruit/', delete_fruit_view, name='delete_fruit'),
    ])),
    path('create-category/', create_category_view, name='create_category'),

]