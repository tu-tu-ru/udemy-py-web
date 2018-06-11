from django.db import models

import datetime 

from datetime import datetime, date, time, timedelta

from django.utils import timezone

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    # CharField stands for a box for typing
    publish_date = models.DateTimeField('date published')
      
    def __str__(self):
        return self.question_text
    
    def was_published_recently(self):
        return self.publish_date >= timezone.now() - timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # Modify the db
    choice_text = models.CharField(max_length=200)
    # Text of the options (choice)
    votes = models.IntegerField(default=0) 
    # count of votes
    # FIXME
    # The given value od default is 0 but it doesn't work.
    # Change it to 1 then works
    def __str__(self):
        return self.choice_text