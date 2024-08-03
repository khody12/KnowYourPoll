from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Pollster(models.Model):
    name_of_pollster = models.CharField(max_length=75)
    info = models.TextField()
    quality_of_pollster = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    def __str__(self):
        return f"{self.name_of_pollster}"


class Poll(models.Model):
    harris_support = models.FloatField(null=False)
    trump_support = models.FloatField(null=False)
    third_party_support = models.FloatField(null=True)

    date_published = models.DateField()
    link_to_poll = models.URLField(null=True)
    type_of_voters = models.CharField(max_length=50)
    number_of_respondents = models.IntegerField()
    pollster = models.ForeignKey(Pollster, on_delete=models.CASCADE,related_name="polls") #if pollster is deleted, models.CASCADE makes it so all polls by said pollster are also deleted.
    
    def __str__(self):
        return f"{self.pollster.name_of_pollster} {self.date_published}"
    
    