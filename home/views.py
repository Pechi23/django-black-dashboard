from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from home.models import *
from .utils import init,read_futures
from datetime import datetime 


# Pages -- Dashboard
def index(request):
    #init()
    context = {
    'parent': 'pages',
    'segment': 'dashboard',
    "stats" : Stats.objects.all().count(),
    "players" : Player.objects.all().count(),
    "teams" : Team.objects.all().count(),
    "members" : Member.objects.all().count(),
    "games" : Game.objects.filter(played=True).count()
    }
    
    return render(request, 'pages/dashboard.html', context)

@login_required(login_url='/accounts/auth-signin')
def tables(request):
    #init()
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
def futures(request):
    #read_futures()
    
    all_matches = Game.objects.filter(date__gte=now().date()).order_by('date')
    paginator = Paginator(all_matches, 10)
    
    page = request.GET.get('page', 1)

    try:
        matches = paginator.page(page)
    except:
        matches = paginator.page(1)
    
    context = {
    'parent': 'pages',
    'segment': 'futures',
    'matches': matches,
    'page_obj': matches,
  }
    return render(request, 'pages/futures.html', context)

