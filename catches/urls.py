from django.urls import path
from . import views

app_name = 'catches'

urlpatterns = [
    path('', views.catch_list, name='catch_list'),
    path('<int:catch_id>/', views.catch_detail, name='catch_detail'),
    path('create/', views.catch_create, name='catch_create'),
    path('<int:catch_id>/update/', views.catch_update, name='catch_update'),
    path('<int:catch_id>/delete/', views.catch_delete, name='catch_delete'),
    path('my-catches/', views.my_catches, name='my_catches'),
]
