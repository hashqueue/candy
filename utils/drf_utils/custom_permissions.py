# -*- coding: utf-8 -*-
# @File    : custom_permissions.py
# @Software: PyCharm
# @Description:
import re
from functools import reduce
from rest_framework import permissions
from candy.settings import WHITE_URL_LIST


class RbacPermission(permissions.BasePermission):
    """
    自定义权限类
    """

    def has_permission(self, request, view):
        request_url = request.path
        request_method = request.method
        # 演示环境禁止删除数据
        # if request.method == 'DELETE':
        #     return False
        # URL白名单 如果请求url在白名单, 放行
        for safe_url in WHITE_URL_LIST:
            if re.match(f'^{safe_url}$', request_url):
                return True
        # admin权限直接放行(admin默认拥有所有权限, 系统初始化数据时配置admin拥有全部权限)
        # role_name_list = request.user.roles.values_list('name', flat=True)
        # if 'admin' in role_name_list:
        #     return True
        # RBAC权限(API接口)验证
        get_user_permissions(request.user)


    # def has_object_permission(self, request, view, obj):
    #     """
    #     判断对象的权限
    #     @param request:
    #     @param view:
    #     @param obj:
    #     @return:
    #     """
    #     get_user_permissions(request.user)


def get_user_permissions(user_obj):
    """

    @param user_obj:
    @return:
    """
    role_list = user_obj.roles.all()
    request_api_permissions = list()
    for role in role_list:
        permission_list = role.permissions.all()
        for permission in permission_list:
            if permission.is_menu is False:
                # 去重
                if {'method': permission.method, 'url_path': permission.url_path} not in request_api_permissions:
                    request_api_permissions.append({'method': permission.method, 'url_path': permission.url_path})
        print(permission_list)
    print(role_list)
    print(request_api_permissions)
    return role_list

