from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from interview.models import DEGREE_TYPE

from django.utils.translation import gettext_lazy as _  # 多语言

# 语言生成命令——django-admin makemessages -l zh_HANS -l en，-l后面对应语言简写
# 语言编译为二进制命令——django-admin compilemessages
# windows系统可能需要安装 gettext，
# https://stackoom.com/question/3dxc9/%E5%9C%A8Windows%E4%B8%AD%E5%AE%89%E8%A3%85gettext-%E6%89%BE%E4%B8%8D%E5%88%B0msguniq-%E7%A1%AE%E4%BF%9D%E6%82%A8%E5%B7%B2%E5%AE%89%E8%A3%85-%E6%88%96%E6%9B%B4%E9%AB%98%E7%89%88%E6%9C%AC%E7%9A%84GNU-gettext%E5%B7%A5%E5%85%B7

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
    # Translators:职位实体的翻译
    job_type = models.SmallIntegerField(blank=False, choices=JobTypes, verbose_name=_('职位类别'))
    job_name = models.CharField(max_length=250, blank=False, verbose_name=_('职位名称'))
    job_city = models.SmallIntegerField(choices=Cities, blank=False, verbose_name=_('工作地点'))
    job_responsibility = models.TextField(max_length=1024, verbose_name=_('职位职责'))
    job_requirement = models.TextField(max_length=1024, blank=False, verbose_name=_('职位要求'))
    creator = models.ForeignKey(User, verbose_name=_('创建人'), null=True, on_delete=models.SET_NULL)  # 关联当前登录用户
    created_date = models.DateTimeField(verbose_name=_('创建时间'), default=datetime.now)
    modified_date = models.DateTimeField(verbose_name=_('修改时间'), default=datetime.now)

    class Meta:
        verbose_name = _('职位')
        verbose_name_plural = _('职位')


class Resume(models.Model):
    # Translators:简历实体的翻译
    username = models.CharField(max_length=135, verbose_name=_('姓名'))
    applicant = models.ForeignKey(User, verbose_name=_('申请人'), null=True, on_delete=models.SET_NULL)
    city = models.CharField(max_length=135, verbose_name=_('城市'))
    phone = models.CharField(max_length=135, verbose_name=_('手机号码'))
    email = models.EmailField(max_length=135, blank=True, verbose_name=_('邮箱'))
    apply_position = models.CharField(max_length=135, blank=True, verbose_name=_('应聘职位'))
    born_address = models.CharField(max_length=135, blank=True, verbose_name=_('家乡'))
    gender = models.CharField(max_length=135, blank=True, verbose_name=_('性别'))

    # 学校与学历信息
    bachelor_school = models.CharField(max_length=135, blank=True, verbose_name=_('本科学校'))
    master_school = models.CharField(max_length=135, blank=True, verbose_name=_('研究生学校'))
    doctor_school = models.CharField(max_length=135, blank=True, verbose_name=_('博士生学校'))
    major = models.CharField(max_length=135, blank=True, verbose_name=_('专业'))
    degree = models.CharField(max_length=135, choices=DEGREE_TYPE, blank=True, verbose_name=_('学历'))
    created_date = models.DateTimeField(default=datetime.now, verbose_name=_('创建时间'))
    modified_date = models.DateTimeField(default=datetime.now, null=True, blank=True, verbose_name=_('更新时间'))

    # 候选人自我介绍，工作经历，项目经历
    candidate_introduction = models.TextField(max_length=1024, blank=True, verbose_name=_('自我介绍'))
    work_experience = models.TextField(max_length=1024, blank=True, verbose_name=_('工作经历'))
    project_experience = models.TextField(max_length=1024, blank=True, verbose_name=_('项目经历'))

    class Meta:
        verbose_name = _('简历')
        verbose_name_plural = _('简历')
