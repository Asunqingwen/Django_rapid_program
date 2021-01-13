from django.contrib import admin
from .models import JobsResume, JobsJob, Candidate

# Register your models here.

admin.site.register(JobsResume)
admin.site.register(JobsJob)
admin.site.register(Candidate)
