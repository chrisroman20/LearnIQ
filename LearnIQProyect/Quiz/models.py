from django.db import models
from django.conf import settings

class Question(models.Model):
    QUESTION_TYPES = [
        ('visual', 'Visual'),
        ('auditory', 'Auditory'),
        ('kinesthetic', 'Kinesthetic'),
    ]
    
    text = models.TextField()
    image = models.ImageField(upload_to='questions/images/', blank=True, null=True)
    audio_file = models.FileField(upload_to='questions/audio/', blank=True, null=True)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    
    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return self.text

class QuizResult(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Asegura que solo haya un resultado por usuario
    visual_score = models.PositiveIntegerField(default=0)
    auditory_score = models.PositiveIntegerField(default=0)
    kinesthetic_score = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f'Result for {self.user.username}'
