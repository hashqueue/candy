# -*- coding: utf-8 -*-
# @Time    : 2021/3/21 下午8:40
# @Author  : anonymous
# @File    : serializers.py
# @Software: PyCharm
# @Description:
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from utils.drf_utils.base_model_serializer import BaseModelSerializer

from .models import User, Organization


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    用户注册序列化器
    """
    password_confirm = serializers.CharField(min_length=8,
                                             max_length=128,
                                             label='确认密码',
                                             help_text='确认密码',
                                             write_only=True,
                                             required=True,
                                             allow_blank=False,
                                             error_messages={
                                                 'min_length': '密码长度不能小于8',
                                                 'max_length': '密码长度不能大于128', })

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'password_confirm')
        extra_kwargs = {
            'username': {
                'label': '用户名',
                'help_text': '用户名',
                'min_length': 1,
                'max_length': 150,
                'error_messages': {
                    'min_length': '用户名长度不能小于1',
                    'max_length': '用户名长度不能大于150',
                }
            },
            'password': {
                'label': '密码',
                'help_text': '密码',
                'write_only': True,
                'required': True,
                'min_length': 8,
                'max_length': 128,
                'error_messages': {
                    'min_length': '密码长度不能小于8',
                    'max_length': '密码长度不能大于128',
                }
            },
            'email': {
                'label': '邮箱',
                'help_text': '邮箱',
                'required': True,
                # 添加邮箱重复校验
                'validators': [UniqueValidator(queryset=User.objects.all(), message='此邮箱已被使用')],
            },
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('两次输入密码不一致')
        return attrs

    def create(self, validated_data):
        # 移除数据库模型类中不存在的字段password_confirm
        validated_data.pop('password_confirm')
        # 创建用户实例
        user_instance = User.objects.create_user(**validated_data)
        return user_instance


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        """
        重写validate方法, 添加user_id字段
        :param attrs:
        :return:
        """
        data = super().validate(attrs)
        data['user_id'] = self.user.id
        return {"code": 20000, "message": "登录成功", "data": data}


class OrganizationCreateUpdateSerializer(BaseModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'
        read_only_fields = ('id', 'create_time', 'update_time')


class OrganizationRetrieveSerializer(BaseModelSerializer):
    parent_organization_name = serializers.CharField(source='parent.name', required=False, read_only=True,
                                                     help_text='父组织架构名称')

    class Meta:
        model = Organization
        fields = '__all__'
