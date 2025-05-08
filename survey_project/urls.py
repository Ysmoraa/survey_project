# survey_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from survey_app import views as survey_views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', survey_views.registro, name='signup'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('', include('survey_app.urls')),
    
]