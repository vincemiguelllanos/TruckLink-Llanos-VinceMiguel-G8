from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, redirect, render
from .forms import UserProfileUpdateForm, UserRegistrationForm
from .models import UserProfile


def register_view(request):
  if request.method == 'POST':
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      user.set_password(form.cleaned_data['password'])
      user.save()
      UserProfile.objects.create(
          user=user,
          role=form.cleaned_data['role'],
          contact_number=form.cleaned_data.get('contact_number'),
      )
      messages.success(
          request, 'Registration successful! You can now log in.'
      )
      return redirect('login')
  else:
    form = UserRegistrationForm()
  return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
  if request.method == 'POST':
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
      user = form.get_user()
      login(request, user)
      role = user.profile.role
      if role in ['admin', 'dispatcher']:
        return redirect('dispatcher_dashboard')
      elif role == 'driver':
        return redirect('driver_dashboard')
      else:
        return redirect('client_dashboard')
  else:
    form = AuthenticationForm()
  return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
  logout(request)
  return redirect('login')


@login_required
def dispatcher_dashboard(request):
  if request.user.profile.role not in ['admin', 'dispatcher']:
    return redirect('login')
  return render(request, 'dashboards/dispatcher.html')


@login_required
def driver_dashboard(request):
  if request.user.profile.role != 'driver':
    return redirect('login')
  return render(request, 'dashboards/driver.html')


@login_required
def client_dashboard(request):
  if request.user.profile.role != 'client':
    return redirect('login')
  return render(request, 'dashboards/client.html')


@login_required
def profile_view(request):
  profile = get_object_or_404(UserProfile, user=request.user)
  if request.method == 'POST':
    profile_form = UserProfileUpdateForm(
        request.POST, request.FILES, instance=profile
    )
    request.user.first_name = request.POST.get('first_name')
    request.user.last_name = request.POST.get('last_name')
    request.user.email = request.POST.get('email')
    if profile_form.is_valid():
      request.user.save()
      profile_form.save()
      messages.success(request, 'Profile updated successfully.')
      return redirect('profile')
  else:
    profile_form = UserProfileUpdateForm(instance=profile)
  return render(
      request,
      'accounts/profile.html',
      {'profile': profile, 'profile_form': profile_form},
  )