import simplejson as json

from django.http import HttpResponse

#from project.apps.shredder.models import Pair


def pair_api(request):

    content = {
                "images": [
                  {
                    "id": "42",
                    "src": "./static/images/test.png"
                  },
                  {
                    "id": "43",
                    "src": "./static/images/test.png"
                  }
                ]
            }
    content = json.dumps(content)
    return HttpResponse(content, mimetype='application/json')
