from django import forms

from project.apps.shredder.models import Vote


class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        exclude = ('user', 'pair', 'created',)
