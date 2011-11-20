import math
import random

from django.db.models import Max


def get_random_item(model, max_id=None):
    """
    Return a random item from the database
    """
    if max_id is None:
        max_id = model.objects.aggregate(Max('id')).values()[0]
    min_id = math.ceil(max_id * random.random())
    return model.objects.filter(id__gte=min_id)[0]
