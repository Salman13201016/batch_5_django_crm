"""
URL configuration for crm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
from django.urls import path, include
from . import views as v
urlpatterns = [
    path('category/',v.category, name='course_category'),
    path('content/',v.course_content, name='course_content'),
    path('category/edit/<int:cat_id>',v.course_edit, name='category_edit'),
    path('category/delete/<int:cat_id>',v.course_cat_delete, name='course_cat_delete'),
    ]
