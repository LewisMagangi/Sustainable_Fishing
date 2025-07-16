from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum, Avg, Count
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Catch


@admin.register(Catch)
class CatchAdmin(admin.ModelAdmin):
    # List display configuration
    list_display = (
        'fish_type', 'fisher_link', 'weight', 'location', 'catch_date', 
        'status', 'price', 'profit_indicator', 'created_at'
    )
    
    list_filter = (
        'status', 'fish_type', 'catch_date', 'created_at', 
        ('fisher', admin.RelatedOnlyFieldListFilter),
        'location'
    )
    
    search_fields = ('fish_type', 'fisher__username', 'fisher__full_name', 'location', 'notes')
    
    ordering = ('-catch_date', '-created_at')
    
    # Fieldsets for the form
    fieldsets = (
        ('Catch Information', {
            'fields': ('fisher', 'fish_type', 'weight', 'location', 'catch_date')
        }),
        ('Sales Information', {
            'fields': ('status', 'price', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    # Date hierarchy for easy navigation
    date_hierarchy = 'catch_date'
    
    # Custom methods for list display
    def fisher_link(self, obj):
        url = reverse('admin:users_user_change', args=[obj.fisher.id])
        return format_html('<a href="{}">{}</a>', url, obj.fisher.full_name or obj.fisher.username)
    fisher_link.short_description = 'Fisher'
    fisher_link.admin_order_field = 'fisher__full_name'
    
    def profit_indicator(self, obj):
        if obj.status == 'sold' and obj.price:
            if obj.price > 1000:  # Assuming good profit threshold
                return format_html('<span style="color: green;">💰 High</span>')
            elif obj.price > 500:
                return format_html('<span style="color: orange;">💵 Medium</span>')
            else:
                return format_html('<span style="color: red;">💸 Low</span>')
        elif obj.status == 'donated':
            return format_html('<span style="color: blue;">🎁 Donated</span>')
        else:
            return format_html('<span style="color: gray;">⏳ Pending</span>')
    profit_indicator.short_description = 'Profit'
    
    # Actions
    actions = ['mark_as_sold', 'mark_as_donated', 'mark_as_unsold', 'export_catches']
    
    def mark_as_sold(self, request, queryset):
        count = queryset.update(status='sold')
        self.message_user(request, f'{count} catches marked as sold.')
    mark_as_sold.short_description = 'Mark selected catches as sold'
    
    def mark_as_donated(self, request, queryset):
        count = queryset.update(status='donated')
        self.message_user(request, f'{count} catches marked as donated.')
    mark_as_donated.short_description = 'Mark selected catches as donated'
    
    def mark_as_unsold(self, request, queryset):
        count = queryset.update(status='unsold')
        self.message_user(request, f'{count} catches marked as unsold.')
    mark_as_unsold.short_description = 'Mark selected catches as unsold'
    
    def export_catches(self, request, queryset):
        # This would implement CSV export functionality
        count = queryset.count()
        self.message_user(request, f'Export functionality for {count} catches (implement CSV export).')
    export_catches.short_description = 'Export selected catches'
    
    # Customize the changelist view
    def changelist_view(self, request, extra_context=None):
        # Add statistics to the changelist view
        response = super().changelist_view(request, extra_context=extra_context)
        
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response
        
        # Calculate statistics
        metrics = {
            'total_catches': qs.count(),
            'total_weight': qs.aggregate(Sum('weight'))['weight__sum'] or 0,
            'avg_weight': qs.aggregate(Avg('weight'))['weight__avg'] or 0,
            'total_revenue': qs.filter(status='sold').aggregate(Sum('price'))['price__sum'] or 0,
            'sold_count': qs.filter(status='sold').count(),
            'donated_count': qs.filter(status='donated').count(),
            'unsold_count': qs.filter(status='unsold').count(),
        }
        
        # Add metrics to context
        response.context_data['summary'] = metrics
        
        return response
    
    # Optimize queries
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('fisher')
    
    # Add custom CSS and JS
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
        js = ('admin/js/custom_admin.js',)
