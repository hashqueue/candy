from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from utils.drf_utils.custom_json_response import JsonResponse, unite_response_format_schema
from system.serializers.users import UserRegisterSerializer, MyTokenObtainPairSerializer, UserCreateUpdateSerializer, \
    UserRetrieveSerializer, UserListDestroySerializer, UserResetPasswordSerializer
from system.models import User


# Create your views here.
@extend_schema(tags=['用户登录'])
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    @extend_schema(
        responses={
            200: {
                "type": "object",
                "properties": {
                    "code": {"type": "integer", 'description': '业务状态码'},
                    "message": {"type": "string", 'description': '业务提示消息'},
                    "data": {"type": "object",
                             'description': '数据',
                             "properties": {
                                 "refresh": {"type": "string", 'description': 'refresh JWT token'},
                                 "access": {"type": "string", 'description': 'JWT token'},
                                 "user_id": {"type": "integer", 'description': '用户ID'}
                             }}
                },
                "example": {
                    "code": 20000,
                    "message": "登录成功",
                    "data": {
                        "refresh": "eyJ0xxx.eyJ0xxx.lw-sX",
                        "access": "eyJ0xxx.eyJ0.xxx.3bAec",
                        "user_id": 1
                    }
                },
            },
        },
    )
    def post(self, request, *args, **kwargs):
        """
        用户登录
        * `username`字段可填写用户的`username`或`email`, 只要校验成功就可以`登录成功`
        * 响应体中`access`就是JWT的`token`值, 用于访问其他接口时做用户认证使用
        """
        return super().post(request, *args, **kwargs)


@extend_schema(tags=['用户注册'])
class UserRegisterView(CreateAPIView):
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        """
        用户注册
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return JsonResponse(data=serializer.data, msg='注册成功', code=20000, status=status.HTTP_201_CREATED,
                            headers=headers)

    @extend_schema(responses=unite_response_format_schema('user-register', UserRegisterSerializer))
    def post(self, request, *args, **kwargs):
        """
        用户注册
        * `所有字段`都是`必填项`
        """
        return super().post(request, *args, **kwargs)


@extend_schema(tags=['用户管理'])
class UserViewSet(ModelViewSet):
    queryset = User.objects.all().order_by('-id')

    def get_serializer_class(self):
        if self.action == 'update' or self.action == 'partial_update' or self.action == 'create':
            return UserCreateUpdateSerializer
        elif self.action == 'destroy' or self.action == 'list':
            return UserListDestroySerializer
        elif self.action == 'retrieve':
            return UserRetrieveSerializer
        elif self.action == 'reset_password':
            return UserResetPasswordSerializer

    @extend_schema(responses=unite_response_format_schema('create-user', UserCreateUpdateSerializer))
    def create(self, request, *args, **kwargs):
        """
        create user
        """
        res = super().create(request, *args, **kwargs)
        return JsonResponse(data=res.data, msg='success', code=20000, status=status.HTTP_201_CREATED,
                            headers=res.headers)

    def list(self, request, *args, **kwargs):
        """
        select user list
        """
        res = super().list(request, *args, **kwargs)
        return JsonResponse(data=res.data, msg='success', code=20000, status=status.HTTP_200_OK)

    @extend_schema(responses=unite_response_format_schema('select-user-detail', UserRetrieveSerializer))
    def retrieve(self, request, *args, **kwargs):
        """
        select user detail
        """
        res = super().retrieve(request, *args, **kwargs)
        return JsonResponse(data=res.data, msg='success', code=20000, status=status.HTTP_200_OK)

    @extend_schema(
        responses=unite_response_format_schema('update-user-detail', UserCreateUpdateSerializer))
    def update(self, request, *args, **kwargs):
        """
        update user detail
        """
        res = super().update(request, *args, **kwargs)
        return JsonResponse(data=res.data, msg='success', code=20000)

    @extend_schema(
        responses=unite_response_format_schema('partial-update-user-detail',
                                               UserCreateUpdateSerializer))
    def partial_update(self, request, *args, **kwargs):
        """
        partial update user detail
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        delete user
        """
        return super().destroy(request, *args, **kwargs)

    @extend_schema(responses=unite_response_format_schema('reset-password-detail', UserResetPasswordSerializer))
    @action(methods=['patch'], detail=True)
    def reset_password(self, request, pk=None, version=None):
        """
        重置密码
        """
        user_obj: User = self.get_object()
        serializer = UserResetPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user_obj.set_password(request.data.get('password'))
            user_obj.save()
            return JsonResponse(data=None, msg='success', code=20000)
