from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from utils.drf_utils.custom_json_response import JsonResponse, unite_response_format_schema
from system.serializers.organization import OrganizationCreateUpdateSerializer, OrganizationRetrieveSerializer
from system.models import Organization


@extend_schema(tags=['组织架构管理'])
class OrganizationViewSet(ModelViewSet):
    queryset = Organization.objects.all().order_by('-id')

    def get_serializer_class(self):
        if self.action == 'update' or self.action == 'partial_update' or self.action == 'create':
            return OrganizationCreateUpdateSerializer
        elif self.action == 'list' or self.action == 'retrieve' or self.action == 'destroy':
            return OrganizationRetrieveSerializer

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
        res = super().list(request, *args, **kwargs)
        return JsonResponse(data=res.data, msg='success', code=20000)

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
