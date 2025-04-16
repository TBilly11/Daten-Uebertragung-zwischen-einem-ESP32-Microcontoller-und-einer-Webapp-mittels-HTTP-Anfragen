"""lock_web_interface URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from lock_web_interface.views import home, api, admin as management

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home.home, name="home"),
    path('home', home.home, name="home"),
    path('login', home.login, name="login"),
    path('logout', home.logout, name="logout"),
    path('signup', home.signup, name="signup"),
    path('management', management.ManagementView.as_view(), name="management"),
    path('management/users', management.UserView.as_view(), name="management_users"),
    path('management/toggle_auth', management.OneAuthUsersView.as_view(), name="management_toggle_auth"),
    path('management/login_entries', management.LogEntryView.as_view(), name="management_login_entries"),
    path('api/send_mail', api.send_mail_with_login_code, name="api_send_mail"),
    path('api/one_factor_auth', api.can_authenticate_with_one_factor, name="api_one_factor_auth"),
    path('api/login_entry', api.add_login_entry, name="api_login_entry"),
]
