from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    # 职位列表
    url(r'^joblist/', views.joblist, name='joblist'),
    # 职位详情
    url(r'^job/(?P<job_id>\d+)/$', views.detail, name='detail'),

    # 提交简历
    path('resume/add/', views.ResumeCreateView.as_view(), name='resume-add'),
    # 简历详情
    path('resume/<int:pk>/', views.ResumeDetailView.as_view(), name='resume-detail'),

    # 管理员创建HR账号的页面
    path('create_hr_user/', views.create_hr_user, name='create_hr_user'),

    # 首页自动跳转到职位列表
    url(r'^$', views.joblist, name='index')
]

from django.conf import settings

if settings.DEBUG:
    # 有XSS漏洞的视图页面
    urlpatterns += [
        url(r'detail_resume/(?P<resume_id>\d+)/$', views.detail_resume, name='detail_resume'),
    ]
