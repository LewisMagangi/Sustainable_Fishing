from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from .models import EducationalContent, TimelinePost
from .forms import EducationalContentForm, ContentFilterForm


def is_educator_or_admin(user):
    """Check if user is educator or admin (as per database schema design notes)"""
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def home_view(request):
    """Home page view showing platform overview and featured content"""
    # Get featured educational content
    featured_content = EducationalContent.objects.filter(
        is_published=True, 
        featured=True
    ).order_by('-created_at')[:3]
    
    # Get recent posts from timeline
    recent_posts = TimelinePost.objects.select_related('author').order_by('-created_at')[:6]
    
    # Get platform statistics
    stats = {
        'total_content': EducationalContent.objects.filter(is_published=True).count(),
        'total_posts': TimelinePost.objects.count(),
        'featured_content_count': featured_content.count(),
    }
    
    # Get latest educational content
    latest_content = EducationalContent.objects.filter(
        is_published=True
    ).order_by('-created_at')[:6]
    
    context = {
        'featured_content': featured_content,
        'recent_posts': recent_posts,
        'latest_content': latest_content,
        'stats': stats,
        'title': 'Home - Sustainable Fishing Platform'
    }
    
    return render(request, 'content/home.html', context)


def content_list(request):
    """Display list of published educational content"""
    contents = EducationalContent.objects.filter(is_published=True).order_by('-featured', '-created_at')
    
    # Filter by category if provided
    category_filter = request.GET.get('category')
    if category_filter:
        contents = contents.filter(category=category_filter)
    
    # Filter by difficulty level if provided
    difficulty_filter = request.GET.get('difficulty_level')
    if difficulty_filter:
        contents = contents.filter(difficulty_level=difficulty_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        contents = contents.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query) |
            Q(author__username__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(contents, 9)  # Show 9 content pieces per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'category_filter': category_filter,
        'difficulty_filter': difficulty_filter,
        'search_query': search_query,
        'category_choices': EducationalContent.CATEGORY_CHOICES,
        'difficulty_choices': EducationalContent.DIFFICULTY_CHOICES,
    }
    return render(request, 'content/content_list.html', context)


def content_detail(request, content_id):
    """Display details of a specific educational content"""
    content = get_object_or_404(EducationalContent, id=content_id, is_published=True)
    
    # Increment read count
    content.increment_read_count()
    
    # Get related content (same category, different content)
    related_content = EducationalContent.objects.filter(
        category=content.category,
        is_published=True
    ).exclude(id=content.id)[:3]
    
    context = {
        'content': content,
        'related_content': related_content,
    }
    return render(request, 'content/content_detail.html', context)


@login_required
@user_passes_test(is_educator_or_admin, login_url='/admin/login/')
def content_create(request):
    """Create new educational content (educators and admins only)"""
    if request.method == 'POST':
        form = EducationalContentForm(request.POST)
        if form.is_valid():
            content = form.save(commit=False)
            content.author = request.user
            content.save()
            messages.success(request, 'Educational content created successfully!')
            return redirect('content:detail', content_id=content.id)
    else:
        form = EducationalContentForm()
    
    context = {'form': form}
    return render(request, 'content/content_form.html', context)


@login_required
@user_passes_test(is_educator_or_admin, login_url='/admin/login/')
def content_update(request, content_id):
    """Update existing educational content (author, educators and admins only)"""
    content = get_object_or_404(EducationalContent, id=content_id)
    
    # Check if user is the author or admin
    if content.author != request.user and not request.user.is_superuser:
        messages.error(request, 'You can only edit your own content.')
        return redirect('content:detail', content_id=content.id)
    
    if request.method == 'POST':
        form = EducationalContentForm(request.POST, instance=content)
        if form.is_valid():
            form.save()
            messages.success(request, 'Educational content updated successfully!')
            return redirect('content:detail', content_id=content.id)
    else:
        form = EducationalContentForm(instance=content)
    
    context = {'form': form, 'content': content}
    return render(request, 'content/content_form.html', context)


@login_required
@user_passes_test(is_educator_or_admin, login_url='/admin/login/')
def content_delete(request, content_id):
    """Delete educational content (author, educators and admins only)"""
    content = get_object_or_404(EducationalContent, id=content_id)
    
    # Check if user is the author or admin
    if content.author != request.user and not request.user.is_superuser:
        messages.error(request, 'You can only delete your own content.')
        return redirect('content:detail', content_id=content.id)
    
    if request.method == 'POST':
        content.delete()
        messages.success(request, 'Educational content deleted successfully!')
        return redirect('content:content_list')
    
    context = {'content': content}
    return render(request, 'content/content_confirm_delete.html', context)


@login_required
@user_passes_test(is_educator_or_admin, login_url='/admin/login/')
def my_content(request):
    """Display current user's educational content"""
    contents = EducationalContent.objects.filter(author=request.user).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(contents, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'page_obj': page_obj}
    return render(request, 'content/my_content.html', context)


def featured_content(request):
    """Display featured educational content"""
    contents = EducationalContent.objects.filter(is_published=True, featured=True).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(contents, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'page_obj': page_obj}
    return render(request, 'content/featured_content.html', context)
