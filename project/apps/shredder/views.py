import simplejson as json

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect


from project.apps.shredder.forms import VoteForm
from project.apps.shredder.models import Pair
from project.apps.shredder.utils import get_random_item

from social_auth.models import SocialUser, IdentityProvider

def json_response(content, code=200):
    user = request.session.get('user',None)
    if not user:
        json_response_error('User is not authenticated! Log in to play!', code=401)
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
    user = request.session.get('user',None)
    if not user:
        json_response_error('User is not authenticated! Log in to play!', code=401)
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
    user = request.session.get('user',None)
    if not user:
        json_response_error('User is not authenticated! Log in to play!', code=401)
    if request.GET:
        form = VoteForm(request.GET)
        if form.is_valid():
            vote = form.save(commit=False)
            try:
                pair = Pair.objects.get(hash_id=request.GET['hash_id'])
            except ObjectDoesNotExist:
                return json_response_error('Object does not exist', code=404)
            vote.user = request.session.get('user',None)
            # vote.user = request.user
            vote.pair = pair
            vote.save()

            return json_response_success('Accepted', code=202)
        else:
            return json_response_success('Invalid Form', code=403)
    return json_response_error('Forbidden', code=403)

def game(request):
    user = request.session.get('user',None)
    if not user:
        return HttpResponseRedirect('/login')
    return render_to_response("shredder/game.html")