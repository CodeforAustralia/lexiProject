from django.db import models

# Create your models here.
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
    subset_common_words = models.IntegerField(null=False)

    def __str__(self):
        return ('Source: ' + self.source + ' - Threshold: ' + str(self.threshold*100)) + '% - Common Words subset: ' + str(self.subset_common_words)

    def get_source_description(self, code):
        for source in self.SOURCE_CHOICES:
            if code == source[0]:
                return source[1]

class Word(models.Model):
    word = models.CharField(primary_key=True, max_length=50)
    is_common = models.BooleanField(default=False)
    is_business_word = models.BooleanField(default=False)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    creation_user = models.CharField(max_length=20, default='admin')   # ToDo: Change using the session user request.session['member_id']
    suggestions = models.ManyToManyField(to='self')

    def __str__(self):
        return self.word

    # ToDo: Define the DB model to associate a suggestion for a uncommon word.
    # ToDo: Check and create properly encapsulation.
    