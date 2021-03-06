from django.contrib import admin
from .models import Country, Province, Area, City


class ReadOnlyAdmin(admin.ModelAdmin):
    '''只读站点，只能显示数据'''
    readonly_fields = []

    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]

    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + \
               [field.name for field in obj._meta.fields] + \
               [field.name for field in obj._meta.many_to_many]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


# @admin.register(Country)
# class CountryAdmin(ReadOnlyAdmin):
#     search_fields = ('chn_name', 'eng_name',)
#
#
# @admin.register(Province)
# class ProvinceAdmin(ReadOnlyAdmin):
#     search_fields = ('chn_name', 'eng_name',)
#
#
# @admin.register(City)
# class CityAdmin(ReadOnlyAdmin):
#     # 用于优化有大量关联数据的字段，比如一个人，可能会管理多个企业
#     autocomplete_fields = ['provinceid', 'countryid', ]  # 模糊查询输入信息相关的数据，对应城市和国家的search_fields
#
#     # 使用ReadOnlyAdmin中的list_display
#     # list_display = ('cityid', 'countryid', 'areaid', 'provinceid', 'chn_name', 'eng_name')
