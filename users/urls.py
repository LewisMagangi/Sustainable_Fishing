from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Authentication URLs
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Profile URLs
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('profile/edit-class/', views.UserProfileUpdateView.as_view(), name='edit_profile_class'),
    path('profile/change-password/', views.change_password_view, name='change_password'),
    path('profile/delete/', views.delete_account_view, name='delete_account'),
    
    # User management URLs
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/<int:user_id>/', views.user_detail_view, name='user_detail'),
    
    # API URLs
    path('api/stats/', views.api_user_stats, name='api_user_stats'),
]