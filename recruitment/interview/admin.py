import codecs
import csv
from datetime import datetime

from django.contrib import admin
from django.db.models import Q
from django.http import HttpResponse

from .models import Candidate
from . import candidate_fieldset as CF
from . import dingtalk
import logging

# Register your models here.

logger = logging.getLogger(__name__)

exportable_fields = ('username', 'city', 'phone', 'bachelor_school', 'master_school', 'degree', 'first_result',
                     'first_interviewer_user', 'second_result', 'second_interviewer_user', 'hr_result', 'hr_score',
                     'hr_remark',
                     'hr_interviewer_user')


def notify_interviewer(modeladmin, request, queryset):
    '''
    钉钉通知一面面试官
    :param modeladmin:
    :param request:
    :param queryset:
    :return:
    '''
    candidates = ""
    interviewers = ""
    for obj in queryset:
        candidates += obj.username + ";"
        interviewers += obj.first_interviewer_user.username + ";"
    dingtalk.send("候选人%s进入面试环节，亲爱的面试官，请准备好面试：%s" % (candidates, interviewers))


notify_interviewer.short_description = u'通知一面面试官'


def export_model_as_csv(modeladmin, request, queryset):
    '''
    所选数据导出为csv
    :param modeladmin:
    :param request: 用户发起的请求
    :param queryset: 用户选择的结果列表
    :return:
    '''
    response = HttpResponse(content_type='text/csv')
    response.write(codecs.BOM_UTF8)  # 防止csv导出乱码
    field_list = exportable_fields
    response['Content-Disposition'] = 'attachment;filename=recruitment-candidates-list-%s.csv' % (
        datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
    )

    # 写入表头
    writer = csv.writer(response)
    writer.writerow(
        [queryset.model._meta.get_field(f).verbose_name.title() for f in field_list]
    )
    for obj in queryset:
        # 单行记录（各个字段的值），写入到csv文件
        csv_line_values = []
        for field in field_list:
            field_object = queryset.model._meta.get_field(field)
            field_value = field_object.value_from_object(obj)
            csv_line_values.append(field_value)
        writer.writerow(csv_line_values)

    logger.info("%s exported %s candidate records" % (request.user, len(queryset)))

    return response


export_model_as_csv.short_description = u'导出为csv文件'
# 对应model定义的权限
export_model_as_csv.allowed_permissions = ('export',)


class CandidateAdmin(admin.ModelAdmin):
    exclude = ('creator', 'created_date', 'modified_date')
    list_display = (
        'username', 'city', 'bachelor_school', 'first_score', 'first_result', 'first_interviewer_user', 'second_score',
        'second_result', 'second_interviewer_user', 'hr_score', 'hr_result', 'hr_interviewer_user', 'last_editor',
    )

    # 表数据操作定义
    actions = [export_model_as_csv, notify_interviewer]

    def has_export_permission(self, request):
        '''
        export权限判断
        :param request:
        :return:
        '''
        opts = self.opts
        return request.user.has_perm('%s.%s' % (opts.app_label, "export"))

    # 筛选条件
    list_filter = (
        'city', 'first_result', 'second_result', 'hr_result', 'first_interviewer_user', 'second_interviewer_user',
        'hr_interviewer_user')

    # 查询字段
    search_fields = ('username', 'phone', 'email', 'bachelor_school')

    # 默认排序
    ordering = ('hr_result', 'second_result', 'first_result')

    def get_group_names(self, user):
        '''
        获取用户所属组
        :param user:
        :return:
        '''
        group_nams = []
        for g in user.groups.all():
            group_nams.append(g.name)
        return group_nams

    def get_queryset(self, request):
        '''
        只显示所属面试官的应聘者
        :param request:
        :return:
        '''
        qs = super(CandidateAdmin, self).get_queryset(request)

        group_names = self.get_group_names(request.user)
        if request.user.is_superuser or 'hr' in group_names:
            return qs
        return Candidate.objects.filter(
            Q(first_interviewer_user=request.user) or Q(second_interviewer_user=request.user))

    default_list_editable = ('first_interviewer_user', 'second_interviewer_user',)

    def get_list_editable(self, request):
        '''
        面试者列表获取可编辑字段
        :param request:
        :return:
        '''
        group_names = self.get_group_names(request.user)
        # print(group_names)
        if request.user.is_superuser or 'hr' in group_names:
            return self.default_list_editable
        return ()

    def get_changelist_instance(self, request):
        '''
        重载父类方法
        :param request:
        :return:
        '''
        self.list_editable = self.get_list_editable(request)
        return super(CandidateAdmin, self).get_changelist_instance(request)

    # readonly_fields = ('last_editor',)

    def get_readonly_fields(self, request, obj=None):
        '''
        面试者详情页只读字段设置
        :param request:
        :param obj:
        :return:
        '''
        group_names = self.get_group_names(request.user)  # 用户所属群组

        if 'interviewer' in group_names:
            logger.info("interviewer is in user's group for %s" % request.user.username)
            return ('last_editor', 'first_interviewer_user', 'second_interviewer_user',)
        return ('last_editor',)

    def get_fieldsets(self, request, obj=None):
        group_names = self.get_group_names(request.user)

        if 'interviewer' in group_names and obj.first_interviewer_user == request.user:
            return CF.default_fieldsets_first
        if 'interviewer' in group_names and obj.second_interviewer_user == request.user:
            return CF.default_fieldsets_second
        return CF.default_fieldsets

    def save_model(self, request, obj, form, change):
        obj.last_editor = request.user.username
        if not obj.creator:
            obj.creator = request.user.username
        obj.modified_date = datetime.now()
        obj.save()


admin.site.register(Candidate, CandidateAdmin)
