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
