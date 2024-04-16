from django.db import models
from django.utils.timezone import now


class Player(models.Model):
    name = models.CharField(max_length=32, null=True, blank=True)

    @property
    def sum_of_stats(self):
        total = sum(stats.total for stats in Stats.objects.filter(player=self))
        if total is not None:
            return total
        return 0

    def __str__(self):
        return self.name

class Stats(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    date = models.DateField()
    team = models.CharField(max_length=64)
    
    Pos = models.CharField(max_length=2)
    Rank = models.PositiveIntegerField()
    
    PPI = models.FloatField()
    MP = models.PositiveIntegerField()
    G = models.PositiveIntegerField()
    SOnT = models.PositiveIntegerField()
    SOffT= models.PositiveIntegerField()
    BS = models.PositiveIntegerField()
    OG = models.PositiveIntegerField()
    A = models.PositiveIntegerField()
    P = models.PositiveIntegerField()
    C = models.PositiveIntegerField()
    Tk = models.PositiveIntegerField()
    INT = models.PositiveIntegerField()
    FW = models.PositiveIntegerField()
    FC = models.PositiveIntegerField()
    O = models.PositiveIntegerField()
    YC = models.PositiveIntegerField()
    RC = models.PositiveIntegerField()
    GC = models.PositiveIntegerField()
    PW = models.PositiveIntegerField()
    SAV = models.PositiveIntegerField()
    Ca = models.PositiveIntegerField()
    KS = models.PositiveIntegerField()
    
    
    @property
    def total(self):
        return self.PPI
    
    def __str__(self):
        return f"{self.player.name}-{self.total}"
    
class Team(models.Model):
    name = models.CharField(max_length=64)
    
    @property
    def total(self):
        count = 0
        total_stats = 0
        #self.member_set.all().order_by("-total")[:12]
        total_stats = sum(member.player.sum_of_stats for member in self.member_set.all())
        return round(total_stats, 2)
    
    @property
    def average(self):
        return round(self.total / 12, 2)

    def __str__(self):
        return self.name
    
class Member(models.Model):
    date_start = models.DateField()
    date_end = models.DateField(null=True, blank=True)
    
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.player.name+"-"+self.team.name

class Game(models.Model):
    date = models.DateField()
    
    host = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="host_team")
    guest = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="guest_team",null=True, blank=True)
    
    played = models.BooleanField(default=False)
    
    @property
    def chances_host(self):
        fraction =  round((self.host.total + self.guest.total)/2 * 60 / 100, 2)
        return round( (self.host.total-fraction) / (self.host.total+self.guest.total-fraction*2) * 100, 2)
    
    
    @property
    def chances_guest(self):
        fraction =  round((self.host.total + self.guest.total)/2 * 60 / 100, 2)
        return round( (self.guest.total-fraction) / (self.host.total+self.guest.total-fraction*2) * 100, 2)
    
    def __str__(self):
        return self.host.name+"-"+self.guest.name+"-"+self.date
    
class Updated(models.Model):
    date = models.DateField(default=now)
    last_excel_read = models.PositiveIntegerField(default=0)
        
    def __str__(self):
        return self.date
    
