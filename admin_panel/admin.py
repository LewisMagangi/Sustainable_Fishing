from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe

# Import models from all apps that need admin interface
from catches.models import Catch


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
    
    def get_queryset(self, request):
        """Optimize queryset with select_related for better performance"""
        queryset = super().get_queryset(request)
        return queryset.select_related('fisher')
    
    def save_model(self, request, obj, form, change):
        """Custom save logic - could add logging or notifications here"""
        if not change:  # Creating new catch
            # Log who created the catch (if needed)
            pass
        super().save_model(request, obj, form, change)
    
    actions = ['mark_as_sold', 'mark_as_unsold', 'mark_as_donated']
    
    def mark_as_sold(self, request, queryset):
        """Bulk action to mark catches as sold"""
        updated = queryset.update(status='sold')
        self.message_user(request, f'{updated} catches were successfully marked as sold.')
    mark_as_sold.short_description = "Mark selected catches as sold"
    
    def mark_as_unsold(self, request, queryset):
        """Bulk action to mark catches as unsold"""
        updated = queryset.update(status='unsold')
        self.message_user(request, f'{updated} catches were successfully marked as unsold.')
    mark_as_unsold.short_description = "Mark selected catches as unsold"
    
    def mark_as_donated(self, request, queryset):
        """Bulk action to mark catches as donated"""
        updated = queryset.update(status='donated')
        self.message_user(request, f'{updated} catches were successfully marked as donated.')
    mark_as_donated.short_description = "Mark selected catches as donated"


# Future admin classes for other apps will go here:
# 
# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     """Centralized admin for User model"""
#     pass
# 
# @admin.register(EducationalContent)
# class EducationalContentAdmin(admin.ModelAdmin):
#     """Centralized admin for Educational Content model"""
#     pass
# 
# @admin.register(TimelinePost)
# class TimelinePostAdmin(admin.ModelAdmin):
#     """Centralized admin for Timeline Posts model"""
#     pass
