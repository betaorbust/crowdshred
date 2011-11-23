import itertools

from django.db import models
from django.db.models import F

from social_auth.models import SocialUser


class Document(models.Model):
    """
    Each document is comprised of many pieces
    """
    name = models.CharField(max_length=255, help_text="Name of the document")
    slug = models.SlugField()

    def __unicode__(self):
        return self.name

    def create_pairs(self):
        pieces = Piece.objects.filter(doc=self)
        pairs = itertools.combinations(pieces, 2)
        for pair in pairs:
            p = Pair(piece1=pair[0], piece2=pair[1])
            p.save()


class Piece(models.Model):
    """
    Each piece is a unique part of a document
    """
    doc = models.ForeignKey(Document)
    hash_id = models.CharField(max_length=255, help_text="A unique image id")

    def __unicode__(self):
        return u'%s %s' % (self.doc, self.hash_id)


class Pair(models.Model):
    """
    A pair is a set of matched pieces
    """
    hash_id = models.CharField(max_length=255)
    piece1 = models.ForeignKey(Piece, related_name="%(app_label)s_%(class)s_piece1")
    piece2 = models.ForeignKey(Piece, related_name="%(app_label)s_%(class)s_piece2")

    votes_made = models.PositiveIntegerField(default=0, help_text="Number of votes by users")
    votes_required = models.PositiveIntegerField(default=0, help_text="Number of votes by users")
    votes_perfect = models.PositiveIntegerField(default=0, help_text="Number of votes by users")
    votes_maybe = models.PositiveIntegerField(default=0, help_text="Number of votes by users")
    votes_no_match = models.PositiveIntegerField(default=0, help_text="Number of votes by users")
    votes_broken = models.PositiveIntegerField(default=0, help_text="Number of votes by users")

    confidence = models.FloatField(default=0.0, help_text="Confidence in pairing")
    points = models.PositiveIntegerField(default=0, help_text="Number of points this pairing is worth")

    def __unicode__(self):
        return '%s %s' % (self.piece1.hash_id, self.piece2.hash_id)

    def get_confidence(self):
        """
        A simple way to determine percentage confidence in a pairing
        """
        return self.votes_perfect - 2 * self.votes_no_match

    def save(self, *args, **kwargs):
        self.confidence = self.get_confidence()
        if not self.hash_id:
            import uuid
            self.hash_id = uuid.uuid4()
        super(Pair, self).save(*args, **kwargs)


class Vote(models.Model):
    """
    Any vote made by a user for a pair of pieces
    """
    STATE_CHOICES = (
        (1, 'Perfect'),
        (2, 'Maybe'),
        (3, 'No Match'),
        (4, 'Broken'),
    )
    user = models.ForeignKey(SocialUser)
    pair = models.ForeignKey(Pair)
    created = models.DateTimeField(auto_now_add=True)
    state = models.PositiveIntegerField(choices=STATE_CHOICES, help_text="User confidence in pair")

    dx = models.FloatField(blank=True, null=True)
    dy = models.FloatField(blank=True, null=True)
    rot0 = models.FloatField(blank=True, null=True)
    rot1 = models.FloatField(blank=True, null=True)

    def __unicode__(self):
        return '%s %s' % (self.user, self.pair)

    def save(self, *args, **kwargs):
        super(Vote, self).save(*args, **kwargs)
        self.pair.votes_made = F('votes_made') + 1
        if self.state == 1:
            self.pair.votes_perfect = F('votes_perfect') + 1
        elif self.state == 2:
            self.pair.votes_maybe = F('votes_maybe') + 1
        elif self.state == 3:
            self.pair.votes_no_match = F('votes_no_match') + 1
        elif self.state == 4:
            self.pair.votes_broken = F('votes_broken') + 1
        self.pair.save()
