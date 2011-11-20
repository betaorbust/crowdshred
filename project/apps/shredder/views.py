import random
import simplejson as json

from django.conf import settings
from django.http import HttpResponse

from project.apps.shredder.models import Pair


def pair_api(request):

    pair = random.choice(Pair.objects.all())
    images = []
    for image in [pair.piece1, pair.piece2]:
        d = {}
        d['id'] = image.hash_id
        d['src'] = "%simages/%s.png" % (settings.STATIC_URL, image.hash_id)
        images.append(d)
    content = json.dumps({"images": images})
    return HttpResponse(content, mimetype='application/json')
