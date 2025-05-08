from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.survey_list, name='survey_list'),
    path('new/', views.create_survey, name='create_survey'),
    path('survey-admin/', views.admin_survey, name='admin_survey'),
    path('edit/<int:survey_id>/', views.edit_survey, name='edit_survey'),
    path('respond/<int:survey_id>/', views.respond_survey, name='respond_survey'),
    path('results/<int:survey_id>/', views.survey_results, name='survey_results'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('publish/<int:survey_id>/', views.publish_survey, name='publish_survey'),
    path('unpublish/<int:survey_id>/', views.unpublish_survey, name='unpublish_survey'),
    path('delete/<int:survey_id>/', views.delete_survey, name='delete_survey'),
    
]