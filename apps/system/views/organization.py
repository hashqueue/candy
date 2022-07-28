from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from utils.drf_utils.custom_json_response import JsonResponse, unite_response_format_schema
from system.serializers.organization import OrganizationCreateUpdateSerializer, OrganizationRetrieveSerializer, \
    OrganizationListSerializer
from system.models import Organization


@extend_schema(tags=['组织架构管理'])
class OrganizationViewSet(ModelViewSet):
    queryset = Organization.objects.all().order_by('-id')

    def get_serializer_class(self):
        if self.action == 'update' or self.action == 'partial_update' or self.action == 'create':
            return OrganizationCreateUpdateSerializer
        elif self.action == 'retrieve' or self.action == 'destroy':
            return OrganizationRetrieveSerializer
        elif self.action == 'list':
            return OrganizationListSerializer

    @extend_schema(responses=unite_response_format_schema('create-organization', OrganizationCreateUpdateSerializer))
    def create(self, request, *args, **kwargs):
        """
        create organization
        """
        res = super().create(request, *args, **kwargs)
        return JsonResponse(data=res.data, msg='success', code=20000, status=status.HTTP_201_CREATED,
                            headers=res.headers)

    def list(self, request, *args, **kwargs):
        """
        select organization list
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
                    # 父组织架构的完整数据
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

    @extend_schema(responses=unite_response_format_schema('select-organization-detail', OrganizationRetrieveSerializer))
    def retrieve(self, request, *args, **kwargs):
        """
        select organization detail
        """
        res = super().retrieve(request, *args, **kwargs)
        return JsonResponse(data=res.data, msg='success', code=20000, status=status.HTTP_200_OK)

    @extend_schema(
        responses=unite_response_format_schema('update-organization-detail', OrganizationCreateUpdateSerializer))
    def update(self, request, *args, **kwargs):
        """
        update organization detail
        """
        res = super().update(request, *args, **kwargs)
        return JsonResponse(data=res.data, msg='success', code=20000)

    @extend_schema(
        responses=unite_response_format_schema('partial-update-organization-detail',
                                               OrganizationCreateUpdateSerializer))
    def partial_update(self, request, *args, **kwargs):
        """
        partial update organization detail
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        delete organization
        """
        return super().destroy(request, *args, **kwargs)
