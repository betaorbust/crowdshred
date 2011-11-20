import simplejson as json

from django.http import HttpResponse

from project.apps.shredder.models import Pair


def pair_api(request):

    pair = Pair.objects.get(id=1)
    images = []
    for image in [pair.piece1, pair.piece2]:
        d = {}
        d['id'] = image.hash_id
        d['src'] = "./static/images/%s.png" % image.hash_id
        images.append(d)
    content = {"images": images}
    content = json.dumps(content)
    return HttpResponse(content, mimetype='application/json')
