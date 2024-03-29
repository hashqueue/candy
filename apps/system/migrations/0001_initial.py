# Generated by Django 3.2.15 on 2022-11-12 14:28

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('title', models.CharField(help_text='权限名称', max_length=64, unique=True, verbose_name='权限名称')),
                ('is_menu', models.BooleanField(help_text='是否为菜单(true为菜单,false为接口)', verbose_name='是否为菜单(true为菜单,false为接口)')),
                ('method', models.CharField(blank=True, choices=[('POST', '增'), ('DELETE', '删'), ('PUT', '改'), ('PATCH', '局部改'), ('GET', '查')], default='', help_text='请求方法', max_length=8, verbose_name='请求方法')),
                ('url_path', models.CharField(blank=True, default='', help_text='请求路径', max_length=256, verbose_name='请求路径')),
                ('icon', models.CharField(blank=True, default='', help_text='图标', max_length=64, verbose_name='图标')),
                ('component', models.CharField(blank=True, default='', help_text='组件路径', max_length=256, verbose_name='组件路径')),
                ('path', models.CharField(blank=True, default='', help_text='路由path', max_length=256, verbose_name='路由path')),
                ('redirect', models.CharField(blank=True, default='', help_text='路由重定向path', max_length=256, verbose_name='路由重定向path')),
                ('is_visible', models.BooleanField(blank=True, help_text='是否显示(true为显示,false为隐藏)', null=True, verbose_name='是否显示(true为显示,false为隐藏)')),
                ('parent', models.ForeignKey(blank=True, help_text='父权限', null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.permission', verbose_name='父权限')),
            ],
            options={
                'verbose_name': '权限',
                'verbose_name_plural': '权限',
                'db_table': 'system_permission',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('name', models.CharField(help_text='角色名', max_length=32, unique=True, verbose_name='角色名')),
                ('desc', models.CharField(blank=True, default='', help_text='描述', max_length=64, verbose_name='描述')),
                ('permissions', models.ManyToManyField(blank=True, help_text='权限', to='system.Permission', verbose_name='权限')),
            ],
            options={
                'verbose_name': '角色',
                'verbose_name_plural': '角色',
                'db_table': 'system_role',
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('name', models.CharField(help_text='名称', max_length=128, verbose_name='名称')),
                ('type', models.CharField(choices=[('company', '公司'), ('department', '部门')], default='department', help_text='类型', max_length=20, verbose_name='类型')),
                ('parent', models.ForeignKey(blank=True, help_text='父组织架构', null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.organization', verbose_name='父组织架构')),
            ],
            options={
                'verbose_name': '组织架构',
                'verbose_name_plural': '组织架构',
                'db_table': 'system_organization',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('name', models.CharField(blank=True, default='', help_text='姓名', max_length=20, verbose_name='姓名')),
                ('birthday', models.DateField(blank=True, help_text='出生日期', null=True, verbose_name='出生日期')),
                ('gender', models.CharField(blank=True, choices=[('male', '男'), ('female', '女')], default='male', help_text='性别', max_length=10, verbose_name='性别')),
                ('mobile', models.CharField(blank=True, default='', help_text='手机号码', max_length=11, verbose_name='手机号码')),
                ('avatar', models.ImageField(blank=True, default='avatars/default.png', help_text='头像', upload_to='avatars/%Y/%m', verbose_name='头像')),
                ('position', models.CharField(blank=True, default='', help_text='职位', max_length=64, verbose_name='职位')),
                ('department', models.ForeignKey(blank=True, help_text='部门', null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.organization', verbose_name='部门')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('roles', models.ManyToManyField(blank=True, help_text='角色', to='system.Role', verbose_name='角色')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
                'db_table': 'system_user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
