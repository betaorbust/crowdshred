import simplejson as json

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from django.http import HttpResponse

from project.apps.shredder.models import Pair, Vote
from project.apps.shredder.utils import get_random_item


def json_response(content, code=200):
    resp = HttpResponse(json.dumps(content), mimetype='application/json')
    resp.code = code
    return resp


def json_response_success(message, code=200):
    content = {
        'message': message,
        'code': code,
        }
    return json_response(content, code=code)


def json_response_error(message, code=404):
    content = {
        'message': 'Error: %s' % message,
        'code': code,
        }
    return json_response(content, code=code)


def pair_api(request):

    pair = get_random_item(Pair)
    images = []
    for image in [pair.piece1, pair.piece2]:
        d = {}
        d['id'] = image.hash_id
        d['src'] = "%simages/%s.png" % (settings.STATIC_URL, image.hash_id)
        images.append(d)
    content = {
            'images': images,
            'pair': pair.hash_id,
        }
    return json_response(content)


def vote_api(request):

    if request.GET:
        state = request.GET['state']
        try:
            pair = Pair.objects.get(hash_id=request.GET['hash_id'])
        except ObjectDoesNotExist:
            return json_response_error('Object does not exist', code=404)
        vote = Vote(user=request.user,
                    pair=pair,
                    state=state)
        vote.save()

        pair.votes_made = F('votes_made') + 1
        if state == '1':
            pair.votes_perfect = F('votes_perfect') + 1
        elif state == '2':
            pair.votes_maybe = F('votes_maybe') + 1
        elif state == '3':
            pair.votes_no_match = F('votes_no_match') + 1
        elif state == '4':
            pair.votes_broken = F('votes_broken') + 1
        pair.save()

        # @TODO: deltas and rotation

        return json_response_success('Accepted', code=202)
    return json_response_error('Forbidden', code=403)
