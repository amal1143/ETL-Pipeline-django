from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import DataEngineer, APISource, ETLJob, SystemSettings


# -------------------- HOME --------------------

def homepage(request):
    return render(request, "homepage.html")


def about(request):
    return render(request, "about.html")


# -------------------- AUTHENTICATION --------------------

def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("engineer_dashboard")

        messages.error(request, "Invalid Username or Password")

    return render(request, "login.html")


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

        DataEngineer.objects.create(user=user, department=department)

        messages.success(request, "Registration Successful")
        return redirect("login")

    return render(request, "register.html")


def logout_view(request):
    logout(request)
    return redirect("login")


# -------------------- DASHBOARD --------------------

@login_required
def engineer_dashboard(request):

    context = {
        "total_sources": APISource.objects.filter(created_by=request.user).count(),
        "total_jobs": ETLJob.objects.filter(created_by=request.user).count(),
        "successful_jobs": ETLJob.objects.filter(created_by=request.user, status="Completed").count(),
        "failed_jobs": ETLJob.objects.filter(created_by=request.user, status="Failed").count(),
    }

    return render(request, "engineer_dashboard.html", context)


# -------------------- API SOURCES --------------------

@login_required
def api_sources(request):

    if request.method == "POST":

        APISource.objects.create(
            created_by=request.user,
            api_name=request.POST.get("api_name"),
            base_url=request.POST.get("base_url"),
            api_key=request.POST.get("api_key"),
            status=request.POST.get("status"),
        )

        messages.success(request, "API Source Added Successfully")
        return redirect("api_sources")

    apis = APISource.objects.filter(created_by=request.user)

    return render(request, "api_sources.html", {"apis": apis})


@login_required
def edit_api(request, id):

    api = get_object_or_404(APISource, id=id, created_by=request.user)

    if request.method == "POST":
        api.api_name = request.POST.get("api_name")
        api.base_url = request.POST.get("base_url")
        api.api_key = request.POST.get("api_key")
        api.status = request.POST.get("status")
        api.save()

        messages.success(request, "API Source Updated Successfully")
        return redirect("api_sources")

    return render(request, "edit_api.html", {"api": api})


@login_required
def delete_api(request, id):

    api = get_object_or_404(APISource, id=id, created_by=request.user)
    api.delete()

    messages.success(request, "API Source Deleted Successfully")
    return redirect("api_sources")


# -------------------- ETL JOBS --------------------

@login_required
def etl_jobs(request):

    if request.method == "POST":

        api = get_object_or_404(
            APISource,
            id=request.POST.get("api_source"),
            created_by=request.user
        )

        ETLJob.objects.create(
            created_by=request.user,
            api_source=api,
            job_name=request.POST.get("job_name"),
            destination_table=request.POST.get("destination_table"),
            schedule=request.POST.get("schedule"),
            status=request.POST.get("status"),
        )

        messages.success(request, "ETL Job Created Successfully")
        return redirect("etl_jobs")

    context = {
        "jobs": ETLJob.objects.filter(created_by=request.user),
        "apis": APISource.objects.filter(created_by=request.user)
    }

    return render(request, "etl_jobs.html", context)


# -------------------- COMMON JOB QUERY --------------------

def user_jobs(request):
    return ETLJob.objects.filter(created_by=request.user).order_by("-created_at")


# -------------------- PIPELINE EXECUTION --------------------

@login_required
def pipeline_execution(request):

    if request.method == "POST":

        job = get_object_or_404(
            ETLJob,
            id=request.POST.get("job"),
            created_by=request.user
        )

        job.status = "Running"
        job.save()

        messages.success(request, "Pipeline Started Successfully")

    return render(request, "pipeline_execution.html", {"jobs": user_jobs(request)})


# -------------------- WAREHOUSE SYNC --------------------

@login_required
def warehouse_sync(request):

    if request.method == "POST":

        job = get_object_or_404(
            ETLJob,
            id=request.POST.get("job_id"),
            created_by=request.user
        )

        job.status = "Completed"
        job.save()

        messages.success(request, "Data Warehouse Synchronization Completed")
        return redirect("warehouse_sync")

    return render(request, "warehouse.html", {"jobs": user_jobs(request)})

# -------------------- WAREHOUSE SYNC --------------------

@login_required
def warehouse_sync(request):

    jobs = user_jobs(request)

    return render(request,"warehouse.html",{"jobs": jobs})

@login_required
def sync_warehouse(request, id):

    job = get_object_or_404(
        ETLJob,
        id=id,
        created_by=request.user
    )

    job.status = "Running"
    job.save()
    job.status = "Completed"
    job.save()
    messages.success(request,"Data Warehouse Synchronization Completed Successfully")
    return redirect("warehouse_sync")
# -------------------- ETL JOB HISTORY --------------------

@login_required
def etl_job_history(request):
    return render(request, "etl_job_history.html", {"jobs": user_jobs(request)})


# -------------------- MONITORING --------------------

@login_required
def monitoring_dashboard(request):

    jobs = ETLJob.objects.filter(created_by=request.user)

    context = {
        "total_sources": APISource.objects.filter(created_by=request.user).count(),
        "total_jobs": jobs.count(),
        "completed_jobs": jobs.filter(status="Completed").count(),
        "running_jobs": jobs.filter(status="Running").count(),
        "failed_jobs": jobs.filter(status="Failed").count(),
    }

    return render(request, "monitoring_dashboard.html", context)


# -------------------- REPORTS --------------------

@login_required
def reports(request):

    jobs = ETLJob.objects.filter(created_by=request.user)

    context = {
        "total_sources": APISource.objects.filter(created_by=request.user).count(),
        "total_jobs": jobs.count(),
        "completed": jobs.filter(status="Completed").count(),
        "running": jobs.filter(status="Running").count(),
        "pending": jobs.filter(status="Pending").count(),
        "failed": jobs.filter(status="Failed").count(),
    }

    return render(request, "reports.html", context)


# -------------------- PROFILE --------------------

@login_required
def profile(request):

    engineer = get_object_or_404(DataEngineer, user=request.user)

    return render(request, "profile.html", {"engineer": engineer})


# -------------------- SETTINGS --------------------

@login_required
def settings_page(request):

    settings = SystemSettings.objects.first()

    if not settings:
        settings = SystemSettings.objects.create(notification_email="admin@example.com")

    if request.method == "POST":
        settings.retry_count = request.POST.get("retry_count")
        settings.batch_size = request.POST.get("batch_size")
        settings.notification_email = request.POST.get("notification_email")
        settings.schedule = request.POST.get("schedule")
        settings.log_level = request.POST.get("log_level")
        settings.save()

        messages.success(request, "Settings Updated Successfully")
        return redirect("settings_page")

    return render(request, "settings.html", {"settings": settings})


# -------------------- PIPELINE LOGS --------------------

@login_required
def pipeline_logs(request):
    return render(request, "pipeline_logs.html", {"jobs": user_jobs(request)})


# -------------------- DATA VALIDATION --------------------

@login_required
def data_validation(request):
    return render(request, "data_validation.html", {"jobs": user_jobs(request)})


# -------------------- NOTIFICATIONS --------------------

@login_required
def notifications(request):
    return render(request, "notifications.html", {"jobs": user_jobs(request)})


# -------------------- ADMIN SETTINGS --------------------

@login_required
def admin_settings(request):

    if request.method == "POST":
        messages.success(request, "Settings Updated Successfully.")
        return redirect("admin_settings")

    return render(request, "admin_settings.html")