from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.db.models import Count
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # List display configuration
    list_display = (
        'username', 'full_name', 'email', 'role', 'location', 
        'profile_picture_preview', 'catches_count', 'posts_count', 
        'is_active', 'created_at'
    )
    
    list_filter = (
        'role', 'is_active', 'is_staff', 'is_superuser', 
        'created_at', 'updated_at'
    )
    
    search_fields = ('username', 'full_name', 'email', 'location')
    
    ordering = ('-created_at',)
    
    # Fieldsets for the edit form
    fieldsets = (
        ('Basic Information', {
            'fields': ('username', 'password')
        }),
        ('Personal Information', {
            'fields': ('full_name', 'email', 'role', 'location', 'bio', 'profile_picture')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Important dates', {
            'fields': ('last_login', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Fieldsets for the add form
    add_fieldsets = (
        ('Basic Information', {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
        ('Personal Information', {
            'fields': ('full_name', 'role', 'location', 'bio', 'profile_picture')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'last_login')
    
    # Custom methods for list display
    def profile_picture_preview(self, obj):
        if obj.profile_picture:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 50%; object-fit: cover;" />',
                obj.profile_picture
            )
        return format_html(
            '<div style="width: 50px; height: 50px; border-radius: 50%; background-color: #f8f9fa; '
            'display: flex; align-items: center; justify-content: center; border: 2px solid #dee2e6;">'
            '<i class="fas fa-user" style="color: #6c757d;"></i></div>'
        )
    profile_picture_preview.short_description = 'Profile Picture'
    
    def catches_count(self, obj):
        count = obj.catches.count()
        if count > 0:
            url = reverse('admin:fishing_catch_changelist') + f'?fisher__id__exact={obj.id}'
            return format_html('<a href="{}">{} catches</a>', url, count)
        return '0 catches'
    catches_count.short_description = 'Catches'
    
    def posts_count(self, obj):
        count = obj.timeline_posts.count()
        if count > 0:
            url = reverse('admin:content_timelinepost_changelist') + f'?author__id__exact={obj.id}'
            return format_html('<a href="{}">{} posts</a>', url, count)
        return '0 posts'
    posts_count.short_description = 'Posts'
    
    # Actions
    actions = ['activate_users', 'deactivate_users', 'make_educators', 'make_fishermen']
    
    def activate_users(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f'{count} users have been activated.')
    activate_users.short_description = 'Activate selected users'
    
    def deactivate_users(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count} users have been deactivated.')
    deactivate_users.short_description = 'Deactivate selected users'
    
    def make_educators(self, request, queryset):
        count = queryset.update(role='educator')
        self.message_user(request, f'{count} users have been made educators.')
    make_educators.short_description = 'Make selected users educators'
    
    def make_fishermen(self, request, queryset):
        count = queryset.update(role='fisherman')
        self.message_user(request, f'{count} users have been made fishermen.')
    make_fishermen.short_description = 'Make selected users fishermen'
    
    # Customize the changelist view
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('catches', 'timeline_posts')
    
    # Add custom CSS and JS
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
        js = ('admin/js/custom_admin.js',)
