# -*- coding: utf-8 -*-
# @File    : custom_permissions.py
# @Software: PyCharm
# @Description:
import re
from rest_framework import permissions
from candy.settings import WHITE_URL_LIST, API_PREFIX
from utils.drf_utils.model_utils import get_user_permissions


class RbacPermission(permissions.BasePermission):
    """
    自定义权限类
    """

    def has_permission(self, request, view):
        request_url_path = request.path
        request_method = request.method
        """演示环境禁止删除数据"""
        # if request.method == 'DELETE':
        #     return False
        """URL白名单 如果请求url在白名单, 放行"""
        for safe_url in WHITE_URL_LIST:
            if re.match(f'^{safe_url}$', request_url_path):
                return True
        """admin权限直接放行(admin默认拥有所有权限, 系统初始化数据时配置admin拥有全部权限)"""
        role_name_list = request.user.roles.values_list('name', flat=True)
        if 'admin' in role_name_list:
            return True
        """RBAC权限验证"""
        # API权限验证
        user_permissions = get_user_permissions(request.user)
        for user_permission in user_permissions:
            if user_permission.get('method') == request_method and re.match(
                    f"^{(API_PREFIX + user_permission.get('url_path'))}$",
                    request_url_path):
                return True

    # def has_object_permission(self, request, view, obj):
    #     """
    #     判断对象的权限
    #     @param request:
    #     @param view:
    #     @param obj:
    #     @return:
    #     """
    #     pass
