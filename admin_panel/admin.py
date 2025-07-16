from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe

# Import models from all apps that need admin interface
from catches.models import Catch
from educational_content.models import EducationalContent


@admin.register(Catch)
class CatchAdmin(admin.ModelAdmin):
    """Centralized admin for Catch model"""
    list_display = ['fish_type', 'weight', 'fisher_link', 'catch_date', 'status_badge', 'price_display', 'location', 'created_at']
    list_filter = ['status', 'fish_type', 'catch_date', 'location', 'created_at']
    search_fields = ['fish_type', 'fisher__username', 'fisher__first_name', 'fisher__last_name', 'location', 'notes']
    date_hierarchy = 'catch_date'
    ordering = ['-catch_date', '-created_at']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 25
    
    fieldsets = (
        ('Catch Information', {
            'fields': ('fisher', 'fish_type', 'weight', 'catch_date', 'location'),
            'description': 'Basic information about the catch'
        }),
        ('Sales Information', {
            'fields': ('status', 'price'),
            'description': 'Sales status and pricing information'
        }),
        ('Additional Details', {
            'fields': ('notes',),
            'classes': ('collapse',),
            'description': 'Optional additional notes about the catch'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
            'description': 'System timestamps'
        }),
    )
    
    def fisher_link(self, obj):
        """Display fisher name as a link to their user admin page"""
        url = reverse('admin:auth_user_change', args=[obj.fisher.pk])
        return format_html('<a href="{}">{}</a>', url, obj.fisher.username)
    fisher_link.short_description = 'Fisher'
    fisher_link.admin_order_field = 'fisher__username'
    
    def status_badge(self, obj):
        """Display status with colored badge"""
        colors = {
            'sold': '#28a745',      # green
            'unsold': '#ffc107',    # yellow
            'donated': '#17a2b8'    # blue
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 12px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    status_badge.admin_order_field = 'status'
    
    def price_display(self, obj):
        """Display price with currency formatting"""
        if obj.price:
            return format_html('<span style="color: #28a745; font-weight: bold;">${}</span>', obj.price)
        return mark_safe('<span style="color: #6c757d;">-</span>')
    price_display.short_description = 'Price'
    price_display.admin_order_field = 'price'
    

@admin.register(EducationalContent)
class EducationalContentAdmin(admin.ModelAdmin):
    """Centralized admin for Educational Content model"""
    list_display = ['title', 'author_link', 'category_badge', 'difficulty_badge', 'published_status', 'featured_status', 'read_count', 'created_at']
    list_filter = ['category', 'difficulty_level', 'is_published', 'featured', 'created_at', 'author']
    search_fields = ['title', 'content', 'author__username', 'author__first_name', 'author__last_name']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    readonly_fields = ['read_count', 'created_at', 'updated_at']
    list_per_page = 25
    
    fieldsets = (
        ('Content Information', {
            'fields': ('author', 'title', 'content', 'category', 'difficulty_level'),
            'description': 'Basic educational content information'
        }),
        ('Publication Settings', {
            'fields': ('is_published', 'featured'),
            'description': 'Control content visibility and prominence'
        }),
        ('Statistics', {
            'fields': ('read_count',),
            'classes': ('collapse',),
            'description': 'Content engagement statistics'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
            'description': 'System timestamps'
        }),
    )
    
    def author_link(self, obj):
        url = reverse('admin:auth_user_change', args=[obj.author.pk])
        return format_html('<a href="{}">{}</a>', url, obj.author.username)
    author_link.short_description = 'Author'
    
    def category_badge(self, obj):
        colors = {
            'sustainability': '#28a745',
            'techniques': '#007bff', 
            'regulations': '#ffc107',
            'conservation': '#17a2b8'
        }
        color = colors.get(obj.category, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            color, obj.get_category_display()
        )
    category_badge.short_description = 'Category'
    
    def difficulty_badge(self, obj):
        colors = {'beginner': '#28a745', 'intermediate': '#ffc107', 'advanced': '#dc3545'}
        color = colors.get(obj.difficulty_level, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            color, obj.get_difficulty_level_display()
        )
    difficulty_badge.short_description = 'Difficulty'
    
    def published_status(self, obj):
        if obj.is_published:
            return format_html('<span style="color: #28a745; font-weight: bold;">✓ Published</span>')
        return format_html('<span style="color: #dc3545; font-weight: bold;">✗ Draft</span>')
    published_status.short_description = 'Status'
    
    def featured_status(self, obj):
        if obj.featured:
            return format_html('<span style="color: #ffc107;">⭐ Featured</span>')
        return format_html('<span style="color: #6c757d;">-</span>')
    featured_status.short_description = 'Featured'


# Future admin classes will go here:
# @admin.register(TimelinePost)
# class TimelinePostAdmin(admin.ModelAdmin):
#     """Centralized admin for Timeline Posts model"""
#     pass
