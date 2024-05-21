from django.urls import path
from . import views

urlpatterns = [
    path('account_recovery/', views.account_recovery, name='account_recovery'),
    path('', views.login_view, name='login'),
    path('insecure_storage/', views.insecure_storage, name='insecure_storage'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
]
