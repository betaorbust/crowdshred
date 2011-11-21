import itertools

from django.contrib.auth.models import User
from django.db import models


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
    votes_required = models.PositiveIntegerField(default=3, help_text="Number of votes for confidence")
    points = models.PositiveIntegerField(default=0, help_text="Number of points this pairing is worth")

    def __unicode__(self):
        return '%s %s' % (self.piece1.hash_id, self.piece2.hash_id)

    def confidence(self):
        """
        A simple way to determine percentage confidence in a pairing
        """
        return float(self.votes_made) / float(self.votes_required)

    def save(self, *args, **kwargs):
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
    user = models.ForeignKey(User)
    pair = models.ForeignKey(Pair)
    created = models.DateTimeField(auto_now_add=True)
    state = models.PositiveIntegerField(choices=STATE_CHOICES, help_text="User confidence in pair")

    def __unicode__(self):
        return '%s %s' % (self.piece1.hash_id, self.piece2.hash_id)
