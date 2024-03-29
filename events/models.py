from django.db import models

# Create your models here.


class Venue(models.Model):

    name = models.CharField('Venue Name' , max_length=120)
    address = models.CharField(max_length=300)
    zip_code = models.CharField('Zip Code' , max_length=15)
    phone = models.CharField('Contact Phone' , max_length=25)
    web = models.URLField('Website Address')
    email_address = models.EmailField('Email Address')

    def __str__(self): # Retorna o nome na área de admin
        return self.name


class MyClubUser(models.Model):

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField('User Email')

    def __str__(self): # Retorna o nome na área de admin
        return self.first_name + ' ' + self.last_name




class Event(models.Model):

    name = models.CharField('Event Name' , max_length=120)
    event_date = models.DateTimeField('Event Date')
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE) # -> Conecta a tabela "Event" a tabela "Venues"
    #venue = models.CharField(max_length=120)
    manager = models.CharField(max_length=60)
    description = models.TextField(blank=True)
    attendees = models.ManyToManyField(MyClubUser , blank=True)

    def __str__(self): # Retorna o nome na área de admin
        return self.name


