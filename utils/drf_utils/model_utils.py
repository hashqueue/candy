def get_obj_child_ids(parent: int, models_class_name, ids: set):
    """
    获取models模型的子id集合
    :param parent: models模型类ID
    :param models_class_name: models模型对象类
    :param ids: 默认为空集合
    """
    objs = models_class_name.objects.filter(parent=parent)
    for obj in objs:
        ids.add(obj.id)
        get_obj_child_ids(obj.id, models_class_name, ids)


def get_user_permissions(user_obj):
    """
    获取用户对象所拥有的所有权限
    @param user_obj:
    @return:
    """
    role_list = user_obj.roles.all()
    request_api_permissions = list()
    for role in role_list:
        permission_list = role.permissions.all()
        for permission in permission_list:
            # 去重
            permission_data = {
                'name': permission.name,
                'is_menu': permission.is_menu,
                'method': permission.method,
                'url_path': permission.url_path,
                'icon': permission.icon,
            }
            if permission_data not in request_api_permissions:
                request_api_permissions.append(permission_data)
    return request_api_permissions
