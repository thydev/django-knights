from __future__ import unicode_literals
from django.db import models

class KnightManager(models.Manager):
    def create_validator(self, postData):
        errors = {}
        if len(postData['name']) < 2:
            errors["knight"] = "Kight name should be more than 2 characters"
        elif Knight.objects.filter(name=postData['name']).count() > 0:
            errors['knight'] = "This knight name {} already exists".format(postData['name'])

        return errors

    # def save(self, postData):
    #     self.name = postData['name']
    #     self.title = postData['title']
    #     self.save()
    #     return self

class MatchManager(models.Manager):
    def create_validator(self, postData):
        errors = {}
        if not postData.get('player1'):
            errors["player1"] = "Please select player 1"

        if not postData.get('player2'):
            errors["player2"] = "Please select player 2"

        if postData.get('player1') and postData.get('player2'):
            if postData['player1']  == postData['player2']:
                errors["player"] = "Player 1 and Player 2 should not be the same"

        return errors

class Knight(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = KnightManager()

    def __repr__(self):
        return "<Knight: {}>".format(self.name)

class Match(models.Model):

    loser = models.ForeignKey(Knight, on_delete=models.CASCADE, related_name="loser_matches")
    winner = models.ForeignKey(Knight, on_delete=models.CASCADE, related_name="winner_matches")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MatchManager()

    def __repr__(self):
        return "<{} vs. {}>".format(self.winner.name, self.player2.name, self.winner.name)