def get_organization_child_ids(parent: int, models_class_name, ids: set):
    """
    获取models模型的子id集合
    :param parent: models模型类ID
    :param models_class_name: models模型对象类
    :param ids: 默认为空集合
    """
    organizations = models_class_name.objects.filter(parent=parent)
    for organization in organizations:
        ids.add(organization.id)
        get_organization_child_ids(organization.id, models_class_name, ids)
