from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from interview.models import DEGREE_TYPE

# Create your models here.

JobTypes = [
    (0, '技术类'),
    (1, '产品类'),
    (2, '运营类'),
    (3, '设计类')
]

Cities = [
    (0, '北京'),
    (1, '上海'),
    (2, '深圳'),
    (3, '广州')
]


class Job(models.Model):
    job_type = models.SmallIntegerField(blank=False, choices=JobTypes, verbose_name='职位类别')
    job_name = models.CharField(max_length=250, blank=False, verbose_name='职位名称')
    job_city = models.SmallIntegerField(choices=Cities, blank=False, verbose_name='工作地点')
    job_responsibility = models.TextField(max_length=1024, verbose_name='职位职责')
    job_requirement = models.TextField(max_length=1024, blank=False, verbose_name='职位要求')
    creator = models.ForeignKey(User, verbose_name='创建人', null=True, on_delete=models.SET_NULL)  # 关联当前登录用户
    created_date = models.DateTimeField(verbose_name='创建时间', default=datetime.now)
    modified_date = models.DateTimeField(verbose_name='修改时间', default=datetime.now)

    class Meta:
        verbose_name = u'职位'
        verbose_name_plural = u'职位'


class Resume(models.Model):
    username = models.CharField(max_length=135, verbose_name=u'姓名')
    applicant = models.ForeignKey(User, verbose_name=u'申请人', null=True, on_delete=models.SET_NULL)
    city = models.CharField(max_length=135, verbose_name=u'城市')
    phone = models.CharField(max_length=135, verbose_name=u'手机号码')
    email = models.EmailField(max_length=135, blank=True, verbose_name=u'邮箱')
    apply_position = models.CharField(max_length=135, blank=True, verbose_name=u'应聘职位')
    born_address = models.CharField(max_length=135, blank=True, verbose_name=u'家乡')
    gender = models.CharField(max_length=135, blank=True, verbose_name=u'性别')

    # 学校与学历信息
    bachelor_school = models.CharField(max_length=135, blank=True, verbose_name=u'本科学校')
    master_school = models.CharField(max_length=135, blank=True, verbose_name=u'研究生学校')
    doctor_school = models.CharField(max_length=135, blank=True, verbose_name=u'博士生学校')
    major = models.CharField(max_length=135, blank=True, verbose_name=u'专业')
    degree = models.CharField(max_length=135, choices=DEGREE_TYPE, blank=True, verbose_name=u'学历')
    created_date = models.DateTimeField(default=datetime.now, verbose_name=u'创建时间')
    modified_date = models.DateTimeField(default=datetime.now, null=True, blank=True, verbose_name=u'更新时间')

    # 候选人自我介绍，工作经历，项目经历
    candidate_introduction = models.TextField(max_length=1024, blank=True, verbose_name=u'自我介绍')
    work_experience = models.TextField(max_length=1024, blank=True, verbose_name=u'工作经历')
    project_experience = models.TextField(max_length=1024, blank=True, verbose_name=u'项目经历')

    class Meta:
        verbose_name = u'简历'
        verbose_name_plural = u'简历'
