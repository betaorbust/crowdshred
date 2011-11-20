import random
import simplejson as json

from django.http import HttpResponse

from project.apps.shredder.models import Pair


def pair_api(request):

    pair = random.choice(Pair.objects.all())
    images = []
    for image in [pair.piece1, pair.piece2]:
        d = {}
        d['id'] = image.hash_id
        d['src'] = "./static/images/%s.png" % image.hash_id
        images.append(d)
    content = json.dumps({"images": images})
    return HttpResponse(content, mimetype='application/json')
