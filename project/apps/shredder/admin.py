from django.contrib import admin
from project.apps.shredder.models import Document, Piece, Pair, Vote


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Document, DocumentAdmin)


class PieceAdmin(admin.ModelAdmin):
    list_display = ('doc', 'hash_id')

admin.site.register(Piece, PieceAdmin)


class PairAdmin(admin.ModelAdmin):
    list_display = ('piece1', 'piece2',
                    'votes_made', 'votes_required', 'points')

admin.site.register(Pair, PairAdmin)


class VoteAdmin(admin.ModelAdmin):
    list_display = ('pair', 'created', 'state')

admin.site.register(Vote, VoteAdmin)
