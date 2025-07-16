from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Sum
from django.urls import reverse
from django.utils import timezone
from .models import TimelinePost, EducationalContent, PostLike


class PostLikeInline(admin.TabularInline):
    model = PostLike
    extra = 0
    readonly_fields = ('user', 'created_at')
    can_delete = False


@admin.register(TimelinePost)
class TimelinePostAdmin(admin.ModelAdmin):
    # List display configuration
    list_display = (
        'title', 'author_link', 'post_type', 'likes_count', 
        'engagement_indicator', 'created_at'
    )
    
    list_filter = (
        'post_type', 'created_at', 'updated_at',
        ('author', admin.RelatedOnlyFieldListFilter),
    )
    
    search_fields = ('title', 'content', 'author__username', 'author__full_name')
    
    ordering = ('-created_at',)
    
    # Fieldsets for the form
    fieldsets = (
        ('Post Information', {
            'fields': ('author', 'title', 'content', 'post_type')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Engagement', {
            'fields': ('likes_count',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('likes_count', 'created_at', 'updated_at')
    
    # Date hierarchy for easy navigation
    date_hierarchy = 'created_at'
    
    # Inlines
    inlines = [PostLikeInline]
    
    # Custom methods for list display
    def author_link(self, obj):
        url = reverse('admin:users_user_change', args=[obj.author.id])
        return format_html('<a href="{}">{}</a>', url, obj.author.full_name or obj.author.username)
    author_link.short_description = 'Author'
    author_link.admin_order_field = 'author__full_name'
    
    def engagement_indicator(self, obj):
        if obj.likes_count > 50:
            return format_html('<span style="color: green;">🔥 High</span>')
        elif obj.likes_count > 20:
            return format_html('<span style="color: orange;">👍 Medium</span>')
        elif obj.likes_count > 0:
            return format_html('<span style="color: blue;">💙 Low</span>')
        else:
            return format_html('<span style="color: gray;">😐 None</span>')
    engagement_indicator.short_description = 'Engagement'
    
    # Actions
    actions = ['feature_posts', 'unfeature_posts', 'reset_likes']
    
    def feature_posts(self, request, queryset):
        # This would add a featured field to the model
        count = queryset.count()
        self.message_user(request, f'{count} posts marked as featured (implement featured field).')
    feature_posts.short_description = 'Feature selected posts'
    
    def unfeature_posts(self, request, queryset):
        count = queryset.count()
        self.message_user(request, f'{count} posts unfeatured (implement featured field).')
    unfeature_posts.short_description = 'Unfeature selected posts'
    
    def reset_likes(self, request, queryset):
        count = queryset.update(likes_count=0)
        self.message_user(request, f'Likes reset for {count} posts.')
    reset_likes.short_description = 'Reset likes for selected posts'
    
    # Optimize queries
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('author')


@admin.register(EducationalContent)
class EducationalContentAdmin(admin.ModelAdmin):
    # List display configuration
    list_display = (
        'title', 'author_link', 'category', 'difficulty_level', 
        'is_published', 'featured', 'read_count', 'popularity_indicator', 'created_at'
    )
    
    list_filter = (
        'category', 'difficulty_level', 'is_published', 'featured', 
        'created_at', 'updated_at',
        ('author', admin.RelatedOnlyFieldListFilter),
    )
    
    search_fields = ('title', 'content', 'author__username', 'author__full_name')
    
    ordering = ('-created_at',)
    
    # Fieldsets for the form
    fieldsets = (
        ('Content Information', {
            'fields': ('author', 'title', 'content', 'category', 'difficulty_level')
        }),
        ('Publishing', {
            'fields': ('is_published', 'featured')
        }),
        ('Statistics', {
            'fields': ('read_count',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('read_count', 'created_at', 'updated_at')
    
    # Date hierarchy for easy navigation
    date_hierarchy = 'created_at'
    
    # Custom methods for list display
    def author_link(self, obj):
        url = reverse('admin:users_user_change', args=[obj.author.id])
        return format_html('<a href="{}">{}</a>', url, obj.author.full_name or obj.author.username)
    author_link.short_description = 'Author'
    author_link.admin_order_field = 'author__full_name'
    
    def popularity_indicator(self, obj):
        if obj.read_count > 1000:
            return format_html('<span style="color: green;">🌟 Very Popular</span>')
        elif obj.read_count > 500:
            return format_html('<span style="color: orange;">⭐ Popular</span>')
        elif obj.read_count > 100:
            return format_html('<span style="color: blue;">👁️ Moderate</span>')
        elif obj.read_count > 0:
            return format_html('<span style="color: gray;">👀 Low</span>')
        else:
            return format_html('<span style="color: lightgray;">📖 New</span>')
    popularity_indicator.short_description = 'Popularity'
    
    # Actions
    actions = ['publish_content', 'unpublish_content', 'feature_content', 'unfeature_content']
    
    def publish_content(self, request, queryset):
        count = queryset.update(is_published=True)
        self.message_user(request, f'{count} content items published.')
    publish_content.short_description = 'Publish selected content'
    
    def unpublish_content(self, request, queryset):
        count = queryset.update(is_published=False)
        self.message_user(request, f'{count} content items unpublished.')
    unpublish_content.short_description = 'Unpublish selected content'
    
    def feature_content(self, request, queryset):
        count = queryset.update(featured=True)
        self.message_user(request, f'{count} content items featured.')
    feature_content.short_description = 'Feature selected content'
    
    def unfeature_content(self, request, queryset):
        count = queryset.update(featured=False)
        self.message_user(request, f'{count} content items unfeatured.')
    unfeature_content.short_description = 'Unfeature selected content'
    
    # Customize the changelist view
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response
        
        # Calculate statistics
        metrics = {
            'total_content': qs.count(),
            'published_count': qs.filter(is_published=True).count(),
            'featured_count': qs.filter(featured=True).count(),
            'total_reads': qs.aggregate(Sum('read_count'))['read_count__sum'] or 0,
            'categories': qs.values('category').annotate(count=Count('id')).order_by('-count'),
            'difficulty_levels': qs.values('difficulty_level').annotate(count=Count('id')).order_by('-count'),
        }
        
        response.context_data['summary'] = metrics
        return response
    
    # Optimize queries
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('author')


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ('user_link', 'post_link', 'created_at')
    list_filter = ('created_at', 'post__post_type')
    search_fields = ('user__username', 'user__full_name', 'post__title')
    ordering = ('-created_at',)
    
    def user_link(self, obj):
        url = reverse('admin:users_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.full_name or obj.user.username)
    user_link.short_description = 'User'
    user_link.admin_order_field = 'user__full_name'
    
    def post_link(self, obj):
        url = reverse('admin:content_timelinepost_change', args=[obj.post.id])
        return format_html('<a href="{}">{}</a>', url, obj.post.title)
    post_link.short_description = 'Post'
    post_link.admin_order_field = 'post__title'
    
    # Optimize queries
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('user', 'post')


# Admin site customization
admin.site.site_header = 'Sustainable Fishing Administration'
admin.site.site_title = 'Sustainable Fishing Admin'
admin.site.index_title = 'Welcome to Sustainable Fishing Administration'
