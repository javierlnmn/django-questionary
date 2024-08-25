from django.urls import path
from django.contrib.auth import views as auth_views
from users import views

app_name='users'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('login/<int:user_id>/', views.login_user, name='login_user'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
