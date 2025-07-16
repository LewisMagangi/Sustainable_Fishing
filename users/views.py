from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DetailView, ListView

from .models import User
from .forms import UserRegistrationForm, UserLoginForm, ProfileUpdateForm, PasswordChangeForm
from fishing.models import Catch
from content.models import TimelinePost, EducationalContent


def register_view(request):
    """Handle user registration"""
    if request.user.is_authenticated:
        return redirect('users:profile')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('users:login')
    else:
        form = UserRegistrationForm()
    
    context = {
        'form': form,
        'title': 'Register - Sustainable Fishing'
    }
    return render(request, 'users/register.html', context)


def login_view(request):
    """Handle user login"""
    if request.user.is_authenticated:
        return redirect('users:profile')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.full_name or user.username}!')
                next_url = request.GET.get('next')
                return redirect(next_url) if next_url else redirect('users:profile')
    else:
        form = UserLoginForm()
    
    context = {
        'form': form,
        'title': 'Login - Sustainable Fishing'
    }
    return render(request, 'users/login.html', context)


@login_required
def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('users:login')


@login_required
def profile_view(request):
    """Display user profile"""
    user = request.user
    
    # Get user's recent catches
    recent_catches = Catch.objects.filter(fisher=user).order_by('-created_at')[:5]
    
    # Get user's recent timeline posts
    recent_posts = TimelinePost.objects.filter(author=user).order_by('-created_at')[:5]
    
    # Get user's educational content if they're an educator
    educational_content = None
    if user.role == 'educator':
        educational_content = EducationalContent.objects.filter(author=user).order_by('-created_at')[:5]
    
    # Calculate stats
    total_catches = Catch.objects.filter(fisher=user).count()
    total_posts = TimelinePost.objects.filter(author=user).count()
    total_educational = EducationalContent.objects.filter(author=user).count() if user.role == 'educator' else 0
    
    context = {
        'user': user,
        'recent_catches': recent_catches,
        'recent_posts': recent_posts,
        'educational_content': educational_content,
        'total_catches': total_catches,
        'total_posts': total_posts,
        'total_educational': total_educational,
        'title': f'{user.full_name or user.username} - Profile'
    }
    return render(request, 'users/profile.html', context)


@login_required
def edit_profile_view(request):
    """Handle profile editing"""
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('users:profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    context = {
        'form': form,
        'title': 'Edit Profile - Sustainable Fishing'
    }
    return render(request, 'users/edit_profile.html', context)


@login_required
def change_password_view(request):
    """Handle password change"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password has been changed successfully.')
            return redirect('users:profile')
    else:
        form = PasswordChangeForm(request.user)
    
    context = {
        'form': form,
        'title': 'Change Password - Sustainable Fishing'
    }
    return render(request, 'users/change_password.html', context)


def user_detail_view(request, user_id):
    """Display public user profile"""
    user = get_object_or_404(User, id=user_id)
    
    # Get user's public information
    recent_catches = Catch.objects.filter(fisher=user).order_by('-created_at')[:10]
    recent_posts = TimelinePost.objects.filter(author=user).order_by('-created_at')[:10]
    
    # Get educational content if they're an educator
    educational_content = None
    if user.role == 'educator':
        educational_content = EducationalContent.objects.filter(
            author=user, 
            is_published=True
        ).order_by('-created_at')[:10]
    
    # Calculate public stats
    total_catches = Catch.objects.filter(fisher=user).count()
    total_posts = TimelinePost.objects.filter(author=user).count()
    total_educational = EducationalContent.objects.filter(
        author=user, 
        is_published=True
    ).count() if user.role == 'educator' else 0
    
    context = {
        'profile_user': user,
        'recent_catches': recent_catches,
        'recent_posts': recent_posts,
        'educational_content': educational_content,
        'total_catches': total_catches,
        'total_posts': total_posts,
        'total_educational': total_educational,
        'title': f'{user.full_name or user.username} - Profile'
    }
    return render(request, 'users/user_detail.html', context)


class UserListView(ListView):
    """List all users with search and filter functionality"""
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = User.objects.all().order_by('-created_at')
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(username__icontains=search_query) |
                Q(full_name__icontains=search_query) |
                Q(location__icontains=search_query)
            )
        
        # Filter by role
        role_filter = self.request.GET.get('role')
        if role_filter:
            queryset = queryset.filter(role=role_filter)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Community Members - Sustainable Fishing'
        context['search_query'] = self.request.GET.get('search', '')
        context['role_filter'] = self.request.GET.get('role', '')
        context['role_choices'] = User.ROLE_CHOICES
        return context


@login_required
def dashboard_view(request):
    """Dashboard view showing user statistics and overview"""
    user = request.user
    
    # Get user stats
    total_catches = Catch.objects.filter(fisher=user).count()
    total_posts = TimelinePost.objects.filter(author=user).count()
    total_educational = EducationalContent.objects.filter(author=user).count()
    
    # Get recent activity
    recent_catches = Catch.objects.filter(fisher=user).order_by('-created_at')[:5]
    recent_posts = TimelinePost.objects.filter(author=user).order_by('-created_at')[:5]
    
    # Get community stats (if admin)
    community_stats = {}
    if user.role == 'admin':
        community_stats = {
            'total_users': User.objects.count(),
            'total_fishermen': User.objects.filter(role='fisherman').count(),
            'total_educators': User.objects.filter(role='educator').count(),
            'total_catches': Catch.objects.count(),
            'total_posts': TimelinePost.objects.count(),
            'total_educational': EducationalContent.objects.count(),
        }
    
    context = {
        'user': user,
        'total_catches': total_catches,
        'total_posts': total_posts,
        'total_educational': total_educational,
        'recent_catches': recent_catches,
        'recent_posts': recent_posts,
        'community_stats': community_stats,
        'title': f'Dashboard - {user.full_name or user.username}'
    }
    return render(request, 'users/dashboard.html', context)


@login_required
@require_http_methods(['POST'])
def delete_account_view(request):
    """Handle account deletion"""
    user = request.user
    
    # Log out the user
    logout(request)
    
    # Delete the user account
    user.delete()
    
    messages.success(request, 'Your account has been deleted successfully.')
    return redirect('users:login')


# API-style views for AJAX requests
@login_required
@csrf_exempt
def api_user_stats(request):
    """API endpoint for user statistics"""
    if request.method == 'GET':
        user = request.user
        stats = {
            'total_catches': Catch.objects.filter(fisher=user).count(),
            'total_posts': TimelinePost.objects.filter(author=user).count(),
            'total_educational': EducationalContent.objects.filter(author=user).count(),
            'member_since': user.created_at.strftime('%B %Y'),
            'role': user.get_role_display(),
            'location': user.location,
        }
        return JsonResponse(stats)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Class-based view for updating user profile"""
    model = User
    form_class = ProfileUpdateForm
    template_name = 'users/edit_profile.html'
    success_url = reverse_lazy('users:profile')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Your profile has been updated successfully.')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Profile - Sustainable Fishing'
        return context
