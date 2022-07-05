# -*- coding: utf-8 -*-
# @Time    : 2021/3/22 下午1:49
# @Author  : anonymous
# @File    : urls.py
# @Software: PyCharm
# @Description:
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView
from .views import MyTokenObtainPairView, UserRegisterView, OrganizationViewSet

router = routers.DefaultRouter()
# 如果视图类中没有指定queryset，则需要手动指定basename
router.register(prefix=r'organizations', viewset=OrganizationViewSet, basename='organization')
urlpatterns = [
    path('user/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/register/', UserRegisterView.as_view(), name='user_register'),
    path('', include(router.urls)),
]
