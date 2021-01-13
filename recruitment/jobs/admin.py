from django.contrib import admin
from .models import Job, Resume
from interview.models import Candidate
from datetime import datetime
from django.contrib import messages


# Register your models here.
class JobAdmin(admin.ModelAdmin):
    '''
    职位管理类
    '''
    exclude = ('creator', 'created_date', 'modified_date')
    list_display = ('job_name', 'job_type', 'job_city', 'creator', 'created_date', 'modified_date')

    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        super().save_model(request, obj, form, change)


def enter_interview_process(modeladmin, request, queryset):
    '''
    勾选候选人简历，进入面试
    :param modeladmin:
    :param request:
    :param queryset:
    :return:
    '''
    candidate_names = ""
    for resume in queryset:
        candidate = Candidate()
        # 把obj中所有对应属性，拷贝到candidate对象中
        candidate.__dict__.update(resume.__dict__)
        candidate.created_date = datetime.now()
        candidate.modified_date = datetime.now()
        candidate_names += candidate.username + ","
        candidate.creator = request.user.username
        candidate.save()
    messages.add_message(request, messages.INFO, '候选人：%s已成功进入面试流程' % candidate_names)


enter_interview_process.short_description = u"进入面试流程"


class ResumeAdmin(admin.ModelAdmin):
    '''
    简历管理类
    '''
    actions = [enter_interview_process, ]

    # exclude = ('applicant', 'created_date', 'modified_date')

    list_display = (
        'username', 'applicant', 'city', 'apply_position', 'bachelor_school', 'master_school', 'doctor_school', 'major',
        'created_date')

    readonly_fields = ('applicant', 'created_date', 'modified_date')

    fieldsets = (
        (None, {'fields': (
            "applicant", ("username", "city", "phone", "gender"), ("email", "apply_position", "born_address"),
            ('bachelor_school', 'master_school', 'doctor_school'), ("major", "degree"),
            ('created_date', 'modified_date'),
            "candidate_introduction", "work_experience", "project_experience",
        )}),
    )

    def save_model(self, request, obj, form, change):
        obj.applicant = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Job, JobAdmin)
admin.site.register(Resume, ResumeAdmin)
