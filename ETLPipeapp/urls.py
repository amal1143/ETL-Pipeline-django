from django.urls import path
from . import views


urlpatterns = [

    # Home
    path('', views.homepage, name='homepage'),

    path('about/', views.about, name='about'),


    # Authentication
    path('login/', views.login_view, name='login'),

    path('register/', views.register, name='register'),

    path('logout/', views.logout_view, name='logout'),


    # Dashboard
    path('dashboard/',views.engineer_dashboard,name='engineer_dashboard'),


    # API Source CRUD
    path('api-sources/',views.api_sources,name='api_sources'),

    path('api-sources/edit/<int:id>/',views.edit_api,name='edit_api'),

    path('api-sources/delete/<int:id>/',views.delete_api,name='delete_api'),



    # ETL
    path('etl-jobs/',views.etl_jobs,name='etl_jobs'),


    path('pipeline/',views.pipeline_execution,name='pipeline'),


    path('warehouse-sync/',views.warehouse_sync,name='warehouse_sync'),


    path('etl-job-history/',views.etl_job_history,name='etl_job_history'),


    # Other Pages
    path('monitoring/',views.monitoring_dashboard,name='monitoring_dashboard'),


    path('reports/',views.reports,name='reports'),


    path('profile/',views.profile,name='profile'),


    path('settings/',views.settings_page,name='settings_page'),


    path('logs/',views.pipeline_logs,name='pipeline_logs'),


]