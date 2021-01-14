from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DetailView
from django.contrib.auth.models import User, Group
import logging

from .models import Job, Resume, Cities, JobTypes

logger = logging.getLogger(__name__)


def joblist(request):
    job_list = Job.objects.order_by('job_type')
    # template = loader.get_template('joblist.html')
    context = {'job_list': job_list}

    for job in job_list:
        job.city_name = Cities[job.job_city][1]
        job.type_name = JobTypes[job.job_type][1]

    # return HttpResponse(template.render(context))
    return render(request, 'joblist.html', context)


def detail(request, job_id):
    try:
        job = Job.objects.get(pk=job_id)
        job.city_name = Cities[job.job_city][1]
        logger.info('job info fetched from database jobid:%s' % job_id)  # 测试页面缓存功能
    except Job.DoesNotExist:
        raise Http404("Job does not exist")
    return render(request, 'job.html', {'job': job})


class ResumeDetailView(DetailView):
    '''
    简历详情页
    '''
    model = Resume
    template_name = 'resume_detail.html'


# 这个URL仅允许有创建用户权限的用户访问
# @csrf_exempt  # 不处理CSRF攻击
@permission_required('auth.user_add')
def create_hr_user(request):
    if request.method == 'GET':
        return render(request, 'create_hr_user.html', {})
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        hr_group = Group.objects.get(name='hr')
        user = User(is_superuser=False, username=username, is_active=True, is_staff=True)
        user.set_password(password)
        user.save()
        user.groups.add(hr_group)

        messages.add_message(request, messages.INFO, 'user created %s' % username)
        return render(request, 'create_hr_user.html')
    return render(request, 'create_hr_user.html')


def detail_resume(request, resume_id):
    '''直接返回HTML内容的视图（这段代码返回的页面有XSS漏洞，能够被攻击者利用）'''
    try:
        resume = Resume.objects.get(pk=resume_id)
        content = "name: %s <br> introduction: %s <br>" % (resume.username, resume.candidate_introduction)
        return HttpResponse(content)
    except Resume.DoesNotExist:
        raise Http404('resume does not exist')


class ResumeCreateView(LoginRequiredMixin, CreateView):
    '''
    简历职位页面
    '''
    template_name = 'resume_form.html'
    success_url = '/joblist/'
    model = Resume
    fields = ["username", "city", "phone", "gender", "email", "apply_position",
              'bachelor_school', 'master_school', 'doctor_school', "major", "degree",
              "candidate_introduction", "work_experience", "project_experience"]

    def get_initial(self):
        '''
        从URL请求参数带入默认值
        :return:
        '''
        initial = {}
        for x in self.request.GET:
            initial[x] = self.request.GET[x]
        return initial

    def form_valid(self, form):
        '''
        简历跟当前用户关联
        :param form:
        :return:
        '''
        self.object = form.save(commit=False)
        self.object.applicant = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
