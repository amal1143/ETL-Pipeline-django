from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import DataEngineer, APISource, ETLJob
from .models import SystemSettings


# -------------------- Home --------------------

def homepage(request):
    return render(request, "homepage.html")


# -------------------- Logout --------------------

def logout_view(request):
    logout(request)
    return redirect("login")


# -------------------- Login --------------------

def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect("engineer_dashboard")

        messages.error(request, "Invalid Username or Password")

    return render(request, "login.html")


# -------------------- Register --------------------

def register(request):

    if request.method == "POST":

        full_name = request.POST.get("full_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        department = request.POST.get("department")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm_password")

        if password != confirm:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=full_name
        )

        DataEngineer.objects.create(
            user=user,
            department=department
        )

        messages.success(request, "Registration Successful")
        return redirect("login")

    return render(request, "register.html")


# -------------------- Dashboard --------------------

@login_required
def engineer_dashboard(request):

    total_sources = APISource.objects.count()
    total_jobs = ETLJob.objects.count()
    successful_jobs = ETLJob.objects.filter(status="Completed").count()
    failed_jobs = ETLJob.objects.filter(status="Failed").count()

    context = {
        "total_sources": total_sources,
        "total_jobs": total_jobs,
        "successful_jobs": successful_jobs,
        "failed_jobs": failed_jobs,
    }

    return render(request, "engineer_dashboard.html", context)


# -------------------- API Sources --------------------

@login_required
def api_sources(request):

    if request.method == "POST":

        APISource.objects.create(
            api_name=request.POST.get("api_name"),
            base_url=request.POST.get("base_url"),
            api_key=request.POST.get("api_key"),
            status=request.POST.get("status"),
        )

        messages.success(request, "API Source Added Successfully")
        return redirect("api_sources")

    apis = APISource.objects.all()

    return render(
        request,
        "api_sources.html",
        {
            "apis": apis
        }
    )


# -------------------- ETL Jobs --------------------

@login_required
def etl_jobs(request):

    if request.method == "POST":

        api = APISource.objects.get(
            id=request.POST.get("api_source")
        )

        ETLJob.objects.create(
            api_source=api,
            job_name=request.POST.get("job_name"),
            destination_table=request.POST.get("destination_table"),
            schedule=request.POST.get("schedule"),
            status=request.POST.get("status"),
        )

        messages.success(request, "ETL Job Created Successfully")
        return redirect("etl_jobs")

    jobs = ETLJob.objects.all()
    apis = APISource.objects.all()

    return render(
        request,
        "etl_jobs.html",
        {
            "jobs": jobs,
            "apis": apis
        }
    )


# -------------------- Pipeline Execution --------------------

@login_required
def pipeline_execution(request):

    if request.method == "POST":

        job = ETLJob.objects.get(
            id=request.POST.get("job")
        )

        job.status = "Running"
        job.save()

        messages.success(request, "Pipeline Started Successfully")

    jobs = ETLJob.objects.all().order_by("-created_at")

    return render(
        request,
        "pipeline_execution.html",
        {
            "jobs": jobs
        }
    )


# -------------------- ETL Job History --------------------

@login_required
def etl_job_history(request):

    jobs = ETLJob.objects.all().order_by("-created_at")

    return render(
        request,
        "etl_job_history.html",
        {
            "jobs": jobs
        }
    )



# -------------------- Warehouse Synchronization --------------------

@login_required
def warehouse_sync(request):

    jobs = ETLJob.objects.all().order_by("-created_at")

    if request.method == "POST":

        job = ETLJob.objects.get(
            id=request.POST.get("job_id")
        )

        job.status = "Completed"
        job.save()

        messages.success(request, "Data Warehouse Synchronization Completed")

        return redirect("warehouse_sync")

    return render(
        request,
        "warehouse.html",
        {
            "jobs": jobs
        }
    )




@login_required
def warehouse_sync(request):

    jobs = ETLJob.objects.filter(status="Completed")

    return render(
        request,
        "warehouse.html",
        {
            "jobs": jobs
        }
    )




@login_required
def monitoring_dashboard(request):

    total_sources = APISource.objects.count()

    total_jobs = ETLJob.objects.count()

    completed_jobs = ETLJob.objects.filter(
        status="Completed"
    ).count()

    running_jobs = ETLJob.objects.filter(
        status="Running"
    ).count()

    failed_jobs = ETLJob.objects.filter(
        status="Failed"
    ).count()

    context = {
        "total_sources": total_sources,
        "total_jobs": total_jobs,
        "completed_jobs": completed_jobs,
        "running_jobs": running_jobs,
        "failed_jobs": failed_jobs,
    }

    return render(
        request,
        "monitoring_dashboard.html",
        context
    )


@login_required
def reports_dashboard(request):

    total_jobs = ETLJob.objects.count()

    completed = ETLJob.objects.filter(
        status="Completed"
    ).count()

    running = ETLJob.objects.filter(
        status="Running"
    ).count()

    failed = ETLJob.objects.filter(
        status="Failed"
    ).count()

    pending = ETLJob.objects.filter(
        status="Pending"
    ).count()

    jobs = ETLJob.objects.all().order_by("-created_at")

    context = {
        "total_jobs": total_jobs,
        "completed": completed,
        "running": running,
        "failed": failed,
        "pending": pending,
        "jobs": jobs,
    }

    return render(
        request,
        "reports_dashboard.html",
        context
    )



@login_required
def profile(request):

    engineer = DataEngineer.objects.get(
        user=request.user
    )

    return render(
        request,
        "profile.html",
        {
            "engineer": engineer
        }
    )




@login_required
def settings_page(request):

    settings = SystemSettings.objects.first()

    if not settings:

        settings = SystemSettings.objects.create(
            retry_count=3,
            batch_size=1000,
            notification_email="admin@example.com",
            schedule="Daily",
            log_level="INFO"
        )

    if request.method == "POST":

        settings.retry_count = request.POST.get("retry_count")
        settings.batch_size = request.POST.get("batch_size")
        settings.notification_email = request.POST.get("notification_email")
        settings.schedule = request.POST.get("schedule")
        settings.log_level = request.POST.get("log_level")

        settings.save()

        messages.success(request, "Settings Updated Successfully")

        return redirect("settings_page")

    return render(
        request,
        "settings.html",
        {
            "settings": settings
        }
    )

@login_required
def pipeline_logs(request):

    jobs = ETLJob.objects.all().order_by("-created_at")

    return render(
        request,
        "pipeline_logs.html",
        {
            "jobs": jobs
        }
    )

@login_required
def profile(request):

    engineer = DataEngineer.objects.get(
        user=request.user
    )

    return render(
        request,
        "profile.html",
        {
            "engineer": engineer
        }
    )


@login_required
def reports(request):

    total_sources = APISource.objects.count()
    total_jobs = ETLJob.objects.count()

    completed = ETLJob.objects.filter(status="Completed").count()
    running = ETLJob.objects.filter(status="Running").count()
    pending = ETLJob.objects.filter(status="Pending").count()
    failed = ETLJob.objects.filter(status="Failed").count()

    context = {
        "total_sources": total_sources,
        "total_jobs": total_jobs,
        "completed": completed,
        "running": running,
        "pending": pending,
        "failed": failed,
    }

    return render(
        request,
        "reports.html",
        context
    )

@login_required
def data_validation(request):

    jobs = ETLJob.objects.all().order_by("-created_at")

    return render(
        request,
        "data_validation.html",
        {
            "jobs": jobs
        }
    )

@login_required
def notifications(request):

    jobs = ETLJob.objects.all().order_by("-created_at")

    return render(
        request,
        "notifications.html",
        {
            "jobs": jobs
        }
    )

@login_required
def admin_settings(request):

    if request.method == "POST":

        messages.success(
            request,
            "Settings Updated Successfully."
        )

        return redirect("admin_settings")

    return render(
        request,
        "admin_settings.html"
    )

@login_required
def edit_api(request, id):

    api = APISource.objects.get(id=id)

    if request.method == "POST":

        api.api_name = request.POST.get("api_name")
        api.base_url = request.POST.get("base_url")
        api.api_key = request.POST.get("api_key")
        api.status = request.POST.get("status")

        api.save()

        messages.success(request, "API Source Updated Successfully")

        return redirect("api_sources")

    return render(
        request,
        "edit_api.html",
        {
            "api": api
        }
    )


@login_required
def delete_api(request, id):

    api = APISource.objects.get(id=id)

    api.delete()

    messages.success(request, "API Source Deleted Successfully")

    return redirect("api_sources")

@login_required
def etl_job_history(request):

    jobs = ETLJob.objects.all().order_by("-created_at")

    return render(
        request,
        "etl_job_history.html",
        {
            "jobs": jobs
        }
    )

def about(request):
    return render(request, "about.html")