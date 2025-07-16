from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Catch
from .forms import CatchForm


def catch_list(request):
    """Display list of all catches"""
    catches = Catch.objects.select_related('fisher').order_by('-catch_date', '-created_at')
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        catches = catches.filter(status=status_filter)
    
    # Filter by fish type if provided
    fish_type_filter = request.GET.get('fish_type')
    if fish_type_filter:
        catches = catches.filter(fish_type__icontains=fish_type_filter)
    
    # Pagination
    paginator = Paginator(catches, 12)  # Show 12 catches per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'fish_type_filter': fish_type_filter,
        'status_choices': Catch.STATUS_CHOICES,
    }
    return render(request, 'fishing/catch_list.html', context)


def catch_detail(request, catch_id):
    """Display details of a specific catch"""
    catch = get_object_or_404(Catch, id=catch_id)
    context = {'catch': catch}
    return render(request, 'fishing/catch_detail.html', context)


@login_required
def catch_create(request):
    """Create a new catch entry"""
    if request.method == 'POST':
        form = CatchForm(request.POST)
        if form.is_valid():
            catch = form.save(commit=False)
            catch.fisher = request.user
            catch.save()
            messages.success(request, 'Catch logged successfully!')
            return redirect('fishing:catch_detail', catch_id=catch.id)
    else:
        form = CatchForm()
    
    context = {'form': form}
    return render(request, 'fishing/catch_form.html', context)


@login_required
def catch_update(request, catch_id):
    """Update an existing catch entry"""
    catch = get_object_or_404(Catch, id=catch_id, fisher=request.user)
    
    if request.method == 'POST':
        form = CatchForm(request.POST, instance=catch)
        if form.is_valid():
            form.save()
            messages.success(request, 'Catch updated successfully!')
            return redirect('fishing:catch_detail', catch_id=catch.id)
    else:
        form = CatchForm(instance=catch)
    
    context = {'form': form, 'catch': catch}
    return render(request, 'fishing/catch_form.html', context)


@login_required
def catch_delete(request, catch_id):
    """Delete a catch entry"""
    catch = get_object_or_404(Catch, id=catch_id, fisher=request.user)
    
    if request.method == 'POST':
        catch.delete()
        messages.success(request, 'Catch deleted successfully!')
        return redirect('fishing:catch_list')
    
    context = {'catch': catch}
    return render(request, 'fishing/catch_confirm_delete.html', context)


@login_required
def my_catches(request):
    """Display current user's catches"""
    catches = Catch.objects.filter(fisher=request.user).order_by('-catch_date', '-created_at')
    
    # Pagination
    paginator = Paginator(catches, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'page_obj': page_obj}
    return render(request, 'fishing/my_catches.html', context)
