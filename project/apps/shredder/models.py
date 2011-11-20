from django.db import models


class Document(models.Model):
    """
    Each document is comprised of many pieces
    """
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    def __unicode__(self):
        return self.name


class Piece(models.Model):
    """
    Each piece is a unique part of a document
    """
    doc = models.ForeignKey(Document)
    hash_id = models.CharField(max_length=255)

    def __unicode__(self):
        return u'%s %s' % (self.doc, self.hash_id)


class Pair(models.Model):
    """
    A pair is a set of matched pieces
    """
    piece1 = models.ForeignKey(Piece)
    piece2 = models.ForeignKey(Piece)
    votes_made = models.PositiveIntegerField(default=0)
    votes_required = models.PositiveIntegerField(default=3)
    points = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return '%s %s' % (self.piece1.hash_id, self.piece2.hash_id)

    def confidence(self):
        return float(self.votes_made) / float(self.votes_required)


class Vote(models.Model):
    """
    Any vote made by a user in the system
    """
    STATE_CHOICES = (
        (1, 'Perfect'),
        (2, 'Maybe'),
        (3, 'No Match'),
        (4, 'Broken'),
    )
    piece1 = models.ForeignKey(Piece)
    piece2 = models.ForeignKey(Piece)
    # user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    state = models.PositiveIntegerField(choices=STATE_CHOICES)

    def __unicode__(self):
        return '%s %s' % (self.piece1.hash_id, self.piece2.hash_id)
