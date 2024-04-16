from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from home.models import *
from .utils import init,read_futures


# Pages -- Dashboard
def index(request):
    init()
    context = {
    'parent': 'pages',
    'segment': 'dashboard',
    "stats" : Stats.objects.all().count(),
    "players" : Player.objects.all().count(),
    "teams" : Team.objects.all().count(),
    "members" : Member.objects.all().count(),
    "games" : Game.objects.filter(date__lte=now().date()).count()
    }
    
    return render(request, 'pages/dashboard.html', context)

@login_required(login_url='/accounts/auth-signin')
def tables(request):
    init()
    teams_with_total_stats = Team.objects.annotate(
        total_stats=Sum('member__player__stats__PPI')
    )

    # Order the teams by their total stats in descending order
    ordered_teams = teams_with_total_stats.order_by('-total_stats')

    context = {
    'parent': 'pages',
    'segment': 'tables',
    'teams': ordered_teams
  }
    return render(request, 'pages/tables.html', context)
  
@login_required(login_url='/accounts/auth-signin')
def tables2(request):
    read_futures()
    
    context = {
    'parent': 'pages',
    'segment': 'tables',
    'matches': Game.objects.filter(date__gte=now().date()),
  }
    return render(request, 'pages/tables2.html', context)

