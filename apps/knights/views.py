from django.shortcuts import render, redirect
from models import Knight, Match
from random import randint
from django.contrib import messages
from django.db.models import Q

#Home page
def index(request):
    context = {
        'players': Knight.objects.all(),
        'matches': Match.objects.all(),
    }
    return render(request, 'knights/index.html', context)

def create(request):
    print "creating"
    if request.method != 'POST':
        return redirect('/')

    # Create a knight
    # Validation for creating new object
    errors = Knight.objects.create_validator(request.POST)
    if len(errors) > 0:
        for tag, error in errors.iteritems():
            # messages.error(request, error, extra_tags=tag)
            messages.error(request, error, extra_tags="createknight")
        return redirect('/')
    # print Knight.save(request.POST) # Not working ===> Research moere
    Knight.objects.create(name = request.POST['name'], title = request.POST['title'])
    return redirect('/')    

def matching(request):
    print "m matching"
    if request.method != 'POST':
        return redirect('/')

    # Create a match
    print request.POST.get('player1'), "<=== player1"
    print request.POST.get('player2'), "<=== player2"
    # fat = True
    # fitness = ("skinny", "fat")[fat]
    # print "Ali is", fitness
    # # Output: Ali is fat

    # Validation for creating new object
    errors = Match.objects.create_validator(request.POST)
    if len(errors) > 0:
        for tag, error in errors.iteritems():
            # messages.error(request, error, extra_tags=tag)
            messages.error(request, error, extra_tags="creatematching")
        return redirect('/')
    player1 = Knight.objects.get(id = request.POST.get('player1'))
    player2 = Knight.objects.get(id = request.POST.get('player2'))

    winner = (player1, player2)[randint(1,2) == 1]
    match = Match(player1 = player1, player2 = player2, winner = winner)
    match.save()
    
    return redirect('/')

def showknight(request, id):
    knight = Knight.objects.get(id=id)
    context = {
        'knight': knight,
        'losses': knight.count_losses(),
        'matches': Match.objects.filter(Q(player1=knight) | Q(player2=knight)).order_by('-created_at')
    }
    return render(request, 'knights/showknight.html', context)

def count_losses(kinghtself):
    wins = kinghtself.winner_matches.count()
    match1 = kinghtself.player1_matches.count()
    match2 = kinghtself.player2_matches.count()
    losses = match1 + match2 - wins
    
    return losses