from django.db.models import Sum
from .models import *
import os.path
from openpyxl import Workbook, load_workbook
from datetime import datetime
from django.utils.timezone import localdate

def init():
    if Stats.objects.all().count() > 0:
        return
      
    '''
    Player.objects.all().delete()
    Stats.objects.all().delete()
    Team.objects.all().delete()
    Member.objects.all().delete()
    Game.objects.all().delete()
    '''
    
    i = 1
    while True:
        file_path = 'matches/'+str(i)+'.xlsx'
        if os.path.exists(file_path) is False:
            break
        
        book = load_workbook(file_path)
        sheet = book.active
        
        index = 2
        while sheet['B'+str(index)].value is not None:
            s = Stats()
            
            player_name  = sheet['B'+str(index)].value
            try:
                s.player = Player.objects.get(name = player_name)
            except Player.DoesNotExist:
                newPlayer = Player(name = player_name)
                newPlayer.save()
                s.player = newPlayer 
            
            
            host = sheet['C1'].value
            guest = sheet['D1'].value
            
            if i % 2 == 0:
                s.team = guest
            else:
                s.team = host
                
            try:
                current_team = Team.objects.get(name = s.team)
            except Team.DoesNotExist:
                newTeam = Team(name = s.team)
                newTeam.save()
                current_team = newTeam 
                
            s.date = datetime.date(datetime.strptime( sheet['B1'].value, "%Y-%m-%d"))
            
            try:
                member = Member.objects.filter(player=s.player).get(team=current_team)
                if member.date_start > s.date:
                    member.date_start = s.date
                    member.save()
            except Member.DoesNotExist:
                newMember = Member(player=s.player, team=current_team, date_start = s.date)
                newMember.save()
            
            
            
            if i % 2 == 0:
                try:
                    match = Game.objects.filter(date=s.date).get(guest=current_team)
                except Game.DoesNotExist:
                    newMatch = Game(date = s.date)
                    newMatch.host = Team.objects.get(name = host)
                    newMatch.guest = Team.objects.get(name = guest)
                    newMatch.save()
            
            s.Pos   = sheet['C'+str(index)].value
            s.Rank  = sheet['D'+str(index)].value
            s.PPI   = sheet['E'+str(index)].value
            s.MP    = sheet['F'+str(index)].value
            s.G     = sheet['G'+str(index)].value
            s.SOnT  = sheet['H'+str(index)].value 
            s.SOffT = sheet['I'+str(index)].value
            s.BS    = sheet['J'+str(index)].value
            s.OG    = sheet['K'+str(index)].value
            s.A     = sheet['L'+str(index)].value
            s.P     = sheet['M'+str(index)].value
            s.C     = sheet['N'+str(index)].value
            s.Tk    = sheet['O'+str(index)].value
            s.INT   = sheet['P'+str(index)].value
            s.FW    = sheet['Q'+str(index)].value
            s.FC    = sheet['R'+str(index)].value
            s.O     = sheet['S'+str(index)].value
            s.YC    = sheet['T'+str(index)].value
            s.RC    = sheet['U'+str(index)].value
            s.GC    = sheet['V'+str(index)].value
            s.PW    = sheet['W'+str(index)].value
            s.SAV   = sheet['X'+str(index)].value
            s.Ca    = sheet['Y'+str(index)].value
            s.KS    = sheet['Z'+str(index)].value
            s.save()
            index += 1
        i += 1
        
def read_futures():
  if Game.objects.filter(date__gte=now().date()) is not None:
    return 
  
  
  file_path = 'future/future-matches.xlsx'
  if os.path.exists(file_path) is False:
    return
      
  book = load_workbook(file_path)
  sheet = book.active
  
  index = 1
  while sheet['B'+str(index)].value is not None:
    date  = sheet['B'+str(index)].value
    
    
    host = sheet['C'+str(index)].value
    guest = sheet['D'+str(index)].value
        
    
        
    date = datetime.date(datetime.strptime( sheet['B'+str(index)].value, "%Y-%m-%d"))
    
    
    try:
        match = Game.objects.filter(date=date).get(guest__name=guest)
    except Game.DoesNotExist:
        newMatch = Game(date = date)
        newMatch.host = Team.objects.get(name = host)
        newMatch.guest = Team.objects.get(name = guest)
        newMatch.save()
  
    index += 1