from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Choices for paragraph difficulty
# These choices will be used in the admin panel to filter paragraphs by difficulty
DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('beginner', 'Beginner'),
        ('hard', 'Hard'),
    ]

class Paragraph(models.Model):
    text = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)

    def __str__(self):
        return f"{self.difficulty.title()} Paragraph #{self.id}" #display the difficulty and id in the admin panel like "Easy Paragraph #1" and .title() capitalizes the first letter of the difficulty

class TypingResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    wpm = models.FloatField()  # words per minute
    accuracy = models.FloatField()  # percentage
    timestamp = models.DateTimeField(auto_now_add=True)
    typos = models.IntegerField(default=0)
