from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView

from utils.drf_utils.custom_json_response import JsonResponse
from .serializers import UserRegisterSerializer, MyTokenObtainPairSerializer


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

    @extend_schema(
        responses={
            201: {
                "type": "object",
                "properties": {
                    "code": {"type": "integer", 'description': '业务状态码'},
                    "message": {"type": "string", 'description': '业务提示消息'},
                    "data": {"type": "object",
                             'description': '数据',
                             "properties": {
                                 "username": {"type": "string", 'description': '用户名'},
                                 "email": {"type": "string", 'description': '邮箱'}
                             }}
                },
                "example": {
                    "code": 20000,
                    "message": "注册成功",
                    "data": {
                        "username": "string",
                        "email": "user@example.com"
                    }
                },
            },
        },
    )
    def post(self, request, *args, **kwargs):
        """
        用户注册
        * `所有字段`都是`必填项`
        """
        return super().post(request, *args, **kwargs)
