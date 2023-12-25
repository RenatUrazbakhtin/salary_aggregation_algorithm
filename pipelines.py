
# Типы группировок для пайплайна
group_types = {
    "hour": "%Y-%m-%dT%H",
    "day": "%Y-%m-%d",
    "week": "",
    "month": "%Y-%m"
}

def get_pipeline(time_fr, time_to, group_type):
    """
    Получает пайплайн сортировки данных из бд
    :param time_fr: дата начала сортировки
    :param time_to: дата конца сортировки
    :param group_type: группировка данных
    :return: пайплайн агрегации данных
    """

    if group_type not in group_types.keys():
        raise ValueError('Invalid group type')
    else:
        pipeline = [
            {
                "$match": {
                    "dt": {'$gte': time_fr, "$lte": time_to}
                }
            },
            {
                "$group":
                    {
                        "_id": {"$dateToString": {"date": "$dt", "format": group_types[group_type]}},
                        "sum_val": {"$sum": "$value"}
                    }
            },
            {
                "$sort": {"_id": 1}
            },
        ]
    return pipeline
