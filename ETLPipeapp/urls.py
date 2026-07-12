from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path("about/", views.about, name="about"),

    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),

    path('dashboard/', views.engineer_dashboard, name='engineer_dashboard'),
    path('logout/', views.logout_view, name='logout'),

    path('api-sources/', views.api_sources, name='api_sources'),
    path('etl-jobs/', views.etl_jobs, name='etl_jobs'),

    path('pipeline/', views.pipeline_execution, name='pipeline'),

    path('warehouse-sync/', views.warehouse_sync, name='warehouse_sync'),

  
    path('etl-job-history/',views.etl_job_history,name='etl_job_history'),
]