"""recruitment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
   https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
   1. Add an import:  from my_app import views
   2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
   1. Add an import:  from other_app.views import Home
   2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
   1. Import the include() function: from django.urls import include, path
   2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.utils.translation import gettext as _  # 多语言翻译

urlpatterns = [
    url(r'^', include('jobs.urls')),
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),

    url(r'^accounts/', include('registration.backends.simple.urls')),
]

admin.site.site_header = _('银河系科技招聘系统')
