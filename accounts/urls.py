from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path(
        'dashboard/dispatcher/',
        views.dispatcher_dashboard,
        name='dispatcher_dashboard',
    ),
    path('dashboard/driver/', views.driver_dashboard, name='driver_dashboard'),
    path('dashboard/client/', views.client_dashboard, name='client_dashboard'),
    path('profile/', views.profile_view, name='profile'),
]