from django.urls import path
from . import views

app_name = 'content'

urlpatterns = [
    path('', views.content_list, name='content_list'),
    path('<int:content_id>/', views.content_detail, name='detail'),
    path('create/', views.content_create, name='create'),
    path('<int:content_id>/update/', views.content_update, name='update'),
    path('<int:content_id>/delete/', views.content_delete, name='delete'),
    path('my-content/', views.my_content, name='my_content'),
    path('featured/', views.featured_content, name='featured'),
]
