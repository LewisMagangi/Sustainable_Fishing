from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum, Avg
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from users.models import User
from fishing.models import Catch
from content.models import TimelinePost, EducationalContent


def admin_statistics_context(request):
    """
    Context processor to provide statistics to admin templates
    """
    if not request.user.is_staff:
        return {}
    
    try:
        # User statistics
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        fishermen_count = User.objects.filter(role='fisherman').count()
        educators_count = User.objects.filter(role='educator').count()
        
        # Fishing statistics
        total_catches = Catch.objects.count()
        total_weight = Catch.objects.aggregate(Sum('weight'))['weight__sum'] or 0
        total_revenue = Catch.objects.filter(status='sold').aggregate(Sum('price'))['price__sum'] or 0
        avg_catch_weight = Catch.objects.aggregate(Avg('weight'))['weight__avg'] or 0
        
        # Content statistics
        total_posts = TimelinePost.objects.count()
        total_educational = EducationalContent.objects.count()
        published_educational = EducationalContent.objects.filter(is_published=True).count()
        total_likes = TimelinePost.objects.aggregate(Sum('likes_count'))['likes_count__sum'] or 0
        
        return {
            'admin_stats': {
                'total_users': total_users,
                'active_users': active_users,
                'fishermen_count': fishermen_count,
                'educators_count': educators_count,
                'total_catches': total_catches,
                'total_weight': round(total_weight, 2) if total_weight else 0,
                'total_revenue': total_revenue,
                'avg_catch_weight': round(avg_catch_weight, 2) if avg_catch_weight else 0,
                'total_posts': total_posts,
                'total_educational': total_educational,
                'published_educational': published_educational,
                'total_likes': total_likes,
            }
        }
    except Exception:
        return {'admin_stats': {}}


@method_decorator(staff_member_required, name='dispatch')
class AdminDashboardView(TemplateView):
    """
    Custom admin dashboard view with enhanced statistics
    """
    template_name = 'admin/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get comprehensive statistics
        context.update(admin_statistics_context(self.request))
        
        # Get recent activity
        context['recent_users'] = User.objects.select_related().order_by('-created_at')[:5]
        context['recent_catches'] = Catch.objects.select_related('fisher').order_by('-created_at')[:5]
        context['recent_posts'] = TimelinePost.objects.select_related('author').order_by('-created_at')[:5]
        context['recent_educational'] = EducationalContent.objects.select_related('author').order_by('-created_at')[:5]
        
        # Get top performers
        context['top_fishermen'] = User.objects.filter(role='fisherman').annotate(
            catch_count=Count('catches')
        ).order_by('-catch_count')[:5]
        
        context['top_educators'] = User.objects.filter(role='educator').annotate(
            content_count=Count('educational_content')
        ).order_by('-content_count')[:5]
        
        context['popular_posts'] = TimelinePost.objects.order_by('-likes_count')[:5]
        
        return context
