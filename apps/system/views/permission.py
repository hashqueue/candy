from drf_spectacular.utils import extend_schema
from rest_framework import status, serializers
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from utils.drf_utils.custom_json_response import JsonResponse, unite_response_format_schema
from system.serializers.permissions import PermissionCreateUpdateSerializer, PermissionRetrieveSerializer, \
    GetPermissionsTreeWithRoleIdsSerializer, PermissionTreeSerializer
from system.models import Permission, Role


@extend_schema(tags=['权限管理'])
class PermissionViewSet(ModelViewSet):
    queryset = Permission.objects.all().order_by('-id')

    def get_serializer_class(self):
        if self.action == 'update' or self.action == 'partial_update' or self.action == 'create':
            return PermissionCreateUpdateSerializer
        elif self.action == 'retrieve' or self.action == 'destroy':
            return PermissionRetrieveSerializer
        elif self.action == 'list':
            return PermissionTreeSerializer
        elif self.action == 'get_permissions_whit_roles':
            return GetPermissionsTreeWithRoleIdsSerializer

    @extend_schema(responses=unite_response_format_schema('create-permission', PermissionCreateUpdateSerializer))
    def create(self, request, *args, **kwargs):
        """
        create permission
        """
        res = super().create(request, *args, **kwargs)
        return JsonResponse(data=res.data, msg='success', code=20000, status=status.HTTP_201_CREATED,
                            headers=res.headers)

    def list(self, request, *args, **kwargs):
        """
        select permission list
        """
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        tree_dict = {}
        tree_data = []
        for item in serializer.data:
            tree_dict[item['id']] = item
        try:
            for item_id in tree_dict:
                if tree_dict.get(item_id).get('parent'):
                    pid = tree_dict.get(item_id).get('parent')
                    # 父权限的完整数据
                    parent_data = tree_dict.get(pid)
                    # 如果有children就直接追加数据，没有则添加children并设置默认值为[]，然后追加数据
                    parent_data.setdefault('children', []).append(tree_dict.get(item_id))
                else:
                    # item没有parent, 放在最顶层
                    tree_data.append(tree_dict.get(item_id))
            data = {
                'count': len(tree_data),
                'next': None,
                'previous': None,
                'results': tree_data,
                'total_pages': None,
                'current_page': None,
            }

            return JsonResponse(data=data, msg='success', code=20000)
        except Exception:
            # 生成tree型数据报错时，按照非tree格式来返回数据
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                res = self.get_paginated_response(serializer.data)
                return JsonResponse(data=res.data, msg='success', code=20000)
            return JsonResponse(data=serializer.data, msg='success', code=20000)

    @extend_schema(responses=unite_response_format_schema('select-permission-detail', PermissionRetrieveSerializer))
    def retrieve(self, request, *args, **kwargs):
        """
        select permission detail
        """
        res = super().retrieve(request, *args, **kwargs)
        return JsonResponse(data=res.data, msg='success', code=20000, status=status.HTTP_200_OK)

    @extend_schema(
        responses=unite_response_format_schema('update-permission-detail', PermissionCreateUpdateSerializer))
    def update(self, request, *args, **kwargs):
        """
        update permission detail
        """
        res = super().update(request, *args, **kwargs)
        return JsonResponse(data=res.data, msg='success', code=20000)

    @extend_schema(
        responses=unite_response_format_schema('partial-update-permission-detail',
                                               PermissionCreateUpdateSerializer))
    def partial_update(self, request, *args, **kwargs):
        """
        partial update permission detail
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        delete permission
        """
        return super().destroy(request, *args, **kwargs)

    @extend_schema(
        responses=unite_response_format_schema('get-permissions-whit-roles', GetPermissionsTreeWithRoleIdsSerializer))
    @action(methods=['post'], detail=False, url_path='get-roles-permissions')
    def get_permissions_whit_roles(self, request, pk=None, version=None):
        """
        通过角色列表获取权限树列表
        """
        serializer = GetPermissionsTreeWithRoleIdsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            roles_permissions = []
            role_ids = serializer.data.get('role_ids')
            for role_id in role_ids:
                role_objs = Role.objects.filter(id=role_id).all()
                if len(role_objs) == 0:
                    raise serializers.ValidationError(f'id为{role_id}的角色不存在.')
                roles_permissions.extend(role_objs[0].permissions.all())
            roles_permissions = list(set(roles_permissions))
            # 获取权限list
            permissions_serializer = PermissionTreeSerializer(roles_permissions, many=True)
            tree_dict = {}
            tree_data = []
            for item in permissions_serializer.data:
                tree_dict[item['id']] = item
            for item_id in tree_dict:
                if tree_dict.get(item_id).get('parent'):
                    pid = tree_dict.get(item_id).get('parent')
                    # 父权限的完整数据
                    parent_data = tree_dict.get(pid)
                    # 如果有children就直接追加数据，没有则添加children并设置默认值为[]，然后追加数据
                    parent_data.setdefault('children', []).append(tree_dict.get(item_id))
                else:
                    # item没有parent, 放在最顶层
                    tree_data.append(tree_dict.get(item_id))
            return JsonResponse(data={'role_ids': role_ids, 'permissions': tree_data}, msg='success', code=20000)
