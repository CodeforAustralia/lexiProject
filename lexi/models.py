from django.db import models

# Create your models here.
class Message_Analysis(models.Model):
    input_text = models.CharField(max_length = 5000)
    output_text = models.CharField(max_length = 5000)
    total_words = models.IntegerField(default=0)
    common_words = models.IntegerField(default=0)
    uncommon_words = models.IntegerField(default=0)
    business_words = models.IntegerField(default=0)
    analysis_date = models.DateTimeField('analysis date')

    def __str__(self):
        return self.output_text
    def is_accessible(self):
        return ((self.common_words + self.business_words)/self.total_words) >= 0.8  #Higher than 80%

class Common_Word(models.Model):
    word = models.CharField(primary_key=True, max_length = 20)
    times = models.IntegerField(default=1)

    def __str__(self):
        return self.word

class Business_Word(models.Model):
    word = models.CharField(primary_key=True, max_length = 20)
    times = models.IntegerField(default=0)
    
    def __str__(self):
        return self.word

class Configuration(models.Model):
    THESAURUS = 'TH' 
    DATABASE = 'DB'
    AI_MODEL = 'AI'
    SOURCE_CHOICES = [
        (THESAURUS, 'Thesaurus'),
        (DATABASE, 'Database'),
        (AI_MODEL, 'AI Model'),
    ]
    source = models.CharField(
        max_length = 2,
        choices = SOURCE_CHOICES,
        default = THESAURUS
    )
    threshold = models.FloatField(default = 0.8) # Look if these is the best way of creating configuration variables. It will be only one record of the Configuration Model.

    def __str__(self):
        return ('Source: ' + self.source + ' - Threshold: ' + self.threshold)
    