from django.db import models
from django.contrib.auth.models import User


class DataEngineer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class APISource(models.Model):

    api_name = models.CharField(max_length=100)
    base_url = models.URLField()
    api_key = models.CharField(max_length=255)
    status = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.api_name
    
class ETLJob(models.Model):

    api_source = models.ForeignKey(APISource, on_delete=models.CASCADE)

    job_name = models.CharField(max_length=100)

    destination_table = models.CharField(max_length=100)

    schedule = models.CharField(max_length=50)

    status = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.job_name    
    

class ETLHistory(models.Model):

    job = models.ForeignKey(ETLJob,on_delete=models.CASCADE)

    execution_date = models.DateTimeField(auto_now_add=True)

    records_processed = models.IntegerField()

    duration = models.CharField(max_length=50)

    status = models.CharField(max_length=20)

    def __str__(self):
        return self.job.job_name


class SystemSettings(models.Model):

    retry_count = models.IntegerField(default=3)

    batch_size = models.IntegerField(default=1000)

    notification_email = models.EmailField()

    schedule = models.CharField(max_length=50)

    log_level = models.CharField(max_length=20)

    def __str__(self):
        return "System Settings"